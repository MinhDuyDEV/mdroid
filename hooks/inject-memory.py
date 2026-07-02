#!/usr/bin/env python3
"""Layer 5: Inject relevant memories into context at session start.

Hook event: SessionStart (fires when Droid starts or resumes a session)
Input: JSON via stdin with session_id, cwd, source
Output: JSON stdout with hookSpecificOutput.additionalContext. Exit 0.
"""

import json
import os
import sys
import datetime

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from bm25 import rank_documents
from tfidf import compute_tf
from tokenize import tokenize
from markdown import read_memories


def get_memories_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memories.md")


def get_active_slug(cwd: str) -> str:
    active_path = os.path.join(cwd, ".factory", "artifacts", ".active")
    if os.path.exists(active_path):
        try:
            with open(active_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except IOError:
            pass
    return ""


def read_artifact(cwd: str, slug: str, filename: str) -> str:
    if not slug:
        return ""
    path = os.path.join(cwd, ".factory", "artifacts", slug, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            pass
    return ""


def read_agents_md(cwd: str) -> str:
    path = os.path.join(cwd, "AGENTS.md")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            pass
    return ""


def read_rules(cwd: str) -> str:
    """Read all .factory/rules/*.md files and concatenate their content.

    Rules files contain coding standards that Droid follows. Including them
    in the BM25 query context helps inject memories relevant to the active
    coding conventions.
    """
    rules_dir = os.path.join(cwd, ".factory", "rules")
    if not os.path.isdir(rules_dir):
        return ""
    import glob
    parts = []
    for path in sorted(glob.glob(os.path.join(rules_dir, "*.md"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                parts.append(f.read())
        except IOError:
            pass
    return "\n".join(parts)


def read_session_intent(cwd: str) -> str:
    """Read intent from session-state.json as a fallback query source."""
    path = os.path.join(cwd, ".factory", "memory", "session-state.json")
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("intent", "")
    except (json.JSONDecodeError, IOError):
        return ""


def extract_query_terms(context_texts: list) -> list:
    """Extract query terms from context texts using TF."""
    all_tokens = []
    for text in context_texts:
        if text:
            all_tokens.extend(tokenize(text))
    if not all_tokens:
        return []
    tf = compute_tf(all_tokens)
    # Sort by TF descending, return top 30
    sorted_terms = sorted(tf.items(), key=lambda x: x[1], reverse=True)
    return [term for term, _ in sorted_terms[:30]]


def apply_recency_boost(score: float, obs_date: str) -> float:
    """Apply recency boost.

    Recent observations are boosted, with the boost decaying toward 1.0 as the
    observation ages. Formula: boost = 1.0 + 0.1 * (30 - min(days_since, 30)) / 30
    - Today (0 days): boost = 1.1
    - 15 days:       boost = 1.05
    - 30+ days:      boost = 1.0 (no penalty, just no boost)

    Args:
        score: The base BM25 score.
        obs_date: Observation date in YYYY-MM-DD format.

    Returns:
        Boosted score.
    """
    if not obs_date:
        return score
    try:
        obs_datetime = datetime.datetime.strptime(obs_date, "%Y-%m-%d")
        now = datetime.datetime.now()
        days_since = max(0, (now - obs_datetime).days)
        recency_factor = (30 - min(days_since, 30)) / 30  # 1.0 -> 0.0
        boost = 1.0 + 0.1 * recency_factor
        return score * boost
    except (ValueError, TypeError):
        return score


def apply_confidence_boost(score: float, confidence: str) -> float:
    """Apply confidence boost: high=1.2x, medium=1.0x, low=0.8x."""
    confidence = (confidence or "medium").lower()
    if confidence == "high":
        return score * 1.2
    elif confidence == "low":
        return score * 0.8
    return score


def format_context(scored_observations: list) -> str:
    """Format scored observations into context string."""
    if not scored_observations:
        return ""
    lines = [
        "<memory_context>",
        "Relevant knowledge from previous sessions:",
        "",
    ]
    for obs, score in scored_observations:
        obs_type = obs.get("type", "unknown")
        title = obs.get("title", "Untitled")
        content = obs.get("content", "")
        lines.append(f"### [{obs_type}] {title} (relevance: {score:.2f})")
        lines.append(content)
        lines.append("")
    lines.append("</memory_context>")
    return "\n".join(lines)


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    cwd = input_data.get("cwd", os.getcwd())

    memories_path = get_memories_path(cwd)
    if not os.path.exists(memories_path):
        sys.exit(0)

    observations = read_memories(memories_path)
    if not observations:
        sys.exit(0)

    # Build context for query term extraction
    slug = get_active_slug(cwd)
    context_texts = []
    if slug:
        context_texts.append(read_artifact(cwd, slug, "spec.md"))
        context_texts.append(read_artifact(cwd, slug, "plan.md"))
        context_texts.append(read_artifact(cwd, slug, "progress.md"))
    agents_md = read_agents_md(cwd)
    if agents_md:
        context_texts.append(agents_md)
    rules_text = read_rules(cwd)
    if rules_text:
        context_texts.append(rules_text)
    # Fallback: if no artifacts, no AGENTS.md, and no rules, use session intent
    if not any(context_texts):
        intent = read_session_intent(cwd)
        if intent:
            context_texts.append(intent)

    query_terms = extract_query_terms(context_texts)
    if not query_terms:
        sys.exit(0)

    # Build documents for BM25
    documents = []
    for i, obs in enumerate(observations):
        doc_text = obs.get("title", "") + " " + obs.get("content", "")
        documents.append((i, doc_text))

    # Rank by BM25
    ranked = rank_documents(query_terms, documents, top_n=10)

    # Apply boosts and filter
    scored_observations = []
    for idx, score in ranked:
        if score < 0.3:
            continue
        obs = observations[idx]
        boosted_score = apply_recency_boost(score, obs.get("date", ""))
        boosted_score = apply_confidence_boost(boosted_score, obs.get("confidence", "medium"))
        scored_observations.append((obs, boosted_score))

    # Sort by boosted score, take top 5
    scored_observations.sort(key=lambda x: x[1], reverse=True)
    scored_observations = scored_observations[:5]

    context = format_context(scored_observations)
    if not context:
        sys.exit(0)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()

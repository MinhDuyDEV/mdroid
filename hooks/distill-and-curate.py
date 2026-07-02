#!/usr/bin/env python3
"""Layer 3+4: Distill transcript (TF-IDF) then curate observations (regex).

This combined script replaces the separate distill-session.py and
curate-observations.py hooks. Factory runs multiple Stop hooks in
PARALLEL, which caused a race condition: curate read the distillation
file before distill finished writing it. Merging into a single script
guarantees sequential execution: distill -> curate.

Hook event: Stop (fires when Droid finishes responding)
Input: JSON via stdin with session_id, transcript_path, cwd
Output: Exit 0 (silent). Writes distillation + appends to memories.md.
"""

import json
import os
import sys
import datetime
import re

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from tfidf import extract_top_terms, select_key_sentences
from patterns import match_patterns, extract_concepts
from markdown import append_observation, get_existing_titles, is_duplicate


# ---------------------------------------------------------------------------
# Layer 3: Distillation (TF-IDF)
# ---------------------------------------------------------------------------

def get_distill_dir(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memory", "distillations")


def read_transcript(transcript_path: str) -> list:
    """Read a JSONL transcript and extract user + assistant text messages.

    Factory transcript format: each line is a JSON object with:
      - "type": "message" | "session_start" | "todo_state" | ...
      - "message": {"role": "user"|"assistant", "content": [...] | "...", ...}

    Content can be a list of blocks (each with "type": "text"|"tool_use"|"tool_result"|"thinking")
    or a plain string. We extract only "text" blocks, skipping system-reminders and tool I/O.

    Returns a list of message strings.
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    messages = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Only process message-type entries
                if entry.get("type") != "message":
                    continue
                # Role and content are nested under "message"
                msg = entry.get("message", {})
                if not isinstance(msg, dict):
                    continue
                role = msg.get("role", "")
                if role not in ("user", "assistant"):
                    continue
                content = msg.get("content", "")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict):
                            if block.get("type") == "text":
                                text_parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    content = " ".join(text_parts)
                if not isinstance(content, str) or not content.strip():
                    continue
                # Skip system-reminder blocks and pure JSON tool inputs
                if content.startswith("<system") or content.startswith("{"):
                    continue
                messages.append(content)
    except IOError:
        pass
    return messages


def distill(messages: list, session_id: str) -> str:
    """Distill messages into a concise summary using TF-IDF."""
    if not messages:
        return f"# Distillation: {session_id}\n(No text messages to distill)\n"

    top_terms = extract_top_terms(messages, top_n=20)
    key_content = select_key_sentences(messages, top_terms, target_length=2000)

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    lines = [
        f"# Distillation: {session_id}",
        f"**Timestamp**: {timestamp}",
        "",
        f"## Top Terms: {', '.join(top_terms) if top_terms else '(none)'}",
        "",
        "## Key Content:",
        key_content if key_content else "(no key content extracted)",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Layer 4: Curation (regex pattern matching)
# ---------------------------------------------------------------------------

def get_memories_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memories.md")


def read_distillation(path: str) -> str:
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError:
        return ""


def split_sentences(text: str) -> list:
    """Split text into sentences, filtered for context."""
    if not text:
        return []
    lines = text.split("\n")
    content_lines = [
        line for line in lines
        if not line.startswith("#") and not line.startswith("**") and line.strip()
    ]
    content = " ".join(content_lines)
    raw = re.split(r"(?<=[.!?])\s+", content)
    return [s.strip() for s in raw if len(s.strip()) > 30]


# ---------------------------------------------------------------------------
# Combined pipeline
# ---------------------------------------------------------------------------

def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")
    cwd = input_data.get("cwd", os.getcwd())

    # -- Layer 3: Distill --
    messages = read_transcript(transcript_path)
    distillation = distill(messages, session_id)

    distill_dir = get_distill_dir(cwd)
    os.makedirs(distill_dir, exist_ok=True)
    distill_path = os.path.join(distill_dir, f"{session_id}.md")
    with open(distill_path, "w", encoding="utf-8") as f:
        f.write(distillation)

    # -- Layer 4: Curate (runs AFTER distill is written, guaranteed) --
    if not distillation or "(No text messages to distill)" in distillation:
        sys.exit(0)

    sentences = split_sentences(distillation)
    if not sentences:
        sys.exit(0)

    memories_path = get_memories_path(cwd)
    existing_titles = get_existing_titles(memories_path)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    for sentence in sentences:
        result = match_patterns(sentence)
        if result is None:
            continue
        obs_type, title = result

        if is_duplicate(title, existing_titles):
            continue

        concepts = extract_concepts(sentence, max_concepts=5)
        observation = {
            "date": today,
            "title": title,
            "type": obs_type,
            "confidence": "medium",
            "content": sentence.strip(),
            "concepts": concepts,
        }
        append_observation(memories_path, observation)
        existing_titles.add(title)

    sys.exit(0)


if __name__ == "__main__":
    main()

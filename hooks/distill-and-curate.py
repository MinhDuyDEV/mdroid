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
from markdown import append_observation, get_existing_titles, get_existing_contents, is_duplicate, is_content_duplicate


# ---------------------------------------------------------------------------
# Layer 3: Distillation (TF-IDF)
# ---------------------------------------------------------------------------

def get_distill_dir(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memory", "distillations")


# Markers that strongly identify a message as leaked hook output / memory
# context rather than genuine user or assistant prose. If ANY of these appear
# in a message, the entire message is skipped. These are specific enough that
# they essentially never appear in a genuine engineering discussion.
_STRONG_LEAK_MARKERS = (
    "<memory_context>",
    "</memory_context>",
    "hookSpecificOutput",
    "additionalContext",
    "Exit code",
)

# Weaker markers that only flag a message as leaked when TWO OR MORE co-occur.
# A single script-name mention in genuine discussion (e.g. "I fixed the bug in
# distill-and-curate.py") is not enough to skip the message, but a message
# containing both a script name AND a relevance marker is almost certainly
# leaked hook output.
_WEAK_LEAK_MARKERS = (
    "inject-memory.py",
    "distill-and-curate.py",
    "track-artifacts.py",
    "memory-capture-manual.py",
    "save-summary.py",
)


def _is_leaked_output(content: str) -> bool:
    """Return True if content looks like leaked hook output or memory context.

    Hook output leaks into transcripts two ways:
    1. The raw additionalContext block (contains <memory_context> tags).
    2. The rendered hook display text (contains hookSpecificOutput, Exit code,
       script names) that the CLI prints and that users sometimes paste back.
    Either way, re-ingesting it creates garbage observations, so we skip it.

    Strong markers (hookSpecificOutput, additionalContext, <memory_context>,
    Exit code, (relevance:)) skip the message on their own. Weak markers
    (script names) only skip the message when 2+ co-occur, so that a single
    genuine mention of a script name in discussion is not over-filtered.
    """
    # Strong markers: any one is enough to skip.
    for marker in _STRONG_LEAK_MARKERS:
        if marker in content:
            return True
    # Detect the "(relevance: N.NN)" signature emitted by inject-memory.py.
    if re.search(r"\(relevance:\s*\d", content):
        return True
    # Weak markers: need 2+ to co-occur to skip (avoids over-filtering genuine
    # discussion that merely mentions a script name).
    weak_hits = sum(1 for marker in _WEAK_LEAK_MARKERS if marker in content)
    if weak_hits >= 2:
        return True
    return False


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
                # Skip system-reminder blocks and pure JSON tool inputs.
                if content.startswith("<system") or content.startswith("{"):
                    continue
                # Skip leaked hook output / injected memory context. Re-ingesting
                # it lets the curator create garbage observations whose titles
                # are fragments like "(relevance: 1.64)\n..." pulled straight
                # from the injected context, causing a self-reinforcing
                # corruption loop.
                if _is_leaked_output(content):
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
    """Split text into sentences, filtered for context.

    Skips sentences that look like leaked hook output (memory_context
    fragments, relevance markers, escaped-newline artifacts) so they can
    never become observation titles/content.
    """
    if not text:
        return []
    lines = text.split("\n")
    content_lines = [
        line for line in lines
        if not line.startswith("#") and not line.startswith("**") and line.strip()
    ]
    content = " ".join(content_lines)
    raw = re.split(r"(?<=[.!?])\s+", content)
    out = []
    for s in raw:
        s = s.strip()
        if len(s) <= 30:
            continue
        # Reject sentences carrying hook-output markers or escaped newlines.
        # These appear when a transcript re-contains inject-memory output.
        # Note: after json.loads, JSON-escaped \\n becomes real newlines, so
        # we must check for the literal two-char sequence (backslash + n) that
        # survives in the *rendered display text* users paste back, AND for
        # the real newline form via the earlier split (already handled above).
        if (
            "(relevance:" in s
            or "\\n" in s
            or "<memory_context>" in s
            or "</memory_context>" in s
            or "hookSpecificOutput" in s
            or "additionalContext" in s
            or "### [" in s
            or "inject-memory.py" in s
            or "Exit code" in s
        ):
            continue
        out.append(s)
    return out


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
    existing_contents = get_existing_contents(memories_path)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    for sentence in sentences:
        result = match_patterns(sentence)
        if result is None:
            continue
        obs_type, title = result

        if is_duplicate(title, existing_titles):
            continue

        content = sentence.strip()
        # Content-level dedup catches re-ingested memory context that slipped
        # through with slightly different titles (different relevance scores)
        # but the same underlying sentence.
        if is_content_duplicate(content, existing_contents):
            continue

        concepts = extract_concepts(sentence, max_concepts=5)
        observation = {
            "date": today,
            "title": title,
            "type": obs_type,
            "confidence": "medium",
            "content": content,
            "concepts": concepts,
        }
        append_observation(memories_path, observation)
        existing_titles.add(title)
        existing_contents.add(content)

    sys.exit(0)


if __name__ == "__main__":
    main()

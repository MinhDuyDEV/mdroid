#!/usr/bin/env python3
"""Layer 1: Track file artifacts during a session.

Hook events: PreToolUse (Read|Edit|Create|ApplyPatch) + PostToolUse (same)
Input: JSON via stdin with session_id, tool_name, tool_input, tool_response, cwd
Output: Exit 0 (silent). Writes to .factory/memory/session-state.json
"""

import json
import os
import sys
import re
import datetime
import tempfile

# Add lib to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/lib")


def get_state_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memory", "session-state.json")


def load_state(path: str, session_id: str) -> dict:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "session_id": session_id,
        "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "intent": "",
        "files_read": [],
        "files_modified": [],
        "files_created": [],
        "decisions": [],
    }


def save_state(path: str, state: dict) -> None:
    """Atomically write state JSON to avoid corruption from concurrent hooks."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Write to a temp file first, then rename for atomicity.
    fd, tmp_path = tempfile.mkstemp(
        dir=os.path.dirname(path), suffix=".tmp", prefix=".session-state-"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def extract_file_path(tool_input: dict) -> str:
    """Extract file path from tool input."""
    return tool_input.get("file_path") or tool_input.get("path") or ""


def extract_decisions(content: str) -> list:
    """Extract decision sentences from content."""
    if not content:
        return []
    decisions = []
    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", content)
    decision_keywords = re.compile(
        r"\b(decided to|chose to|went with|opted for|switched to|migrated to|"
        r"settled on|we should|let's use)\b", re.IGNORECASE
    )
    for sent in sentences:
        if decision_keywords.search(sent) and len(sent) < 200:
            decisions.append({
                "title": sent.strip()[:80],
                "rationale": sent.strip(),
                "time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            })
    return decisions


def enforce_limits(state: dict) -> None:
    """Enforce size limits on lists in state."""
    state["files_read"] = state["files_read"][-100:]
    state["files_modified"] = state["files_modified"][-50:]
    state["files_created"] = state["files_created"][-20:]
    state["decisions"] = state["decisions"][-10:]


def _extract_first_user_intent(transcript_path: str) -> str:
    """Read the transcript JSONL and return the first user message text.

    This is used as a fallback to populate the session intent when the
    UserPromptSubmit hook hasn't populated it yet.
    """
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
                if entry.get("role") != "user":
                    continue
                content = entry.get("content", "")
                if isinstance(content, list):
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))
                        elif isinstance(block, str):
                            parts.append(block)
                    content = " ".join(parts)
                if isinstance(content, str) and content.strip():
                    # Skip system-reminder blocks and JSON tool inputs
                    text = content.strip()
                    if text.startswith("{") or text.startswith("<system"):
                        continue
                    return text[:200]
    except IOError:
        pass
    return ""


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    session_id = input_data.get("session_id", "unknown")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    cwd = input_data.get("cwd", os.getcwd())

    state_path = get_state_path(cwd)
    state = load_state(state_path, session_id)

    # Update session_id if changed
    if state.get("session_id") != session_id:
        state["session_id"] = session_id

    file_path = extract_file_path(tool_input)
    if not file_path:
        sys.exit(0)

    # Make path relative to cwd if possible
    if file_path.startswith(cwd):
        file_path = os.path.relpath(file_path, cwd)

    # Skip mdroid's own runtime files to avoid self-referential noise.
    if ".factory/memory/" in file_path or file_path == ".factory/memories.md":
        sys.exit(0)

    if tool_name == "Read":
        if file_path not in state["files_read"]:
            state["files_read"].append(file_path)
    elif tool_name in ("Edit", "ApplyPatch"):
        if file_path not in state["files_modified"]:
            state["files_modified"].append(file_path)
    elif tool_name == "Create":
        if file_path not in state["files_created"]:
            state["files_created"].append(file_path)

    # Extract decisions from tool input content
    content = ""
    if isinstance(tool_input.get("content"), str):
        content = tool_input["content"]
    elif isinstance(tool_input.get("new_str"), str):
        content = tool_input["new_str"]
    elif isinstance(tool_input.get("patch"), str):
        content = tool_input["patch"]

    new_decisions = extract_decisions(content)
    state["decisions"].extend(new_decisions)

    # Capture intent from the first user prompt (UserPromptSubmit fires before
    # tools, but PreToolUse may fire first in some flows; check transcript).
    if not state.get("intent"):
        transcript_path = input_data.get("transcript_path", "")
        if transcript_path and os.path.exists(transcript_path):
            intent = _extract_first_user_intent(transcript_path)
            if intent:
                state["intent"] = intent

    enforce_limits(state)
    save_state(state_path, state)
    sys.exit(0)


if __name__ == "__main__":
    main()

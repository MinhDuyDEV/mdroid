#!/usr/bin/env python3
"""Layer 2: Save anchored session summary before context compression.

Hook event: PreCompact (fires before Droid compresses context)
Input: JSON via stdin with session_id, trigger, cwd
Output: Exit 0 (silent). Writes to .factory/memory/session-summary.md
"""

import json
import os
import sys
import datetime


def get_state_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memory", "session-state.json")


def get_summary_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memory", "session-summary.md")


def get_active_slug(cwd: str) -> str:
    active_path = os.path.join(cwd, ".factory", "artifacts", ".active")
    if os.path.exists(active_path):
        try:
            with open(active_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except IOError:
            pass
    return ""


def read_progress(cwd: str, slug: str) -> str:
    if not slug:
        return ""
    progress_path = os.path.join(cwd, ".factory", "artifacts", slug, "progress.md")
    if os.path.exists(progress_path):
        try:
            with open(progress_path, "r", encoding="utf-8") as f:
                return f.read()
        except IOError:
            pass
    return ""


def format_summary(state: dict, progress: str, slug: str) -> str:
    lines = ["# Session Summary", ""]

    intent = state.get("intent", "")
    if not intent:
        intent = "(not captured - see files for session intent)"
    lines.append(f"## Intent: {intent}")
    lines.append("")

    files_read = state.get("files_read", [])
    if files_read:
        lines.append("## Files Read:")
        for f in files_read:
            lines.append(f"- `{f}`")
        lines.append("")

    files_modified = state.get("files_modified", [])
    if files_modified:
        lines.append("## Files Modified:")
        for f in files_modified:
            lines.append(f"- `{f}`")
        lines.append("")

    files_created = state.get("files_created", [])
    if files_created:
        lines.append("## Files Created:")
        for f in files_created:
            lines.append(f"- `{f}`")
        lines.append("")

    decisions = state.get("decisions", [])
    if decisions:
        lines.append("## Decisions:")
        for d in decisions:
            title = d.get("title", "")
            rationale = d.get("rationale", "")
            lines.append(f"- **{title}**: {rationale}")
        lines.append("")

    if progress:
        lines.append("## Next Steps:")
        lines.append("(From progress.md)")
        lines.append("```")
        lines.append(progress)
        lines.append("```")
        lines.append("")
    elif slug:
        lines.append("## Next Steps:")
        lines.append(f"Continue work on feature: {slug}")
        lines.append("")
    else:
        lines.append("## Next Steps:")
        lines.append("(No active feature - check for new tasks)")
        lines.append("")

    return "\n".join(lines)


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    session_id = input_data.get("session_id", "unknown")
    cwd = input_data.get("cwd", os.getcwd())

    state_path = get_state_path(cwd)
    state = {}
    if os.path.exists(state_path):
        try:
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)
        except (json.JSONDecodeError, IOError):
            state = {}

    slug = get_active_slug(cwd)
    progress = read_progress(cwd, slug)

    summary = format_summary(state, progress, slug)
    summary_path = get_summary_path(cwd)
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    sys.exit(0)


if __name__ == "__main__":
    main()

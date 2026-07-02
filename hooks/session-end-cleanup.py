#!/usr/bin/env python3
"""SessionEnd cleanup: remove ephemeral session state.

Hook event: SessionEnd (fires when a Droid session ends)
Input: JSON via stdin with session_id, cwd, reason
Output: Exit 0 (silent). Removes session-state.json and session-summary.md.

This cleans up ephemeral files that are only useful during an active session.
Long-term memory (.factory/memories.md) and distillations/ are preserved.
"""

import json
import os
import sys


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    cwd = input_data.get("cwd", os.getcwd())
    reason = input_data.get("reason", "other")

    memory_dir = os.path.join(cwd, ".factory", "memory")

    # Clean up ephemeral session state
    state_path = os.path.join(memory_dir, "session-state.json")
    if os.path.exists(state_path):
        try:
            os.remove(state_path)
        except OSError:
            pass

    # Clean up session summary (only useful for context compression, which
    # already happened if PreCompact fired)
    summary_path = os.path.join(memory_dir, "session-summary.md")
    if os.path.exists(summary_path):
        try:
            os.remove(summary_path)
        except OSError:
            pass

    # Note: We do NOT remove:
    # - .factory/memories.md (long-term curated observations)
    # - .factory/memory/distillations/ (historical session distillations)
    # - .factory/artifacts/ (feature work records)

    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Manual memory capture: user prefixes messages with # (project) or ## (personal).

Hook event: UserPromptSubmit
Input: JSON via stdin with prompt, session_id, cwd
Output: JSON stdout with systemMessage. Exit 0.
"""

import json
import os
import sys
import datetime


def get_project_memories_path(cwd: str) -> str:
    return os.path.join(cwd, ".factory", "memories.md")


def get_personal_memories_path() -> str:
    home = os.path.expanduser("~")
    return os.path.join(home, ".factory", "memories.md")


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)

    prompt = input_data.get("prompt", "")
    cwd = input_data.get("cwd", os.getcwd())

    if not prompt:
        sys.exit(0)

    # Check for ## prefix (personal memory) or # prefix (project memory)
    is_personal = prompt.startswith("##")
    is_project = prompt.startswith("#") and not is_personal

    if not is_personal and not is_project:
        sys.exit(0)

    # Extract content (strip the # or ## prefix)
    if is_personal:
        content = prompt[2:].strip()
        path = get_personal_memories_path()
    else:
        content = prompt[1:].strip()
        path = get_project_memories_path(cwd)

    if not content:
        sys.exit(0)

    # Append to memories file in the same format the auto-curator uses,
    # so inject-memory.py can parse it via markdown.read_memories().
    os.makedirs(os.path.dirname(path), exist_ok=True)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # Truncate title to 80 chars to match curator convention
    title = content[:80]
    block = (
        f"\n### [{today}]: {title}\n"
        f"**Type**: manual\n"
        f"**Confidence**: high\n"
        f"**Content**: {content}\n"
        f"**Concepts**: []\n"
    )

    with open(path, "a", encoding="utf-8") as f:
        f.write(block)

    scope = "personal" if is_personal else "project"
    output = {
        "systemMessage": f"Saved to {scope} memories: {path}"
    }
    print(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()

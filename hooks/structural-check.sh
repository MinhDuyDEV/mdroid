#!/bin/bash
# structural-check.sh - Validate architecture constraints after file edits.
# Hook event: PostToolUse (Create|Edit|ApplyPatch)
# Input: JSON via stdin (same as other hooks)
# Output: Exit 2 (block) if violation found, stderr sent to Droid. Exit 0 if clean.

# Note: Do NOT use `set -e` here. We need grep to return exit code 1 (no match)
# without aborting the script, and we handle all error paths explicitly.

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Get the filename and check if it's within a plugin/skill directory
FILENAME=$(basename "$FILE_PATH")
DIRNAME=$(dirname "$FILE_PATH")

# Check 3: No .env files in changes (check first, before any skips)
case "$FILENAME" in
    .env|.env.*|*.env)
        echo "STRUCTURAL CHECK FAILED: .env files should not be created or edited directly." >&2
        echo "Use environment variables or a secrets manager instead." >&2
        exit 2
        ;;
esac

# Skip non-md, non-py, non-sh files
case "$FILENAME" in
    *.md|*.py|*.sh) ;;
    *) exit 0 ;;
esac

# Skip files outside the workspace (e.g., in node_modules, .git, etc.)
case "$FILE_PATH" in
    *node_modules*|*.git/*|*/tmp/*|*.factory/memory/*|*.factory/artifacts/*) exit 0 ;;
esac

# Check 1: Plugin/skill SKILL.md files should be under 300 lines
if [ "$FILENAME" = "SKILL.md" ] && [ -f "$FILE_PATH" ]; then
    LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
    if [ "$LINE_COUNT" -gt 300 ]; then
        echo "STRUCTURAL CHECK FAILED: $FILE_PATH has $LINE_COUNT lines (max 300 for skill files)." >&2
        echo "Consider splitting the skill or reducing content." >&2
        exit 2
    fi
fi

# Check 2: Droid .md files should be under 500 lines
case "$DIRNAME" in
    */droids*)
        if [ -f "$FILE_PATH" ]; then
            LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
            if [ "$LINE_COUNT" -gt 500 ]; then
                echo "STRUCTURAL CHECK FAILED: $FILE_PATH has $LINE_COUNT lines (max 500 for droid files)." >&2
                echo "Consider simplifying the droid prompt." >&2
                exit 2
            fi
        fi
        ;;
esac

# Check 5: .factory/rules/ files should be under 200 lines and have rule structure
case "$DIRNAME" in
    */.factory/rules*|*/rules*)
        if [ -f "$FILE_PATH" ] && [[ "$FILENAME" == *.md ]]; then
            LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
            if [ "$LINE_COUNT" -gt 200 ]; then
                echo "STRUCTURAL CHECK FAILED: $FILE_PATH has $LINE_COUNT lines (max 200 for rules files)." >&2
                echo "Split rules into separate files by category." >&2
                exit 2
            fi
            # Check for at least one rule pattern (Applies to / Rule:)
            if ! grep -qE '\*\*Applies to\*\*|\*\*Rule\*\*' "$FILE_PATH"; then
                echo "STRUCTURAL CHECK WARNING: $FILE_PATH may lack rule structure (expected **Applies to** and **Rule** fields)." >&2
                # Warning only, don't block
            fi
        fi
        ;;
esac

# Check 4: Kebab-case filenames for skill/droid directories
case "$DIRNAME" in
    */skills/*|*/droids/*)
        # Check for non-kebab-case (uppercase, underscores, spaces)
        if echo "$FILENAME" | grep -qE '[A-Z _]'; then
            # Allow SKILL.md and .md files with standard naming
            if [ "$FILENAME" != "SKILL.md" ]; then
                echo "STRUCTURAL CHECK WARNING: $FILENAME uses non-kebab-case naming." >&2
                echo "Use lowercase with hyphens (e.g., my-skill.md)." >&2
                # Warning only, don't block
            fi
        fi
        ;;
esac

exit 0

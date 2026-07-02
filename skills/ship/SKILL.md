---
name: ship
description: Commit, create PR, and clean up after verification and review pass. Stages specific files, uses conventional commit format, and never pushes without confirmation. Use after /verify and /review.
user-invocable: true
disable-model-invocation: true
---

# /ship - Commit, PR, Deploy

Ship verified, reviewed work. Lean command: just commit, PR, cleanup.

## Pre-conditions

Before shipping, verify:
1. `/verify` passed (all gates green). Check `.factory/artifacts/<slug>/verify.log`.
2. `/review` passed (no unresolved critical issues). Check `.factory/artifacts/<slug>/review.md`.

If either is missing or failed:
- No verify -> suggest `/verify` first.
- Verify failed -> suggest `/fix` then `/verify`.
- No review -> ask user: "Skip review? (not recommended)" or suggest `/review`.
- Review has critical issues -> suggest `/fix` then re-`/review`.

## Phase 1: Confirm with user

Use AskUser:
- "Ready to ship [feature name]. This will commit the changes. Proceed?"
- "Create a PR after commit? (yes/no)"

Never push or create a PR without explicit confirmation.

## Phase 2: Stage specific files

1. Run `git status` to see changed files.
2. Stage ONLY the files related to this feature. NEVER `git add .` or `git add -A`.
3. Verify staged files with `git diff --cached --name-only`.

If there are files that shouldn't be committed (artifacts, logs, temp files), exclude them.

## Phase 3: Commit

1. Run `git diff --cached` to review ALL staged changes.
2. Check for secrets, credentials, API keys, or sensitive data in the diff. If found -> STOP, warn the user.
   - Note: Droid Shield (enabled by default) also scans for secrets on git commits and pushes. It is a safety net, but you should still review the diff manually. Do not rely on Shield alone.
3. Craft a conventional commit message:
   - `feat: [description]` for new features
   - `fix: [description]` for bug fixes
   - `test: [description]` for test-only changes
   - `refactor: [description]` for refactoring
   - `docs: [description]` for documentation
   - `chore: [description]` for tooling, deps, config
4. Commit: `git commit -m "<type>: <description>"`
5. Record the commit hash.
   - Autonomy note: Committing requires Medium autonomy or higher. If at Off/Low, Droid will prompt for approval.

## Phase 4: Create PR (if requested)

1. Determine the base branch: `git rev-parse --abbrev-ref HEAD` for current, use default branch as base.
2. Push the branch: `git push -u origin <branch>` (only if user confirmed).
   - Autonomy note: Pushing requires High autonomy. If below High, Droid will prompt for approval.
3. Create PR using `gh pr create` with:
   - Title: the commit message summary.
   - Body: summary of changes, link to spec, verification status, review status.
4. Return the PR URL.

## Phase 5: Update progress

Update `.factory/artifacts/<slug>/progress.md`:
- Mark all tasks as complete.
- Record final commit hash and PR URL.
- Add completion timestamp.

## Phase 6: Clean up

1. Remove `.factory/artifacts/.active` (the feature is shipped).
2. Leave the artifact directory intact (it's a record of the work).
3. Suggest: "Feature shipped. Run /spec for the next feature."

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll just use git add ., it's faster" | Never. `git add .` commits stray files, artifacts, logs. Stage specific files. |
| "The diff looks fine, I'll skip reviewing it" | Always review `git diff --cached` before commit. Secrets hide in diffs. |
| "I'll push without asking" | Never push without explicit user confirmation. |
| "Review can wait until after ship" | No. Critical issues in production cost more. Review first. |
| "The commit message doesn't matter" | Conventional commits enable changelogs and releases. Use them. |

## Red Flags

- Using `git add .` or `git add -A`.
- Commiting without reviewing `git diff --cached`.
- Pushing or creating a PR without user confirmation.
- Shipping with unresolved critical review findings.
- Shipping with failing verification gates.
- No commit message type prefix.
- Secrets or credentials in the committed diff.

## Related Commands

- `/verify` - Run verification gates before shipping.
- `/review` - Run multi-persona review before shipping.
- `/fix` - Fix issues blocking ship.

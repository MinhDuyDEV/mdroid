---
name: clean
description: Remove stale artifact directories and reset the active slug. Use to clean up .factory/artifacts/ after features are shipped or abandoned.
user-invocable: true
disable-model-invocation: true
---

# /clean - Artifact Cleanup

Remove stale artifact directories and reset session state.

## Modes

- **`/clean`**: Remove artifact directories for features that are shipped (progress.md marked complete) or have no spec.md.
- **`/clean --all`**: Remove ALL artifact directories (keep .active if it points to an in-progress feature).
- **`/clean --slug <slug>`**: Remove a specific feature's artifact directory.

## Phase 1: Inspect

1. List `.factory/artifacts/` directories.
2. For each, check:
   - Does `spec.md` exist?
   - Does `progress.md` exist and is it marked complete?
   - Does it match the current `.active` slug?
3. Read `.factory/artifacts/.active` to find the current feature slug (if any).

## Phase 2: Classify

| State | Action |
|---|---|
| Shipped (progress.md has "Completed: <date>" and "PR: <url>") | Remove |
| Abandoned (spec.md exists but no progress.md, or progress.md has no commits) | Remove |
| Active (matches .active slug, progress.md shows in-progress work) | Keep |
| No spec.md (orphaned directory) | Remove |
| `--all` mode | Remove all except active |

## Phase 3: Confirm with user

Show the user the list of directories to remove and ask for confirmation. Never remove without asking.

```
Directories to remove:
  .factory/artifacts/old-feature-1/ (shipped, PR #42)
  .factory/artifacts/abandoned-feature/ (no progress)

Keep:
  .factory/artifacts/current-feature/ (active, in progress)

Proceed? (yes/no)
```

## Phase 4: Remove

For each confirmed directory:
1. `rm -rf .factory/artifacts/<slug>/`
2. If the removed slug matches `.active`, remove `.factory/artifacts/.active`.

## Phase 5: Clean session state (optional)

If `--all` mode or no active feature remains:
1. Remove `.factory/memory/session-state.json` (stale file trail).
2. Remove `.factory/memory/session-summary.md` (stale summary).
3. Leave `.factory/memories.md` intact (long-term memory, always keep).
4. Leave `.factory/memory/distillations/` intact (historical distillations, keep for reference).

## Phase 6: Report

```
Cleaned up:
  - Removed 3 artifact directories
  - Removed .active pointer
  - Removed stale session-state.json

Kept:
  - .factory/memories.md (long-term memory)
  - .factory/memory/distillations/ (5 files)
  - .factory/artifacts/current-feature/ (active)
```

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll clean up later" | Stale directories confuse future sessions and bloat the repo. Clean now. |
| "The old artifacts might be useful" | Shipped features have PRs. The artifact is redundant. Remove it. |
| "I'll just delete everything" | Don't. memories.md and active features must be preserved. Use the classification. |

## Red Flags

- Removing the active feature's directory.
- Removing `.factory/memories.md`.
- Removing without user confirmation.
- Removing distillations/ (historical record, keep unless explicitly asked).

---
name: fix
description: Debug and fix bugs with minimal, root-cause changes. Reproduce, isolate, fix, verify. Use for bugfixes (2-3 files) or to resolve issues found by /verify or /review.
user-invocable: true
disable-model-invocation: true
---

# /fix - Debug and Fix Bugs

Resolve bugs with minimal, root-cause fixes. No shotgunning.

## Phase 1: Reproduce

1. Understand the bug from the user's description or the failing test output.
2. Reproduce it:
   - If there's a failing test, run it: `[test command] [test name]`.
   - If it's a runtime error, reproduce the conditions.
   - If you can't reproduce it, ask the user for steps.
3. A fix without reproduction is a guess. Don't guess.

## Phase 2: Isolate

1. Search for the error: Grep for error messages, stack traces, relevant symbols.
2. Read 2-4 files maximum to understand the root cause. Don't read the whole codebase.
3. Identify the root cause, not the symptom.
4. Form a hypothesis: "The bug is in `file:line` because [reason]. The fix is [change]."

## Phase 3: Fix (minimal, root cause)

1. Make the minimal change that addresses the root cause.
2. Don't fix symptoms. Don't refactor unrelated code.
3. If the fix requires touching 4+ files, it's not a bugfix. Suggest `/spec` for a proper change.

## Phase 4: Verify

1. Run the reproduction again. The bug must be gone.
2. Run the relevant test. It must pass.
3. Run typecheck + lint on the changed files.
4. Run the broader test suite if the fix might affect other areas.

If verification fails:
- Re-examine the root cause. Don't patch the fix.
- If the fix is wrong, revert and re-isolate.

## Phase 5: Commit (if part of a feature)

If this fix is part of an active feature:
1. Stage the specific files.
2. Commit: `fix: [description of what was wrong and why]`.
3. Update progress.md.

If standalone, suggest `/ship` or just report the fix.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I know where the bug is, no need to reproduce" | Reproduce first. "Knowing" without proof is guessing. |
| "I'll fix the symptom for now" | Symptom fixes create future bugs. Fix the root cause. |
| "The fix might break other things, I'll check later" | Check now. Run the test suite. |
| "I'll refactor this while I'm here" | No. Out of scope. File a follow-up. |
| "Reading 4 files isn't enough" | Then the bug is complex. Use /spec, not /fix. |

## Red Flags

- Fixing without reproducing the bug first.
- Fixing symptoms instead of root cause.
- Touching 4+ files (that's a feature, not a bugfix).
- Refactoring unrelated code "while I'm here".
- Not running the test suite after the fix.
- Commiting without verifying the fix works.

## Related Commands

- `/verify` - Run gates after the fix.
- `/review` - Review the fix if it's non-trivial.
- `/spec` - If the "bug" requires 4+ files, it's a feature. Spec it.

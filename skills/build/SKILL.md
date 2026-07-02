---
name: build
description: Implement features with TDD discipline. Reads spec/plan and executes tasks wave-by-wave with RED-GREEN-REFACTOR cycle. Supports auto mode (plan + implement in one pass) and --skip-plan for simple features.
user-invocable: true
disable-model-invocation: true
---

# /build - Implement with TDD

Execute implementation tasks with test-driven development and per-task verification.

## Modes

- **`/build`**: Read existing plan.md and execute its tasks.
- **`/build auto`**: Plan + implement all tasks in one pass. Derive tasks from spec, implement, verify, repeat. Pause on failures.
- **`/build --skip-plan`**: For simple features. Convert spec directly into a short task list and implement.
- **`/build task T3`**: Execute a specific task by ID from the plan.

## Phase 1: Load context

1. Read `.factory/artifacts/.active` -> get slug.
2. Read `.factory/artifacts/<slug>/spec.md`.
3. If mode is not `auto` or `--skip-plan`: read `.factory/artifacts/<slug>/plan.md`.
4. Read `AGENTS.md` for build/test/lint commands.
5. Create or read `.factory/artifacts/<slug>/progress.md` (use `templates/progress.md`).

## Phase 2: Derive tasks (auto / --skip-plan only)

If no plan exists:
1. Extract tasks from the spec's task list.
2. For `auto` mode: build a quick dependency graph (mentally, no plan.md file).
3. For `--skip-plan`: create a TodoWrite list with the tasks.
4. Proceed to implementation.

## Phase 3: Wave-based execution

For each wave (or task if sequential):

1. **Check independence**: Can tasks in this wave run in parallel?
   - Yes, independent files -> use Task tool with `general` droid for each.
   - No, shared files -> run sequentially.
2. For each task, run the TDD cycle (Phase 4).
3. After all tasks in a wave: run full verification (`/verify` gates).
4. Update progress.md with task status.

## Phase 4: TDD cycle (per task)

### RED - Write a failing test
1. Write a test that captures the task's requirement.
2. Run it. It must fail for the right reason (not a syntax error).
3. If it fails for the wrong reason, fix the test.

### GREEN - Minimal implementation
1. Write the minimum code to make the test pass.
2. Run the test. It must pass.
3. Don't add anything not required by the test.

### REFACTOR - Clean up
1. Improve the code without changing behavior.
2. Run the test again. It must still pass.

### Commit
1. Stage only the files this task touched. NEVER `git add .`.
2. Commit with prefix: `feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `chore:`.
3. Record the commit hash in progress.md.

## Phase 5: Per-task verification

After each task, run:
- Typecheck (if applicable)
- Lint (if applicable)
- The task's specific verification command from the plan

If any gate fails:
1. Fix the issue immediately.
2. Re-run gates.
3. If verification fails 2x on the same task -> STOP. Report the blocker to the user.

## Stop conditions

- Verification fails 2x on the same task -> stop, report blocker.
- A change requires touching files outside the declared scope -> stop, ask user.
- A test reveals the plan is wrong -> stop, re-plan (suggest `/plan`).

## Phase 6: Update progress

After each task, update `.factory/artifacts/<slug>/progress.md`:
- Mark task status: `[x]` done, `[ ]` pending, `[!]` blocked.
- Mark verify status: PASS / FAIL / N/A.
- Record commit hash.
- Note any deviations or blockers.

## Phase 7: Wave complete check

After each wave:
- All tasks in the wave must be `[x]`.
- Full verification must pass (typecheck + lint + test + build).
- No blockers.

If any fail, resolve before moving to the next wave.

## Phase 8: Done

When all waves complete:
1. Run final full verification.
2. Update progress.md with completion status.
3. Suggest next: `/verify` (formal gate run) -> `/review` (multi-persona) -> `/ship`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The test is obvious, I'll skip RED" | RED proves the test checks the right thing. Skipping it means your test might pass for the wrong reason. |
| "I'll write tests after the code" | That's not TDD. Tests written after tend to test the implementation, not the requirement. |
| "This is too simple for TDD" | Simple things break too. The test takes 30 seconds. |
| "I'll verify at the end" | Per-task verification isolates failures. End-only verification hides which task broke things. |
| "I'll use git add . to save time" | Never. Stage specific files. `git add .` commits artifacts, logs, and stray files. |
| "The refactor is safe, I'll skip re-running tests" | Re-run. Always. Refactors break things silently. |

## Red Flags

- Committing without running the task's verification command.
- Using `git add .` or `git add -A`.
- Skipping the RED phase ("I know it'll fail").
- Touching files outside the task's declared scope.
- Moving to the next task before the current one passes all gates.
- Implementing multiple tasks before verifying any.

## Related Commands

- `/spec` - Create the spec this build implements.
- `/plan` - Create the plan this build executes.
- `/verify` - Run formal verification gates after build.
- `/review` - Multi-persona review of the built code.

## References

- `references/testing-patterns.md` - Test structure (AAA), naming, mock anti-patterns, test types. Load when writing tests in the RED phase.

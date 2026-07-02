---
name: build
description: Implement features with TDD discipline. Reads spec/plan and executes tasks wave-by-wave with RED-GREEN-REFACTOR cycle. Supports auto mode (plan + implement in one pass) and --skip-plan for simple features.
user-invocable: true
disable-model-invocation: true
---

# /build - Implement with TDD

Execute implementation tasks with test-driven development and per-task verification. TDD here is the red -> green loop; refactor belongs to `/review`, not the implementation cycle.

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
5. Read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.
6. Create or read `.factory/artifacts/<slug>/progress.md` (use `templates/progress.md`).

## Phase 1b: Agree the seams

Tests live at **seams** — the public boundaries where you observe behaviour without reaching inside. Before writing any test, write down the seams under test and confirm them with the user (AskUser if needed). No test is written at an unconfirmed seam.

Ask: "What's the public interface, and which seams should we test?" Prefer existing seams to new ones. Use the highest seam possible — the fewer seams across the codebase, the better (the ideal is one). If new seams are needed, propose them at the highest point you can.

This is the `codebase-design` vocabulary: a seam is where a module's interface lives. Agree them up front so testing effort lands on critical paths and complex logic, not every edge case.

## Phase 2: Derive tasks (auto / --skip-plan only)

If no plan exists:
1. Extract tasks from the spec's task list.
2. For `auto` mode: build a quick dependency graph (mentally, no plan.md file).
3. For `--skip-plan`: create a TodoWrite list with the tasks.
4. Proceed to implementation.

## Delegation

Use the Task tool to delegate focused subtasks to specialized droids:
- `explore` for read-only code search and discovery (find patterns, map structure).
- `review` for code review of completed work before proceeding.
- `scout` for external research (docs, API references, prior art).
- `general` for simple parallel tasks that don't need the full TDD cycle.

Do NOT delegate the core implementation. You own the edits. Use `general` droids only for independent tasks within a wave that can run in parallel (no shared files).

## Phase 3: Wave-based execution

For each wave (or task if sequential):

1. **Check independence**: Can tasks in this wave run in parallel?
   - Yes, independent files -> use Task tool with `general` droid for each.
   - No, shared files -> run sequentially.
2. For each task, run the TDD cycle (Phase 4).
3. After all tasks in a wave: run full verification (`/verify` gates).
4. Update progress.md with task status.

## Phase 4: TDD cycle (per task)

Tests verify behaviour through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

### RED - Write a failing test
1. Write a test at an **agreed seam** (Phase 1b) that captures the task's requirement.
2. Run it. It must fail for the right reason (not a syntax error).
3. If it fails for the wrong reason, fix the test.

**One slice at a time.** One seam, one test, one minimal implementation per cycle. Each test is a **tracer bullet** that responds to what the last cycle taught you. Don't write all tests first then all implementation (**horizontal slicing**) — that tests *imagined* behaviour and commits to test structure before understanding the implementation.

Watch for test **anti-patterns** (load `references/testing-patterns.md` for detail):
- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel. The tell: the test breaks when you refactor but behaviour hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`), so it passes by construction and can never disagree. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — all tests first, then all implementation (see above).

### GREEN - Minimal implementation
1. Write the minimum code to make the test pass.
2. Run the test. It must pass.
3. Don't add anything not required by the test. No speculative features, no abstraction for hypothetical needs.

### REFACTOR - Clean up
1. Improve the code without changing behavior.
2. Run the test again. It must still pass.

**Refactor is not part of the core loop's value.** It belongs to the `/review` stage. Keep refactor minimal here — a quick naming or extraction in the same cycle is fine; architectural refactoring is a `/review` or `/improve-codebase-architecture` concern, not a build-step concern.

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
| "I'll write all tests first, then implement" | That's horizontal slicing — tests imagined behaviour before you understand the implementation. One slice at a time. |
| "I'll mock the internal collaborator" | That's implementation-coupled. Test through the agreed seam, not internals. |
| "expect(add(a,b)).toBe(a+b)" | That's tautological — it can never fail. Expected values come from an independent source of truth. |
| "I'll add this abstraction for future needs" | Speculative generality. Don't. Inline back until a real need shows. |
| "I'll agree seams as I go" | Agree them up front (Phase 1b). Unconfirmed seams scatter testing effort. |
| "I'll verify at the end" | Per-task verification isolates failures. End-only verification hides which task broke things. |
| "I'll use git add . to save time" | Never. Stage specific files. `git add .` commits artifacts, logs, and stray files. |
| "The refactor is safe, I'll skip re-running tests" | Re-run. Always. Refactors break things silently. |

## Red Flags

- Writing tests at unagreed seams (no Phase 1b confirmation).
- Committing without running the task's verification command.
- Using `git add .` or `git add -A`.
- Skipping the RED phase ("I know it'll fail").
- Tautological assertions (expected value computed the same way the code computes it).
- Implementation-coupled tests (mocking internals, testing private methods).
- Horizontal slicing (all tests first, then all implementation).
- Touching files outside the task's declared scope.
- Moving to the next task before the current one passes all gates.
- Implementing multiple tasks before verifying any.
- Architectural refactoring inside a build cycle (belongs to /review or /improve-codebase-architecture).

## Related Commands

- `/spec` - Create the spec this build implements.
- `/plan` - Create the plan this build executes.
- `/verify` - Run formal verification gates after build.
- `/review` - Multi-persona review of the built code.

## References

- `references/testing-patterns.md` - Test structure (AAA), naming, mock anti-patterns, test types. Load when writing tests in the RED phase.

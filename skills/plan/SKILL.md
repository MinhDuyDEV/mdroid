---
name: plan
description: Break down a spec into an implementation plan with dependency graph and wave-ordered TDD tasks. Use after /spec for complex features (4+ files, multiple systems).
user-invocable: true
disable-model-invocation: true
---

# /plan - Break Down Implementation

Convert a spec into a dependency-ordered, TDD-aware implementation plan.

## Model recommendation

Architecture planning benefits from high-reasoning models. If mixed models are configured:
- **Planning model** (specModeModel): Use a strong model with high reasoning effort (e.g., Opus with `high`).
- **Implementation model**: Switch to a faster model (e.g., Sonnet, Codex) for `/build`.

Configure in `/settings` or `.factory/settings.json`:
```json
{
  "sessionDefaultSettings": {
    "specModeModel": "<strong model>",
    "specModeReasoningEffort": "high"
  }
}
```

## Phase 1: Load context

1. Read `.factory/artifacts/.active` -> get slug.
2. Read `.factory/artifacts/<slug>/spec.md`.
3. Read `AGENTS.md` for conventions and commands.
4. Grep `.factory/memories.md` for relevant past decisions.
5. Run `git log --oneline -20` for recent change context.

## Phase 2: Explore codebase

Use the Task tool with `explore` droid (or Grep/Glob directly for small projects) to:
- Find the files the spec says will be affected.
- Find related existing patterns and conventions.
- Identify reusable utilities or components.
- Map the current structure of affected modules.

## Phase 3: Goal-backward task derivation

Start from the spec's success criteria and work backward:

1. What's the last thing that must be true? -> That's the last task.
2. What must be true before that? -> Prior tasks.
3. Repeat until you reach the first task (the one with no prerequisites).

For each task, specify:
- **ID**: T1, T2, ...
- **Description**: one sentence.
- **Files**: exact file paths to create or modify.
- **Depends on**: task IDs (or "none").
- **Verify**: the command that proves this task is done.
- **TDD order** (where applicable): write failing test -> implement -> refactor.

## Phase 4: Dependency graph

List all tasks and their dependencies. Verify:
- No circular dependencies.
- Every dependency is an earlier task.
- Tasks with no dependencies form Wave 1.

## Phase 5: Wave assignment

- **Wave 1**: tasks with no dependencies.
- **Wave 2**: tasks depending only on Wave 1 tasks.
- **Wave N**: tasks depending only on earlier waves.

Tasks in the same wave can run in parallel (via Task tool with `general` droid) if they touch independent files.

## Phase 6: Write plan.md

Use `templates/plan.md` and write to `.factory/artifacts/<slug>/plan.md`.

Include:
- Must-Haves: Observable Truths, Required Artifacts, Key Links
- Dependency Graph (textual)
- Tasks grouped by wave with IDs, files, dependencies, verification

## Phase 7: Constitutional compliance gate

Before finalizing, verify the plan passes:
- [ ] Every task has a verification command.
- [ ] No task exceeds ~5 minutes of work (split if larger).
- [ ] Dependencies are acyclic.
- [ ] The plan delivers all of the spec's success criteria.
- [ ] No task touches more than 5 files (split if larger).

If any check fails, revise the plan.

## Phase 8: Confirm

Show the user the plan summary (task count, wave count, estimated scope). Ask:
- Does the order make sense?
- Any missing tasks?

## Next

- `/build` - Execute this plan.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "Tasks are obvious, skip the dependency graph" | Hidden dependencies cause merge conflicts and rework. |
| "I'll define verification during implementation" | No verification = no task. Define it now. |
| "This task is big but I'll handle it in one go" | Split it. Big tasks hide failures. |
| "Waves aren't needed, I'll go sequentially" | Waves enable parallelism. Cheap to assign. |

## Red Flags

- Tasks without verification commands.
- Circular dependencies.
- Tasks touching 6+ files.
- Plan doesn't reference the spec's success criteria.
- No dependency graph (just a flat list).

## Related Commands

- `/spec` - Create the spec this plan implements.
- `/build` - Execute this plan with TDD.

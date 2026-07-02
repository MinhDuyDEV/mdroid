# Orchestration Patterns

> Multi-persona orchestration patterns for parallel review and analysis.

## When to orchestrate

Orchestration means fanning out multiple agents (via Task tool) to work in parallel on independent subtasks. Use it when:
- A task has independent subtasks that can run in parallel.
- You need multiple perspectives on the same artifact (e.g., code review).
- The subtasks don't depend on each other's output.

## Pattern 1: Parallel review personas

Used by `/review`. Spawn N reviewers, each focused on one dimension.

```
                    +---> [correctness reviewer] ---> findings
[review coordinator] +---> [security reviewer]    ---> findings
                    +---> [performance reviewer]  ---> findings
                    +---> [test reviewer]         ---> findings
                                        |
                                        v
                              [synthesize findings]
```

Rules:
- Each reviewer gets the same diff but a focused prompt.
- Reviewers run in parallel (spawn all Task calls in one message).
- Collect all findings, merge, deduplicate, rank by severity.
- Coordinator doesn't review; it orchestrates and synthesizes.

## Pattern 2: Fan-out research

Used by `/research` (complex mode). Spawn scouts for sub-questions.

```
                    +---> [scout: sub-question 1] ---> findings
[research lead]     +---> [scout: sub-question 2] ---> findings
                    +---> [scout: sub-question 3] ---> findings
                                        |
                                        v
                              [cross-check + synthesize]
```

Rules:
- Break the question into independent sub-questions.
- Each scout gets a focused research prompt.
- Cross-check findings: do they agree? Resolve conflicts.
- Synthesize with confidence levels.

## Pattern 3: Pipeline (sequential)

For tasks where each step depends on the previous.

```
[discover] ---> [review each] ---> [synthesize]
```

Rules:
- Each step's output is the next step's input.
- Use when subtasks are dependent.
- Don't parallelize dependent tasks.

## Pattern 4: Map-reduce

For tasks that process many independent items.

```
                    +---> [worker: item 1]  ---> result
[coordinator]       +---> [worker: item 2]  ---> result
                    +---> [worker: item N]  ---> result
                                        |
                                        v
                              [reduce/aggregate]
```

Rules:
- Each worker processes one item independently.
- Reduce step aggregates results.
- Use when items are numerous and independent.

## Anti-pattern: personas-dont-invoke-personas

**Never let a spawned persona spawn its own personas.** This causes:
- Exponential fan-out (N^2 or worse).
- Loss of coordination (no single coordinator sees the full picture).
- Infinite loops (persona A spawns B, B spawns A).

If a persona needs more analysis, it returns its findings to the coordinator. The coordinator decides whether to spawn more work.

## Anti-pattern: Over-orchestration

Don't orchestrate when:
- The task is simple (1-2 tool calls). Just do it.
- The subtasks are dependent. Run sequentially.
- The overhead of spawning exceeds the work. Spawn only when the subtask is substantial.

## Task tool prompt template

When spawning a subagent via Task tool:

```
Goal: [what to accomplish]
Context: [specific files, line ranges, or info needed]
Constraints: [what to avoid, what to preserve]
Expected output: [format and content of the return]
```

Bad: "Review this code." (vague)
Good: "Review src/auth/login.ts:30-80 for input validation. Check: null handling, length validation, injection risks. Report findings with line citations."

## Verification

- [ ] Subtasks are truly independent (no hidden dependencies).
- [ ] Each subagent prompt is specific (goal, context, constraints, output format).
- [ ] No persona spawns its own personas (flat hierarchy).
- [ ] Coordinator synthesizes, doesn't just concatenate.
- [ ] Findings are deduplicated and ranked.

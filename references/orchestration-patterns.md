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

## Pattern 5: Convergence Judge (conditional)

A systemic-pattern finder that reads ALL fan-out findings to see the whole elephant. Used by `/review` (Phase 5). Each reviewer sees one part; the Judge sees the whole. Spawned via the `oracle` droid, which runs a **stronger model** than the reviewer sub-agents — convergence requires deeper reasoning than individual finding-by-finding review.

```
                    +---> [Standards: general]    ---> findings
                    +---> [Spec: general]         ---> findings
[review coordinator] +---> [Security: security-audit] ---> findings
                    +---> [Tests: general]        ---> findings
                                        |
                          [trigger gate: findings >= 5, OR cross-axis conflict, OR --deep]
                                        |
                            +-----------+-----------+
                            |   (gate closed)       |   (gate open)
                            v                       v
                    aggregate flat           [Convergence Judge: oracle droid (strong model)] ---> Judge's report
                                                    |
                                                    v
                                        aggregate + Judge's report
```

### Model asymmetry

Reviewer sub-agents use `general` / `security-audit` (typically `model: inherit` — fast, same model as parent). The Convergence Judge uses the `oracle` droid, configured with a **stronger model + high reasoning effort**. This is deliberate:

- Reviewers are the blind men — each feels one part, fast, accepts false positives.
- The oracle sees the whole elephant — it needs deeper reasoning to converge symptoms into root causes.

If `oracle` is unavailable, fall back to `review` droid (convergence quality drops, but the phase still runs).

### Trigger gate

The Judge is **conditional** — it fires only when findings are numerous enough to hide a systemic pattern:

- **Default mode**: fires when findings ≥ 5 OR any cross-axis/cross-persona conflict exists.
- **`--deep` mode**: always fires, regardless of count.
- **`--quick` mode**: never fires.

When the gate does not fire, aggregate flat (Pattern 1). No Judge for a 2-finding diff.

### What the Judge does

1. **Convergence** — groups findings that are symptoms of one root cause.
2. **False-positive dismissal** — flags findings that are not bugs, with evidence.
3. **Missing mechanism** — names the absent guard/layer/seam that would prevent the cluster.
4. **Conflict resolution** — resolves cross-axis disagreements with a reasoned verdict.

### Rules

- The Judge runs **after** all fan-out sub-agents return (sequential, not parallel).
- The Judge reads ALL findings at once — this is its power and the reason it is sequential.
- The Judge does **not merge axes** (Standards and Spec stay separate in the final report).
- The Judge does **not rerank within an axis** (sub-agents own their rankings).
- The Judge does **not spawn sub-agents** (flat hierarchy — see anti-pattern below).
- The Judge does **not fix** — it reports. The coordinator decides fixes.
- The Judge accepts false positives as input: sub-agents bias toward raising, the Judge prunes with evidence.

### Anti-pattern: Judge merging axes

The Judge's convergence must not collapse the Standards and Spec axes into one list. The two axes exist so neither masks the other. The Judge reads both, finds systemic patterns across both, but reports **additively** — its report sits alongside the axis reports, never replaces them.

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

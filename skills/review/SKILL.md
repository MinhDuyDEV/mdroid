---
name: review
description: Two-axis review of the diff since a fixed point — Standards (does the code follow the repo's documented coding standards plus a Fowler smell baseline?) and Spec (does it faithfully implement the originating spec/issue/PRD?), run as parallel sub-agents so neither pollutes the other. Also runs optional vertical personas (correctness, security, performance, tests). Use after /verify passes, or when the user wants to review a branch, PR, or work-in-progress changes.
user-invocable: true
disable-model-invocation: true
---

# /review - Two-Axis + Vertical-Persona Review with Convergence Judge

Review the changes since a fixed point along two axes that must not be merged, plus optional vertical personas. Running Standards and Spec separately stops one axis masking the other. When findings are numerous enough to hide a systemic pattern, a **Convergence Judge** reads all findings to see the whole elephant.

## Core principles

1. **Accept false positives.** Bug discovery biases toward raising — a wrong finding costs one red test to disprove, a missed bug costs a production incident. Raise it; let the Judge and the user prune.
2. **Standards and Spec are never merged.** Each axis reports independently so neither masks the other. The Judge reads both but never collapses them into one list.
3. **Convergence is conditional.** The Judge only fires when there are enough findings to hide a systemic pattern — a single Critical in a 2-file diff doesn't need a Judge to see it.
4. **Verification is cheap, discovery is hard.** Confirming a finding takes one red test. Use this as the rebuttal whenever someone wants to suppress a noisy-but-cheap-to-check finding.

## Modes

- **`/review --quick`**: 1 axis (Standards only, correctness lens). Fast. No Judge.
- **`/review`** (default): 2 axes (Standards + Spec) + 2 vertical personas (security, tests), in parallel. **Conditional Judge**: fires when findings ≥ 5 or any cross-axis/cross-persona conflict exists.
- **`/review --deep`**: 2 axes + 4 vertical personas (correctness, security, performance, tests) + cross-check + **Judge always fires**.

## Phase 1: Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here — not inside parallel sub-agents.

Also load the spec: read `.factory/artifacts/.active` -> slug -> `.factory/artifacts/<slug>/spec.md` (for the Spec axis and success criteria).

## Phase 2: Identify the spec source

Look for the originating spec, in this order:

1. The active feature's `spec.md` under `.factory/artifacts/<slug>/`.
2. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.).
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

## Phase 3: Identify the standards sources

Anything in the repo that documents how code should be written: `AGENTS.md`, `.factory/rules/*.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** — a fixed set of Fowler code smells in `references/code-smells.md` that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

## Phase 4: Spawn sub-agents in parallel

Send a single message with multiple Task tool calls. Use the `general` droid for each, except security which prefers the `security-audit` droid when available.

### Standards sub-agent

Include:
- The full diff command and commit list.
- The list of standards-source files you found in Phase 3, **plus the smell baseline from `references/code-smells.md`** pasted in full — the sub-agent has no other access to it.
- The brief: "Report — per file/hunk where relevant — (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline smell you spot: name it and quote the hunk. Distinguish hard violations from judgement calls — documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

### Spec sub-agent

Include:
- The diff command and commit list.
- The path or contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### Vertical personas (--deep only, or selectively in default)

Spawn only the personas the mode calls for. Each gets the diff + a focused brief:

- **Security** (prefer `security-audit` droid): input validation, secrets, injection, auth. Cite file:line. Severity: Critical/Important/Minor.
- **Tests**: do tests assert behaviour not "doesn't throw"? Edge cases? Stubs? Coverage? Cite file:line.
- **Correctness** (--deep): edge cases, off-by-one, race conditions, stubs/TODOs. Cite file:line.
- **Performance** (--deep): N+1, unbounded loops, unnecessary allocations, missing indexes. Cite file:line.

For `--deep`, after all reviewers return, run a cross-check: do findings conflict (e.g. security says "add validation" but performance says "avoid extra checks")? Are there findings spanning multiple dimensions?

## Phase 5: Convergence Judge (conditional)

The Convergence Judge is a **systemic-pattern finder**, not a reranker. Its job is to see the whole elephant when sub-agents have each reported on a single part. It fires conditionally; the mode only decides whether the condition is pre-armed.

### Trigger gate

Count all findings returned by Phase 4 (all axes + personas, combined). The Judge fires when **any** of:

1. **Findings ≥ 5** (default mode) — enough signal that a systemic pattern could hide among them.
2. **Cross-axis conflict** — a Standards finding and a Spec finding disagree (e.g. Standards says "extract a helper", Spec says "the helper breaks the contract").
3. **`--deep` mode** — always fires, regardless of count. Deep reviews are for large features where systemic patterns are most likely.

When the gate does not fire (default mode, < 5 findings, no conflict), skip straight to Phase 6. Do not spawn a Judge for a 2-finding diff — there is no elephant to see.

### Spawn the Judge

Spawn **one** Task call using the `oracle` droid. The Judge runs **after** all Phase 4 sub-agents return — it is sequential by necessity, since it reads their findings.

The `oracle` droid runs a **stronger model** than the reviewer sub-agents (which use `general` / `security-audit` with `model: inherit`). This is deliberate: convergence requires deeper reasoning than individual finding-by-finding review. The reviewers are the blind men; the oracle sees the whole elephant. If the `oracle` droid is not available (e.g. user removed it), fall back to the `review` droid — convergence quality drops, but the phase still runs.

Give the Judge:

- **All findings from every axis and persona**, pasted in full. The Judge has no other access to them.
- **The diff command and commit list** (so it can re-read the code if needed to validate a convergence hypothesis).
- **The spec source** (so systemic patterns can be checked against intent, not just against code).

### The Judge's brief

The Judge is the courtroom judge — not a prosecutor, not a defender. It adjudicates:

1. **Convergence**: Group findings that are **symptoms of one root cause**. Name the root cause and list the findings it explains.
   - Example: 3-4 sub-agents each flag a different symptom on the same module (off-by-one, missing null check, unhandled error). The Judge recognises the module lacks a **defensive boundary**, not four separate bugs.
2. **False-positive dismissal**: Flag findings the sub-agents raised that are **not actually bugs** — but only when the Judge can cite why (the sub-agent misread the spec, the code handles the case elsewhere, tooling already enforces it). Never dismiss without evidence.
3. **Missing mechanism**: When findings cluster around an **absent** guard (no validation layer, no error propagation, no seam for testing), name the missing mechanism. This is the Judge's highest-value output: "the bugs you see are because the brake is missing, not because the parachute is too heavy."
4. **Conflict resolution**: When two axes or personas disagree (Security wants more validation, Performance wants fewer checks), the Judge resolves it with a **reasoned verdict**, not a coin flip.

### Output format

The Judge returns a **Judge's Report** (under 500 words):

```
## Convergence Judge

### Root-cause clusters
- [root cause name]: findings [A1, B2, C3] — [explanation]
- [root cause name]: findings [D1, D2] — [explanation]

### False positives dismissed
- Finding [id]: [why it is not a bug, with evidence]

### Missing mechanism
- [name]: [what guard/layer/seam is absent, and which findings it would prevent]

### Conflict resolutions
- [finding A] vs [finding B]: [verdict + reasoning]

### Systemic risk
- [one sentence: the single highest-risk pattern across the entire diff]
```

### What the Judge does NOT do

- It does **not merge the Standards and Spec axes**. They stay separate in the final report.
- It does **not rerank findings within an axis**. Sub-agents own their rankings.
- It does **not spawn its own sub-agents**. Flat hierarchy (see `references/orchestration-patterns.md` anti-pattern: personas-dont-invoke-personas).
- It does **not fix anything**. It reports. The main agent fixes (Phase 7).

## Phase 6: Aggregate

Present the reports under `## Standards`, `## Spec`, and (if run) `## Security`, `## Tests`, etc. headings, verbatim or lightly cleaned. Do **not** merge or rerank findings across the Standards and Spec axes — they are deliberately separate.

If the Convergence Judge fired (Phase 5), append its report under a `## Convergence Judge` heading after all axis/persona reports. The Judge's report is **additive** — it sits alongside the axis reports, never replaces them.

End with a one-line summary: total findings per axis/persona, the worst issue *within each* (if any), and — if the Judge fired — the systemic risk it identified. Don't pick a single winner across axes — that's the reranking the separation exists to prevent.

## Phase 7: Write review.md

Write to `.factory/artifacts/<slug>/review.md`:

```markdown
# Review: [feature name]
## Date: [timestamp]
## Fixed point: [ref]

## Standards
[Standards sub-agent report]

## Spec
[Spec sub-agent report, or "no spec available"]

## Security (if run)
[report]

## Tests (if run)
[report]

## Convergence Judge (if fired)
[Judge's report, or omit if the trigger gate did not fire]

## Summary
[per-axis counts + worst issue per axis, + systemic risk if Judge fired]
```

## Phase 8: Auto-fix rule

- **Critical** -> fix inline now, then re-run `/verify`. Don't ship with critical issues.
- **Important** -> fix inline now if quick, otherwise log to review.md for follow-up.
- **Minor** -> log to review.md. Don't fix now (avoid scope creep).
- **Missing mechanism (Judge)** -> if the Judge identified a missing guard/layer/seam, decide with the user: fix inline if small, or hand off to `/spec` if it requires architectural change. Do not silently ignore it.

For critical fixes: make the minimal change, stage specific files, re-run the affected test.

## Phase 9: Report

Show the user the review summary. If critical issues were found and fixed, note the fix and re-verification. If the Judge fired, surface the systemic risk and any missing mechanism prominently — this is the finding most likely to be lost in a flat findings list.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing -> **Standards pass, Spec fail.**
- Code that does exactly what the spec asked but breaks the project's conventions -> **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

## Next

- No critical issues -> `/ship`.
- Critical issues remain -> `/fix` to resolve, then `/verify`, then re-`/review`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I reviewed it myself, no need for sub-agents" | Single-pass review misses dimension-specific issues. That's why we fan out. |
| "The Spec axis isn't needed, there's no spec" | Then it reports "no spec available". Don't skip the axis — record the gap. |
| "Smells are just opinions" | They're labelled heuristics, always judgement calls — but a documented repo standard overrides them, and they catch real shallowness. |
| "The security persona isn't needed, this isn't a security feature" | Everything is a security feature. Run it. |
| "I'll fix critical issues after shipping" | Never. Critical = block ship. Fix first. |
| "Merge the Standards and Spec findings into one list" | No. The separation exists so neither masks the other. Keep them separate. |
| "That finding is probably a false positive, I'll drop it" | Accept false positives. Raising a wrong finding costs one red test to disprove. Missing a real bug costs a production incident. Raise it; let the Judge or the user prune. |
| "The Judge isn't needed, I can see the pattern myself" | The Judge reads ALL findings at once — you wrote the code, you have confirmation bias. Let the Judge converge. |
| "The Judge fired but found no systemic pattern" | That is a valid outcome. Record "no convergence" in the Judge's report. Don't force a pattern that isn't there. |
| "I'll skip the Judge, there are only 4 findings" | Check the trigger gate. < 5 findings and no conflict means the gate does not fire — that is correct. But if there IS a cross-axis conflict, the Judge fires regardless of count. |
| "I'll skip the Judge, it costs an extra round-trip" | The Judge is conditional precisely to control cost. When it fires, the systemic pattern it finds is worth more than the round-trip. When it doesn't fire, it costs nothing. |

## Red Flags

- Reviewers returning "looks good" without listing what they checked.
- Findings without file:line citations.
- Skipping a persona or axis "because it's not relevant".
- Merging Standards and Spec findings into one ranked list.
- Not pasting the smell baseline into the Standards sub-agent prompt (it has no other access).
- Shipping with unresolved critical issues.
- Not recording findings in review.md.
- The Judge merging axes into one ranked list (it must keep them separate).
- The Judge spawning its own sub-agents (flat hierarchy).
- The Judge dismissing a finding without citing why (dismissals need evidence too).
- Suppressing a noisy finding to "save the user time" — accept false positives, let red tests prune.
- Firing the Judge on a 2-finding diff (the trigger gate exists for a reason).

## References

Personas should load these checklists during review:
- `references/code-smells.md` - Standards axis: the 12 Fowler smells baseline.
- `references/security-checklist.md` - Security persona.
- `references/performance-checklist.md` - Performance persona (--deep).
- `references/testing-patterns.md` - Tests persona.

## Related Commands

- `/verify` - Run verification gates before review.
- `/fix` - Fix critical issues found by review.

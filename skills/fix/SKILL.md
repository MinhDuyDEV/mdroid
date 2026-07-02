---
name: fix
description: Disciplined diagnosis loop for hard bugs and performance regressions — build a tight red feedback loop before hypothesising, then fix with a regression test. Use for bugfixes (2-3 files) or to resolve issues found by /verify or /review.
user-invocable: true
disable-model-invocation: true
---

# /fix - Diagnose and Fix Bugs

A discipline for hard bugs. Skip phases only when explicitly justified. For trivial one-line fixes, the loop still applies but compresses fast.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug — one that goes red on *this* bug — you will find the cause. If you don't, no amount of staring at code will save you. Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

A fix without reproduction is a guess. Don't guess — but "reproduction" here means a *tight red loop*, not just "I saw the error once."

### Ways to construct one — try in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive *them* with a structured bash loop so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have *a* loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight — a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100x, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion — a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to *catch this specific bug*.
- [ ] **Deterministic** — same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via a structured bash script.

If you catch yourself reading code to build a theory before this command exists, **stop — jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2 — Reproduce + minimise

Run the loop. Watch it go red — the bug appears. Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure. A minimal repro shrinks the hypothesis space in Phase 3 and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green. Do not proceed until you have reproduced **and** minimised.

## Phase 3 — Hypothesise

Generate **3-5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <Y> will make the bug disappear / <Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for Phase 6.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the minimal, root-cause fix. Don't fix symptoms. Don't refactor unrelated code.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

If the fix requires touching 4+ files, it's not a bugfix — suggest `/spec` for a proper change.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop).
- [ ] Regression test passes (or absence of seam is documented).
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix).
- [ ] Throwaway prototypes/harnesses deleted (or moved to a clearly-marked debug location).
- [ ] Typecheck + lint pass on the changed files.
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns.

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) hand off to the `/improve-codebase-architecture` skill with the specifics. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

## Commit

If this fix is part of an active feature:
1. Stage the specific files (NEVER `git add .`).
2. Commit: `fix: [what was wrong and why]` — include the confirmed hypothesis.
3. Update progress.md.

If standalone, suggest `/ship` or just report the fix.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I know where the bug is, no need for a loop" | A tight red loop is proof. "Knowing" without it is guessing. |
| "I'll hypothesise first, the loop can come later" | Jumping straight to a hypothesis is the exact failure this skill prevents. Loop first. |
| "One hypothesis is enough, it's obvious" | Single-hypothesis generation anchors. Generate 3-5 ranked, falsifiable. |
| "I'll fix the symptom for now" | Symptom fixes create future bugs. Fix the root cause. |
| "The fix might break other things, I'll check later" | Check now. Re-run the loop. Run the broader suite. |
| "I'll refactor this while I'm here" | No. Out of scope. The post-mortem decides follow-ups. |
| "Reading 4 files isn't enough" | Then the bug is complex. Use /spec, not /fix. |
| "I'll log everything and grep" | Never. Targeted logs at hypothesis boundaries, tagged with a prefix. |

## Red Flags

- Hypothesising before a tight red loop exists.
- A loop that can't go red on the user's exact symptom (catches the wrong bug).
- Single-hypothesis debugging (first plausible idea, no alternatives).
- Non-falsifiable hypotheses ("maybe it's a race" with no prediction).
- Fixing symptoms instead of root cause.
- Touching 4+ files (that's a feature, not a bugfix — spec it).
- Refactoring unrelated code "while I'm here".
- Not removing `[DEBUG-...]` instrumentation.
- No regression test, and no documented "no correct seam" finding.
- Commiting without verifying the fix works.

## Related Commands

- `/verify` - Run gates after the fix.
- `/review` - Review the fix if it's non-trivial.
- `/improve-codebase-architecture` - When the post-mortem reveals an architectural cause.
- `/spec` - If the "bug" requires 4+ files, it's a feature.

---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities — shallow modules that should be deep — then grill through whichever one you pick. Use periodically to keep the codebase good for agents to operate in, or when a post-mortem reveals the real finding is that no good seam exists to lock a bug down.
user-invocable: true
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This command is *informed* by the project's domain model and built on a shared design vocabulary:

- Run the `codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary."
- The domain language in `CONTEXT.md` gives names to good seams; ADRs in `docs/adr/` record decisions this command should not re-litigate.

## Process

### 1. Explore

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area you're touching first.

Then use the Task tool with `subagent_type: "explore"` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates

Write the candidates as a markdown report to `.factory/artifacts/architecture-review/` (or to `.factory/artifacts/<active-slug>/architecture-review.md` if a feature is active). For each candidate, render a section with:

- **Files** — which files/modules are involved.
- **Problem** — why the current architecture is causing friction.
- **Solution** — plain English description of what would change.
- **Benefits** — explained in terms of locality and leverage, and how tests would improve.
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`.

Use `CONTEXT.md` vocabulary for the domain, and the `codebase-design` vocabulary for the architecture. If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the section (e.g. a warning: "_contradicts ADR-0007 — but worth reopening because..._"). Don't list every theoretical refactor an ADR forbids.

Do NOT propose interfaces yet. After the report is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, run the `grill-me` skill to walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize — run the `domain-modeling` skill to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `CONTEXT.md`?** Add the term to `CONTEXT.md`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update `CONTEXT.md` right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: "_Want me to record this as an ADR so future architecture reviews don't re-suggest it?_" Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.

## When this command hands off

- **After a bug fix post-mortem** (`/fix` Phase 6) reveals there's no good seam to lock the bug down: this is the survey that finds the architectural cause. The `fix` skill recommends running this when the finding is architectural, not a one-line bug.
- **Periodic maintenance**: run whenever you have a spare moment. Picking one candidate generates an idea you can take into the main flow at `/spec`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It's just a small smell, not worth a survey" | Small smells compound. The survey finds the ones worth doing now. |
| "I'll just fix the shallow module inline" | Deepening needs grilling — constraints, seam placement, surviving tests. Inline fixes don't get that. |
| "The ADR forbids it, so skip" | Only skip if the friction isn't real. If it is, surface it as a conflict worth reopening. |
| "No CONTEXT.md, so I'll use code names" | Create CONTEXT.md lazily and name modules in domain terms. Code names drift. |

## Red Flags

- Proposing interfaces in the report before the user picks a candidate.
- Using "component," "service," "API," or "boundary" instead of the codebase-design vocabulary.
- Re-litigating every ADR-forbidden refactor, not just the friction-real ones.
- Not reading CONTEXT.md / ADRs before exploring.
- A candidate with no before/after depth argument (no leverage or locality gained).

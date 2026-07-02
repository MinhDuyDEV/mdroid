---
name: spec
description: Define what to build. Creates a PRD (spec.md) in .factory/artifacts/<slug>/. Use before /plan and /build to scope features properly. Rejects trivial tasks that don't need a spec.
user-invocable: true
disable-model-invocation: true
---

# /spec - Define What to Build

Convert a feature request into a clear, verifiable specification.

## Triage Gate

Before starting, assess the request:

| Request type | Action |
|---|---|
| Trivial (1 file, known fix) | Reject: "This is trivial. Do it directly without /spec." |
| Bugfix (2-3 files) | Suggest: "This looks like a bugfix. Use /fix instead." |
| Needs research | Suggest: "Run /research first, then /spec with the findings." |
| Feature (3+ files, clear goal) | Proceed. |

If rejecting, stop and tell the user. Don't create artifacts for trivial work.

## Phase 1: Slug and scaffold

1. Derive a slug from the request: lowercase, hyphenated, max 40 chars.
2. Write the slug to `.factory/artifacts/.active`.
3. Create `.factory/artifacts/<slug>/` directory.

## Phase 2: Context gathering

1. Read `AGENTS.md` for project conventions.
2. Grep `.factory/memories.md` for relevant past decisions.
3. Use the Task tool with `explore` droid to find related code.
4. For external unknowns, use the Task tool with `scout` droid (or WebSearch directly if simple).

## Phase 3: Requirements interview

Assess clarity of the request:

- **Clear request** (well-defined outcome, known scope): skip interview, draft directly.
- **Moderate unknowns** (some constraints unclear): use AskUser with a single batch of questions:
  - What's the user-visible outcome?
  - Any constraints (performance, compatibility, scope limits)?
  - What's explicitly out of scope?
  - What defines "done" for this feature?
- **Many unknowns** (vague requirements, multiple facets): use `/interview-me` for one-question-at-a-time structured extraction. The answer to Q1 may change Q2, so batch questions risk wasting cycles.

## Phase 4: Auto-detect complexity

- **Lite**: 1-3 files, no new dependencies, clear solution -> use `templates/spec-lite.md`.
- **Full**: 4+ files, new patterns, multiple systems -> use `templates/spec-full.md`.

## Phase 5: Write spec.md

Fill the chosen template and write to `.factory/artifacts/<slug>/spec.md`.

For Full specs, include:
- Problem statement
- Solution overview
- Affected files (best estimate)
- Tasks with verification commands
- Success criteria (observable, testable)
- Out of scope
- Anti-rationalization section
- Red Flags section

## Phase 6: Review the spec

Read the spec back. Check:
- Is every success criterion observable and testable?
- Is the scope bounded?
- Are out-of-scope items explicit?
- Can a developer implement this without asking more questions?

If any check fails, revise.

## Phase 7: Confirm with user

Show the user the spec summary (problem, solution, success criteria). Ask:
- Does this capture the intent?
- Any missing constraints?

## Phase 8: Next step

- Complex feature -> suggest `/plan`.
- Simple feature -> suggest `/build --skip-plan`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The spec is clear enough, I'll skip the interview" | Unspoken assumptions become bugs. At minimum use batch AskUser. For many unknowns, use /interview-me. |
| "I'll figure out scope during implementation" | Scope creep is the #1 spec failure. Bound it now. |
| "Success criteria are obvious" | If obvious, writing them is cheap. If not, they're critical. |
| "Out of scope isn't needed for a small feature" | Even small features drift. State what's NOT included. |

## Red Flags

- Success criteria that can't be tested or observed.
- No out-of-scope section.
- Spec covers multiple unrelated features (split it).
- Tasks without verification commands.
- Spec created for a trivial task that should've been done directly.

## Related Commands

- `/plan` - Break this spec into an implementation plan.
- `/build --skip-plan` - Implement directly if the spec is simple enough.
- `/research` - Run first if the spec needs external information.

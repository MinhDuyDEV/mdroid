---
name: development-lifecycle
description: Full SDLC routing. Maps requests to the right command (spec, plan, build, verify, review, ship, fix, research, audit, clean). Always relevant when a user asks to build, fix, implement, or ship a feature - determines which workflow command applies. Also the maintenance router: when a skill is added, renamed, or its behaviour changes, re-read this map and update it so it stays accurate.
user-invocable: false
---

# Development Lifecycle

The router that maps requests to the right mdroid command. You don't remember every command, so this is the map — and a stale router is a router that lies, so it carries its own maintenance rule (see bottom).

A **flow** is a path through the commands. Most paths run along one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea -> ship

The route most work travels. You have an idea and want it built.

1. **`/spec`** — sharpen the idea. Start here when you **have a codebase**: it's stateful, retaining what it learns in `CONTEXT.md` (via `domain-modeling`) and `.factory/artifacts/<slug>/spec.md`. For vague requirements, run `/interview-me` (one question at a time) or `/grill-me` (aggressive interrogation) first, then `/spec`. If research is needed first, run `/research`.
2. **`/plan`** (complex features, 5+ files) — break the spec into tracer-bullet vertical slices with a dependency graph and waves (Wave 0 = prefactoring, then Waves 1..N). Skip for simple features (`/build --skip-plan`).
3. **`/build`** — implement each task with TDD (red -> green -> refactor). `build` drives `codebase-design` vocabulary (seams) internally — agree seams up front, one slice at a time. Each task commits.
4. **`/verify`** — run gates (typecheck, lint, test, build). All must pass.
5. **`/review`** — two-axis review (Standards + Spec) plus optional vertical personas (security, tests, correctness, performance). A conditional **Convergence Judge** reads all findings to find systemic patterns (the whole elephant) when findings are numerous (≥5) or in conflict; `--deep` always fires the Judge. Critical -> fix inline, re-verify.
6. **`/ship`** — commit, PR, cleanup.

### Context hygiene

Keep steps 1-2 in **one unbroken context window** — don't compact or clear until after `/plan` — so the grilling, spec, and plan all build on the same thinking. Each `/build` then starts fresh, working from the plan. The limit is the **smart zone**: the window within which the model reasons sharply. If a session approaches it before `/plan`, don't push on degraded — `/handoff` and continue in a fresh thread.

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and issues piling up** -> **`/fix`**. Disciplined diagnosis: build a tight red feedback loop before hypothesising, then fix with a regression test. Its post-mortem hands off to `/improve-codebase-architecture` when the real finding is that there's no good seam to lock the bug down.
- **External unknowns** -> **`/research`**. Gather with confidence levels, then merge onto the main flow at `/spec`.
- **Audit existing code** -> **`/audit`**. Find pattern occurrences, review each, synthesize remediation, then `/fix` if needed.

## Codebase health

Not feature work — upkeep.

- **`/improve-codebase-architecture`** — run whenever you have a spare moment to keep the codebase good for agents to operate in. Surfaces deepening opportunities; picking one generates an idea you can take into the main flow at `/spec`. It's the survey that finds candidates; `codebase-design` is the bench you design the chosen one on.
- **`/clean`** — remove stale artifact directories after features ship.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills — each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`domain-modeling`** — sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word, record a hard-to-reverse decision as an ADR. It's the active discipline `/spec` and `/improve-codebase-architecture` drive to keep `CONTEXT.md` a clean glossary.
- **`codebase-design`** — the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*. `/build` and `/improve-codebase-architecture` both speak it.

## Standalone

Off the main flow entirely.

- **`/prototype`** — throwaway code that answers one design question (does this state model feel right, or what should this UI look like). The detour when a spec question needs a runnable answer; bridge with `/handoff` if it crosses sessions.
- **`/handoff`** — compact the conversation into a temp file so a fresh session can continue. Forks (new session); the Droid-native `compact` continues (same session). Use `/handoff` when you want a fresh session with the current conversation preserved.
- **`/writing-great-skills`** — reference for writing and editing mdroid skills well.
- **`/interview-me`** / **`/grill-me`** — requirement extraction (interview) and stress-testing (grill). Feed their output into `/spec`.

## Precondition

**`/init`** — run before your first main-flow work to bootstrap `AGENTS.md`, `tech-stack.md`, `.factory/rules/` stubs, and a `CONTEXT.md` glossary stub.

## Triage gate (quick reference)

| Request type | Route | Artifacts? |
|---|---|---|
| Trivial (1 file, known fix) | Do directly | No |
| Bugfix (2-3 files) | `/fix` | Optional |
| Feature small (3-5 files) | `/spec` -> `/build --skip-plan` -> `/verify` -> `/ship` | Yes |
| Feature large (5+ files, multi-system) | `/spec` -> `/plan` -> `/build` -> `/verify` -> `/review` -> `/ship` | Yes |
| Multi-feature project (2+ features, needs orchestration) | `/mission-prep` -> `/missions` | Mission-managed |
| Research | `/research` | If active feature |
| Audit | `/audit` | Yes |
| Init project | `/init` | AGENTS.md + tech-stack.md + CONTEXT.md |
| Cleanup | `/clean` | Removes stale artifacts |
| Architecture upkeep | `/improve-codebase-architecture` | Yes |

## How to triage

1. **Estimate file count**: How many files will this touch?
2. **Is it a bug or a feature?**: Bug = something broken. Feature = something new.
3. **Is it a single feature or multi-feature?**: 1 feature -> mdroid workflow. 2+ features needing orchestration -> /missions.
4. **Is the solution known?**: If yes and small -> trivial. If no -> needs spec or research.
5. **Is external info needed?**: If yes -> research first.

## When to skip the lifecycle

- Trivial changes (typo, config tweak, single-line fix): do directly.
- The user explicitly says "just do it": respect that.
- Emergency hotfix: `/fix` directly, document later.

## Router maintenance rule

This map is the index for every user-reachable command. A new command it never mentions, or a stale one it still routes to, is a router that lies. Whenever you add, rename, remove, or change how a user-reachable command fits the flows, re-read this `SKILL.md` and update it so the map stays accurate. The same trigger applies to the top-level `README.md` command table: every command must have an entry, linked to its `SKILL.md`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It's probably trivial" | Estimate file count. If >1 file, it's not trivial. |
| "I'll skip /spec, I know what to do" | If you know, /spec is fast. If you're wrong, /spec catches it. |
| "Review isn't needed for this" | Review is always needed. --quick mode exists for small changes. |
| "I'll verify at the end" | Verify per task. End-only verification hides which change broke things. |
| "Planning is overhead" | For 5+ file features, planning saves more than it costs. |
| "The router is fine, I'll just add the skill" | A skill the router never mentions is unreachable. Update this map when you add one. |

## Red Flags

- Routing a 5-file feature directly to /build without /spec.
- Skipping /verify before /ship.
- Skipping /review for non-trivial changes.
- Creating artifacts for trivial work.
- Not triaging at all (everything goes through the full lifecycle).
- A command existing that this map never mentions (router is stale).
- This map still routing to a command that was removed or renamed.

---
name: development-lifecycle
description: Full SDLC routing. Maps requests to the right command (spec, plan, build, verify, review, ship, fix, research, audit, clean). Always relevant when a user asks to build, fix, implement, or ship a feature - determines which workflow command applies.
user-invocable: false
---

# Development Lifecycle

The router that maps requests to the right mdroid command.

## Triage gate

Every request passes through triage before entering the workflow:

| Request type | Route | Artifacts? |
|---|---|---|
| Trivial (1 file, known fix) | Do directly | No |
| Bugfix (2-3 files) | `/fix` | Optional |
| Feature small (3-5 files) | `/spec` -> `/build --skip-plan` -> `/verify` -> `/ship` | Yes |
| Feature large (5+ files, multi-system) | `/spec` -> `/plan` -> `/build` -> `/verify` -> `/review` -> `/ship` | Yes |
| Multi-feature project (2+ features, needs orchestration) | `/mission-prep` -> `/missions` | Mission-managed |
| Research | `/research` | If active feature |
| Audit | `/audit` | Yes |
| Init project | `/init` | AGENTS.md + tech-stack.md |
| Cleanup | `/clean` | Removes stale artifacts |

## Lifecycle flow

```
User Request
     |
     v
[TRIAGE GATE]
     |
     +-- Trivial? -----> Do directly (no artifacts)
     |
     +-- Bugfix? ------> /fix ----> /verify ----> done
     |
     +-- Research? ----> /research ----> /spec (if feature) or done
     |
     +-- Audit? -------> /audit ----> /fix (if issues) or done
     |
     +-- Multi-feature? -> /mission-prep -> /missions (agent-driven orchestration)
     |
     +-- Feature? -----> /spec
                            |
                            v
                         /plan (optional for simple)
                            |
                            v
                    /build (auto or task mode, TDD)
                            |
                            v
                    /verify (gates: typecheck, lint, test, build)
                            |
                            v
                    /review (4 personas parallel)
                            |
                            +-- Critical issues? -> /fix -> /verify -> /review
                            |
                            v
                    /ship (commit, PR, deploy)
                            |
                            v
                         DONE
```

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

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It's probably trivial" | Estimate file count. If >1 file, it's not trivial. |
| "I'll skip /spec, I know what to do" | If you know, /spec is fast. If you're wrong, /spec catches it. |
| "Review isn't needed for this" | Review is always needed. --quick mode exists for small changes. |
| "I'll verify at the end" | Verify per task. End-only verification hides which change broke things. |
| "Planning is overhead" | For 5+ file features, planning saves more than it costs. |

## Red Flags

- Routing a 5-file feature directly to /build without /spec.
- Skipping /verify before /ship.
- Skipping /review for non-trivial changes.
- Creating artifacts for trivial work.
- Not triaging at all (everything goes through the full lifecycle).

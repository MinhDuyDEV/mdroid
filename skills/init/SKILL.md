---
name: init
description: Bootstrap a project for mdroid workflow. Creates AGENTS.md with conventions and tech-stack.md with build/test commands. Use when starting work on a new or existing project that lacks AGENTS.md.
user-invocable: true
disable-model-invocation: true
---

# /init - Project Setup

Bootstrap project conventions so mdroid commands work effectively.

## Phase 1: Discover

1. Run `ls` and `git log --oneline -10` to understand project state.
2. Detect the tech stack:
   - `package.json` -> Node/JS/TS
   - `pyproject.toml` / `setup.py` / `requirements.txt` -> Python
   - `go.mod` -> Go
   - `Cargo.toml` -> Rust
   - `pom.xml` / `build.gradle` -> Java/Kotlin
3. Detect build/test/lint commands from config files:
   - `package.json` scripts block
   - `Makefile` targets
   - `pyproject.toml` [tool.*] sections
4. Use the Task tool with `explore` droid to map the directory structure if the project is large.

## Phase 2: Write AGENTS.md

Create `AGENTS.md` in the project root with:

```markdown
# AGENTS.md

## Project
[Name and one-line description]

## Tech Stack
[Detected stack]

## Commands
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Typecheck: `[command]`

## Conventions
- [Commit format, e.g., conventional commits]
- [Branch naming, if any]
- [Code style, if detectable]

## Architecture
[Top-level directory map with one-line descriptions]
```

If `AGENTS.md` already exists, read it and update only the missing sections. Do not overwrite.

## Phase 3: Write tech-stack.md

Create `.factory/tech-stack.md` (create `.factory/` if needed):

```markdown
# Tech Stack

## Language
[language + version]

## Framework
[framework + version]

## Package manager
[detected]

## Build system
[detected]

## Test framework
[detected]

## Lint/format
[detected]
```

## Phase 4: Write .factory/rules/ stubs

Create `.factory/rules/` with coding standards stubs for the detected tech stack.

1. Create the directory: `.factory/rules/`
2. Create a language-specific rules file based on detected stack:
   - Node/TS: `typescript.md` (interface over type, avoid any, named exports, early returns)
   - Python: `python.md` (type hints, pathlib over os.path, explicit over implicit)
   - Go: `go.md` (error handling, interface naming, package layout)
   - Rust: `rust.md` (ownership patterns, Result/Option, clippy compliance)
3. Create `testing.md` (test naming, AAA structure, mock at boundaries, colocate tests)
4. Create `security.md` (never hardcode secrets, validate all input, parameterized queries)

Each rules file uses this format:
```markdown
# [Category] Rules

## [Rule Name]
**Applies to**: [file types, contexts]
**Rule**: [specific instruction]
**Example**: [code showing correct usage]
**Rationale**: [why this matters - optional]
```

5. Reference rules in AGENTS.md:
```markdown
## Coding Standards
Follow the conventions documented in `.factory/rules/`:
- `.factory/rules/<language>.md` - Language patterns
- `.factory/rules/testing.md` - Testing conventions
- `.factory/rules/security.md` - Security requirements
```

If `.factory/rules/` already exists, read existing files and update only missing sections. Do not overwrite.

## Phase 5: Verify

- Confirm `AGENTS.md` exists and has all sections filled.
- Confirm `.factory/tech-stack.md` exists.
- Confirm `.factory/rules/` exists with at least 3 rule files.
- Confirm the commands listed actually run (execute one test command to verify).
- Run `/readiness-report` to evaluate the repo's AI-readiness level. If below Level 4, run `/readiness-fix` to close gaps.

## Next

- `/spec` to define the first feature.
- `/mission-prep` if planning a multi-feature project for Missions.
- `/research` if the project needs investigation first.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The project is simple, no need for AGENTS.md" | Simple projects drift too. Write it. |
| "I'll fill in conventions later" | Write what you know now. Update as you learn. |
| "The README has this info" | AGENTS.md is for agents. README is for humans. Both can coexist. |

## Red Flags

- Overwriting an existing AGENTS.md without reading it first.
- Listing commands without verifying they run.
- Skipping the architecture map.

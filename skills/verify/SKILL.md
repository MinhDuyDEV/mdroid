---
name: verify
description: Run verification gates (typecheck, lint, test, build). All must pass. Supports incremental mode (changed files only) and --full mode. Use after /build or before /ship.
user-invocable: true
disable-model-invocation: true
---

# /verify - Run Verification Gates

Execute all verification gates with fresh evidence. "Seems right" is never sufficient.

## Phase 1: Load commands

1. Read `AGENTS.md` for the project's commands.
2. If no AGENTS.md, detect from config files:
   - `package.json` scripts: `typecheck`, `lint`, `test`, `build`
   - `Makefile` targets: `check`, `lint`, `test`, `build`
   - `pyproject.toml`: `[tool.mypy]`, `[tool.ruff]`, `[tool.pytest]`
3. If a gate has no command, mark it as "N/A - skipped" and note why.

## Phase 2: Determine mode

- **Default (incremental)**: Run gates on changed files only (faster).
  - Get changed files: `git diff --name-only HEAD~1` or `git diff --staged --name-only`.
  - Run lint/typecheck targeting those files where the tool supports it.
- **`/verify --full`**: Run gates on the entire project.

## Phase 3: Check cache

1. Read `.factory/artifacts/<slug>/verify.log` if it exists.
2. Compute current fingerprint: `git rev-parse HEAD` + hash of `git diff --staged`.
3. If fingerprint matches the last verify.log entry -> report "unchanged since last verify" and exit.
4. If no match or `--full` -> proceed to run gates.

## Phase 4: Run gates

Run each gate and capture exit code + output. ALL must pass.

### Gate 1: Typecheck
- Command: [from AGENTS.md or detected]
- Pass: exit 0
- Fail: exit non-zero -> report errors

### Gate 2: Lint
- Command: [from AGENTS.md or detected]
- Pass: exit 0
- Fail: exit non-zero -> report errors

### Gate 3: Test
- Command: [from AGENTS.md or detected]
- Pass: exit 0
- Fail: exit non-zero -> report failing tests

### Gate 4: Build
- Command: [from AGENTS.md or detected]
- Pass: exit 0
- Fail: exit non-zero -> report build errors

## Phase 5: Record results

Write to `.factory/artifacts/<slug>/verify.log`:
```
# Verify Log
## [timestamp] fingerprint: [hash]
- typecheck: PASS (exit 0)
- lint: PASS (exit 0)
- test: FAIL (exit 1) - 2 failures
- build: PASS (exit 0)
```

## Phase 6: Report

Show the user:
```
Verification Results:
- Typecheck: PASS
- Lint: PASS
- Test: FAIL (2 failures)
- Build: PASS

Overall: FAIL
```

## Phase 7: Next step

- All gates PASS -> suggest `/review` (if changes significant) or `/ship` (if trivial).
- Any gate FAIL -> suggest `/fix` to resolve failures, then re-run `/verify`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The tests passed before my change, they'll pass now" | Run them. Changes break things. |
| "Typecheck is slow, I'll skip it" | Type errors are bugs. Run it. |
| "The lint warning isn't related to my change" | Fix it anyway. Lint debt accumulates. |
| "Build works locally, it'll work in CI" | Run the build gate. Don't assume. |
| "I'll fix the failing test later" | No. Failing tests block the gate. Fix now. |

## Red Flags

- Marking a gate as PASS without running it.
- Skipping a gate because "it's not relevant".
- Continuing to /ship with a failing gate.
- Not recording results in verify.log.
- Ignoring cache invalidation (running with stale fingerprint).

## Related Commands

- `/build` - Implement tasks (run /verify after).
- `/review` - Review code after verification passes.
- `/ship` - Commit and ship (requires /verify pass).

## References

- `references/testing-patterns.md` - Test structure and anti-patterns to check during the test gate.
- `references/definition-of-done.md` - Project-wide "done" bar for integration and ship-readiness checks.

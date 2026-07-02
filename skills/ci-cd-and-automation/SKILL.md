---
name: ci-cd-and-automation
description: Pipeline automation with Shift Left and Faster is Safer principles. Use when setting up CI/CD, automating tests, or improving pipeline speed.
user-invocable: false
---

# CI/CD and Automation

Automate the path from code to production. Fast pipelines catch bugs sooner.

## Core principles

### Shift Left
- Catch issues as early as possible in the development cycle.
- Lint and typecheck on save (IDE), not just in CI.
- Run unit tests on commit, not just on PR.
- Security scans on PR, not just on merge.
- The earlier you catch it, the cheaper it is to fix.

### Faster is Safer
- Fast pipelines run more often (developers don't skip them).
- Fast feedback = quick fixes.
- Slow pipelines = context switching = bugs missed.
- Optimize pipeline speed: caching, parallelization, selective testing.

## Pipeline stages

### 1. On save (IDE / pre-commit)
- Format check
- Lint (fast rules only)
- Typecheck (incremental)

### 2. On commit (pre-push hook)
- Unit tests (fast subset)
- Lint (all rules)

### 3. On PR
- Full test suite (unit + integration)
- Typecheck (full)
- Lint (full)
- Build
- Security scan (dependency audit, SAST)
- Coverage check (if applicable)

### 4. On merge to main
- Deploy to staging
- E2E tests on staging
- Smoke tests

### 5. On release tag
- Deploy to production
- Smoke tests on production
- Rollback if smoke fails

## Speed optimization

- **Caching**: cache dependencies, build artifacts, test results.
- **Parallelization**: run test suites in parallel across runners.
- **Selective testing**: only run tests affected by the change (dependency graph).
- **Fail fast**: order stages so the most likely to fail run first.
- **Split unit/integration**: unit tests are fast, run them first. Integration later.

## CI checklist

- [ ] Pipeline runs on every PR (not just main).
- [ ] Pipeline fails on any gate failure (typecheck, lint, test, build).
- [ ] Pipeline is fast enough that devs don't skip it (<10 min target).
- [ ] Dependencies are cached.
- [ ] Tests run in parallel.
- [ ] Security scan runs on PR.
- [ ] Deploy is automated (no manual steps for staging).
- [ ] Rollback is automated or one-click.
- [ ] Pipeline status is visible (PR checks, badges).

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "CI is too slow, we'll fix it later" | Slow CI causes skipped runs. Fix it now. |
| "We'll add tests to CI later" | Tests not in CI don't exist. Add them now. |
| "Security scans can wait" | Shift Left. Scan on PR, not after merge. |
| "Manual deploy is fine" | Manual steps are error-prone. Automate. |
| "We don't need E2E" | Unit tests miss integration bugs. Add E2E on staging. |
| "Caching isn't worth the setup" | Caching can cut pipeline time 50%+. Worth it. |

## Verification

- [ ] Pipeline runs on every PR.
- [ ] All gates (typecheck, lint, test, build) fail the pipeline.
- [ ] Pipeline completes in <10 minutes.
- [ ] Dependencies cached.
- [ ] Tests parallelized.
- [ ] Security scan on PR.
- [ ] Automated deploy to staging on merge.
- [ ] Automated or one-click rollback.

## Red Flags

- CI only runs on main (not on PRs).
- Pipeline passes with failing tests.
- Pipeline takes 30+ minutes.
- No caching (every run reinstalls everything).
- No security scanning.
- Manual deploy steps.
- No rollback path.
- Devs skipping CI because it's too slow.

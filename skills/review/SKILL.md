---
name: review
description: Multi-persona parallel code review. Spawns correctness, security, performance, and test reviewers via Task tool. Supports --quick (1 reviewer) and --deep (5 reviewers + cross-check). Use after /verify passes.
user-invocable: true
disable-model-invocation: true
---

# /review - Multi-Persona Parallel Review

Run focused review personas in parallel to catch issues a single pass misses.

## Modes

- **`/review --quick`**: 1 reviewer (correctness only). Fast.
- **`/review`** (default): 4 reviewers in parallel: correctness, security, performance, tests.
- **`/review --deep`**: 5 reviewers + cross-check. Adds architecture reviewer and cross-persona consistency check.

## Phase 1: Load context

1. Read `.factory/artifacts/.active` -> get slug.
2. Read `.factory/artifacts/<slug>/spec.md` (for success criteria).
3. Get the diff to review:
   - `git diff --staged` (staged changes), or
   - `git diff main...HEAD` (branch changes), or
   - `git diff HEAD~N` (last N commits).
4. Determine scope: which files changed.

## Phase 2: Spawn reviewers

Use the Task tool to spawn reviewers in parallel. Each reviewer gets:
- The diff (or instructions to run `git diff`).
- The spec's success criteria.
- A focused persona prompt (see below).

For the security persona, prefer spawning the `security-audit` droid (which has dedicated STRIDE/OWASP training) instead of a generic prompt. Use the persona prompt below for other dimensions, or when `security-audit` is unavailable.

### Persona 1: Correctness
```
Review this diff for correctness. Check:
- Does the code satisfy the spec's success criteria?
- Edge cases: null, empty, boundary, error paths.
- Off-by-one, race conditions, state errors.
- Stub detection: TODOs, placeholder returns, commented-out code.
Report findings with file:line citations. Severity: Critical/Important/Minor.
```

### Persona 2: Security
```
Review this diff for security issues. Check:
- Input validation on all entry points.
- No secrets/keys/credentials in code or logs.
- SQL/injection/command-injection risks.
- Auth and authorization checks.
Report findings with file:line citations. Severity: Critical/Important/Minor.
```

### Persona 3: Performance
```
Review this diff for performance issues. Check:
- N+1 queries, unbounded loops, O(n^2) where O(n) suffices.
- Unnecessary allocations or copies.
- Missing indexes on hot paths.
- Large payloads or unnecessary data transfer.
Report findings with file:line citations. Severity: Critical/Important/Minor.
```

### Persona 4: Tests
```
Review this diff for test quality. Check:
- Do tests assert behavior, not just "doesn't throw"?
- Are edge cases tested?
- Are there stub/placeholder tests?
- Is test coverage adequate for the new code paths?
Report findings with file:line citations. Severity: Critical/Important/Minor.
```

### Persona 5: Architecture (--deep only)
```
Review this diff for architectural issues. Check:
- Does the change respect existing module boundaries?
- Are new abstractions justified or over-engineered?
- Does the change introduce unwanted coupling?
- Are public interfaces clean and minimal?
Report findings with file:line citations. Severity: Critical/Important/Minor.
```

For `--deep` mode, after all reviewers return, run a cross-check:
- Do findings conflict? (e.g., security says "add validation" but performance says "avoid extra checks")
- Are there findings that span multiple dimensions?

## Phase 3: Collect findings

Gather all reviewer outputs. Merge into a single review report.

## Phase 4: Write review.md

Write to `.factory/artifacts/<slug>/review.md`:

```markdown
# Review: [feature name]
## Date: [timestamp]

## Summary
[1-2 sentence verdict]

## Critical (must fix)
- `path:line` - [issue] (found by: [persona]) -> [recommended fix]

## Important (should fix)
- `path:line` - [issue] (found by: [persona]) -> [recommended fix]

## Minor (nice to have)
- `path:line` - [observation] (found by: [persona])

## Passed checks
- [what was verified and looks correct]
```

## Phase 5: Auto-fix rule

- **Critical** -> fix inline now, then re-run `/verify`. Don't ship with critical issues.
- **Important** -> fix inline now if quick, otherwise log to review.md for follow-up.
- **Minor** -> log to review.md. Don't fix now (avoid scope creep).

For critical fixes: make the minimal change, stage specific files, re-run the affected test.

## Phase 6: Report

Show the user the review summary. If critical issues were found and fixed, note the fix and re-verification.

## Next

- No critical issues -> `/ship`.
- Critical issues remain -> `/fix` to resolve, then `/verify`, then re-`/review`.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I reviewed it myself, no need for personas" | Single-pass review misses dimension-specific issues. That's why we fan out. |
| "The security persona isn't needed, this isn't a security feature" | Everything is a security feature. Run it. |
| "Performance is fine for now" | That's a Minor finding, not a reason to skip the persona. |
| "Tests look fine" | The test persona checks quality, not just existence. Run it. |
| "I'll fix critical issues after shipping" | Never. Critical = block ship. Fix first. |

## Red Flags

- Reviewers returning "looks good" without listing what they checked.
- Findings without file:line citations.
- Skipping a persona "because it's not relevant".
- Shipping with unresolved critical issues.
- Not recording findings in review.md.

## Related Commands

- `/verify` - Run verification gates before review.
- `/fix` - Fix critical issues found by review.
- `/ship` - Ship after review passes.

## References

Personas should load these checklists during review:
- `references/security-checklist.md` - Security persona: input validation, auth, data protection, OWASP Top 10.
- `references/performance-checklist.md` - Performance persona: Core Web Vitals, N+1 queries, bundle size.
- `references/accessibility-checklist.md` - Frontend review: keyboard nav, screen readers, contrast, ARIA.
- `references/testing-patterns.md` - Test persona: AAA structure, mock anti-patterns, test types.

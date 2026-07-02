---
name: audit
description: Codebase pattern audit. Finds all occurrences of a pattern, reviews each for issues, and synthesizes prioritized remediation. Use to find tech debt, security anti-patterns, or consistency issues across the codebase.
user-invocable: true
disable-model-invocation: true
---

# /audit - Codebase Pattern Audit

Find all occurrences of a pattern, review each, and produce a prioritized remediation plan.

## Phase 1: Define the audit

1. Parse the user's request: what pattern to audit?
   - Examples: "all raw SQL queries", "all API endpoints without auth", "all useEffect hooks", "all try-catch blocks that swallow errors".
2. If no pattern given, ask the user what to audit.
3. Derive a slug if this is part of a feature, otherwise run standalone.

## Phase 2: Discover (explore)

Use the Task tool with `explore` droid (or Grep/Glob directly for small projects):

1. Grep for the pattern across the codebase.
2. Collect all occurrences with file:line.
3. Categorize by location (module/directory).

## Phase 3: Review each occurrence

Use the Task tool with `review` droid (or review directly for small sets):

For each occurrence:
1. Read the surrounding context.
2. Check for issues: is the pattern used correctly? Are there anti-patterns? Security risks? Performance issues?
3. Classify severity: Critical / Important / Minor.
4. Note the specific issue and recommended fix.

For large sets (>20 occurrences), batch them and review in parallel via Task tool.

## Phase 4: Synthesize

Use the Task tool with `general` droid (or synthesize directly):

1. Group findings by severity.
2. Identify common issues across occurrences.
3. Prioritize: Critical first, then Important, then Minor.
4. Note any systemic issues (e.g., "all API endpoints in module X lack auth").

## Phase 5: Write audit.md

If there's an active feature, write to `.factory/artifacts/<slug>/audit.md`. Otherwise, report directly.

```markdown
# Audit: [pattern]

## Summary
[N occurrences across M files. K critical, J important, L minor.]

## Critical
- `path:line` - [issue] -> [fix]

## Important
- `path:line` - [issue] -> [fix]

## Minor
- `path:line` - [observation]

## Systemic issues
- [if any patterns are widespread]

## Remediation priority
1. [highest priority fix]
2. [next priority]
```

## Next

- If critical/important issues found -> suggest `/fix` (for specific fixes) or `/spec` (for larger remediation).
- If no issues -> report "audit clean".

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "I'll just check a few examples" | Audit means ALL occurrences. Don't sample. |
| "Minor issues aren't worth reporting" | Report them. The team decides what to fix. |
| "I'll fix issues as I find them" | No. Audit is read-only. Fix in /fix after. |
| "The pattern is fine everywhere" | Verify each occurrence. Don't assume. |

## Red Flags

- Sampling instead of checking all occurrences.
- Fixing issues during the audit (audit is read-only).
- No severity classification.
- Not grouping findings by priority.
- Missing systemic issues (patterns across many files).

## Related Commands

- `/fix` - Fix critical issues found by the audit.
- `/spec` - Spec a larger remediation effort.
- `/research` - Research best practices if the pattern is unclear.

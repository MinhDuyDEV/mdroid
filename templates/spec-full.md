# Spec: [Feature Name]

## Problem
[2-4 sentences: What's wrong or what's needed. Why does this matter?]

## Solution
[2-4 sentences: High-level approach. What will we build?]

## Affected Files
- `src/path/to/file.ts` - [what changes]
- `src/path/to/other.ts` - [what changes]

## Tasks
- [ ] [T1] [Task description] -> Verify: `[command]`
- [ ] [T2] [Task description] -> Verify: `[command]`
- [ ] [T3] [Task description] -> Verify: `[command]`

## Success Criteria
- [Observable criterion 1: e.g., "User can log in with email and password"]
- [Observable criterion 2: e.g., "Invalid login shows error message"]
- [Verify: `npm run typecheck && npm run lint && npm test`]
- [Verify: `[specific integration or E2E test]`]

## Out of Scope
- [What's explicitly NOT included in this feature]
- [Edge cases deferred to later iterations]

## Constraints
- [Performance: e.g., "API response < 200ms p95"]
- [Compatibility: e.g., "Must work with Node 18+"]
- [Security: e.g., "All inputs validated"]

## Dependencies
- [External dependency 1: e.g., "Requires v2 of library X"]
- [Internal dependency 1: e.g., "Depends on auth service being updated"]

## Open Questions
- [ ] [Question 1: needs answer before/during implementation]

## Anti-Rationalization

| Rationalization | Rebuttal |
|---|---|
| "Success criteria are obvious" | If obvious, writing them is cheap. If not, they're critical. |
| "I'll figure out scope during implementation" | Scope creep is the #1 spec failure. Bound it now. |
| "Out of scope isn't needed" | Even small features drift. State what's NOT included. |
| "Constraints can be flexible" | State them. Flexible constraints become no constraints. |

## Red Flags
- Success criteria that can't be tested or observed.
- No out-of-scope section.
- Spec covers multiple unrelated features (split it).
- Tasks without verification commands.
- Vague "it should work" criteria without specifics.

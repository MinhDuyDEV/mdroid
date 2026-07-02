---
name: documentation-and-adrs
description: Write Architecture Decision Records and maintain documentation that stays useful. Use when making significant architectural decisions or documenting system design.
user-invocable: false
---

# Documentation and ADRs

Capture decisions and designs while they're fresh. Documentation that decays is worse than none.

## Architecture Decision Records (ADRs)

An ADR records a decision, its context, and its consequences.

### ADR format

```markdown
# ADR-[N]: [Decision title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-X]

## Date
[YYYY-MM-DD]

## Context
[Why this decision is needed. What problem are we solving? What constraints exist?]

## Decision
[What we decided. Be specific. "We will use X for Y because Z."]

## Consequences
- Positive: [what we gain]
- Negative: [what we lose or risk]
- Neutral: [side effects to note]

## Alternatives considered
- [Alternative 1]: [why not chosen]
- [Alternative 2]: [why not chosen]
```

### When to write an ADR

- Choosing a framework, library, or service.
- Architectural patterns (monolith vs microservices, sync vs async).
- Data storage decisions (SQL vs NoSQL, schema design).
- Security model choices.
- Any decision that's hard to reverse and affects multiple people.

### When NOT to write an ADR

- Trivial implementation choices (variable names, file organization).
- Decisions that are easily reversible.
- Personal preferences with no team impact.

## Documentation types

### 1. AGENTS.md (always current)
- Project conventions, build/test commands, architecture map.
- Updated by `/init` and maintained over time.
- This is the first file an agent reads. Keep it accurate.

### 2. API documentation
- Generated from code (OpenAPI, JSDoc, docstrings).
- Examples for every endpoint/function.
- Keep examples runnable (test them in CI).

### 3. Runbooks
- How to deploy, rollback, debug, and handle incidents.
- Step-by-step, copy-pasteable commands.
- Owned by the team on call.

### 4. ADRs (append-only)
- Record of past decisions.
- Never edit an accepted ADR. Supersede it with a new one.

## Documentation maintenance

- **Update on change**: If you change the code, update the docs in the same PR.
- **Test examples**: Runnable examples in CI. If they break, the docs are wrong.
- **Delete stale docs**: Outdated docs mislead. Remove or update them.
- **Single source of truth**: Don't duplicate. Link to the canonical source.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "The code is self-documenting" | Code shows what. Docs show why. You need both. |
| "I'll write the ADR later" | Later = never. Write it when you make the decision. |
| "Docs always go stale" | They go stale if you don't update them with the code. |
| "Nobody reads docs" | Then make them better. Bad docs aren't read. Good docs are. |
| "ADR is overkill for this" | If it affects multiple people and is hard to reverse, it's not overkill. |

## Verification

- [ ] ADR exists for significant architectural decisions.
- [ ] AGENTS.md reflects current conventions and commands.
- [ ] API docs match the actual API.
- [ ] Examples in docs are runnable and tested.
- [ ] No stale documentation (outdated docs removed or updated).
- [ ] Single source of truth (no duplication).

## Red Flags

- No ADRs for major architectural decisions.
- AGENTS.md with outdated commands.
- API docs that don't match the implementation.
- Untested code examples in documentation.
- Duplicated docs that diverge over time.
- Editing accepted ADRs instead of superseding them.

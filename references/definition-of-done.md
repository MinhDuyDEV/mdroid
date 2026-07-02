# Definition of Done

> Project-wide standing bar. Every task must clear this before marking complete.

## Correctness
- [ ] Code does what the spec/requirement says.
- [ ] Edge cases handled: null, empty, boundary, error paths.
- [ ] No stubs, TODOs, or placeholder returns in shipped code paths.
- [ ] No commented-out code or dead code.

## Quality
- [ ] Code is readable and follows project conventions (AGENTS.md).
- [ ] Naming is clear (no cryptic abbreviations).
- [ ] Functions are focused (one responsibility).
- [ ] No unnecessary complexity (YAGNI).

## Integration
- [ ] Typecheck passes.
- [ ] Lint passes.
- [ ] Tests pass.
- [ ] Build passes.
- [ ] No breaking changes to public APIs (or migration path documented).

## Documentation
- [ ] Public interfaces documented.
- [ ] Complex logic has comments explaining WHY (not WHAT).
- [ ] ADR written for architectural decisions.
- [ ] Changelog updated (if user-visible change).

## Ship-readiness
- [ ] Code review completed (no unresolved critical issues).
- [ ] Verification gates green (typecheck, lint, test, build).
- [ ] No secrets, keys, or credentials in code.
- [ ] Commit uses conventional commit format.
- [ ] Files staged intentionally (no `git add .`).

## Anti-patterns (NOT done)
- "It works on my machine" without CI verification.
- "Tests pass" without running them.
- "I'll document later".
- "Review can wait".
- "It's a minor change, skip the gates".

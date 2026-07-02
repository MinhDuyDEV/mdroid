---
name: defense-in-depth
description: Security hardening patterns for layered defense. Input validation, output encoding, least privilege, fail-safe defaults. Use when implementing security-sensitive features or hardening existing code.
user-invocable: false
---

# Defense in Depth

Layered security patterns. No single layer is sufficient; combine them.

## Layer 1: Input validation

Validate at every trust boundary:
- **External input** (HTTP, CLI, file, env): validate type, length, format, range.
- **Inter-service input**: validate even internal calls. Trust boundaries shift.
- **Fail safe**: on validation failure, reject. Don't attempt to "clean" and proceed.

Patterns:
- Whitelist allowed values. Don't blacklist forbidden ones.
- Validate before processing, not after.
- Use parameterized queries for SQL. Always. No string concatenation.
- Encode output for the target context (HTML, URL, JS, CSS).

## Layer 2: Authentication and authorization

- Authenticate every request. No implicit trust.
- Authorize per resource, not just per endpoint.
- Use least privilege: grant the minimum needed.
- Rotate credentials. No long-lived secrets in code.
- Log auth events (success and failure).

## Layer 3: Fail-safe defaults

- On error, deny access. Don't grant.
- On timeout, fail closed. Don't fail open.
- On config missing, use secure defaults. Don't use permissive defaults.
- On parse error, reject input. Don't process partially.

## Layer 4: Logging and monitoring

- Log security events: auth, authz, input validation failures, errors.
- Don't log secrets: passwords, tokens, keys, PII.
- Log enough to investigate, not enough to compromise.
- Alert on anomalies: spike in failures, unexpected access patterns.

## Layer 5: Dependency security

- Pin dependencies. Don't use floating versions.
- Audit dependencies regularly (`npm audit`, `pip audit`, etc.).
- Review new dependencies before adding.
- Remove unused dependencies (they're attack surface).

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It's an internal API, no need to validate" | Internal APIs become external. Validate anyway. |
| "The frontend already validates" | Frontend validation is UX, not security. Server must validate. |
| "I'll add auth later" | No. Auth first. Unauthenticated endpoints are security debt. |
| "Logging the token helps debugging" | Logged tokens are leaked tokens. Don't log secrets. |
| "This dependency is small, no need to audit" | Small dependencies can be malicious. Audit all. |

## Verification

- [ ] All external inputs validated (type, length, format, range).
- [ ] All SQL uses parameterized queries.
- [ ] All output encoded for target context.
- [ ] Auth on every endpoint.
- [ ] Authz checks per resource.
- [ ] No secrets in code or logs.
- [ ] Fail-safe defaults on errors.
- [ ] Dependencies pinned and audited.

## Red Flags

- String-concatenated SQL.
- Unvalidated external input.
- Auth checked at endpoint level only (not per resource).
- Secrets in logs, config files, or source code.
- Floating dependency versions.
- Fail-open error handling.

## References

- `references/security-checklist.md` - Pre-commit security checks, OWASP Top 10 quick check, secrets checklist.

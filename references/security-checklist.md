# Security Checklist

> Pre-commit security checks. Pulled in by /review (security persona) and defense-in-depth skill.

## Pre-commit checks

### Input validation
- [ ] All external inputs validated (type, length, format, range).
- [ ] SQL uses parameterized queries (no string concatenation).
- [ ] No `eval()`, `exec()`, or dynamic code execution with untrusted input.
- [ ] Command execution uses argument arrays (no shell=True with input).
- [ ] File paths validated against traversal (`..`).

### Authentication
- [ ] Authentication required on every endpoint that needs it.
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1).
- [ ] No plaintext passwords stored or logged.
- [ ] Session tokens are random, unguessable, and expire.
- [ ] JWT tokens validated (signature, expiry, issuer).

### Authorization
- [ ] Authorization checks per resource (not just per endpoint).
- [ ] Users can only access their own resources (no IDOR).
- [ ] Admin endpoints require admin role.
- [ ] No privilege escalation paths.

### Data protection
- [ ] No secrets in source code (API keys, passwords, tokens).
- [ ] No secrets in logs, error messages, or debug output.
- [ ] Sensitive data encrypted at rest (PII, passwords, tokens).
- [ ] HTTPS enforced (no HTTP endpoints in production).
- [ ] HSTS header set.

### Headers
- [ ] `Content-Security-Policy` set (restricts script sources).
- [ ] `X-Content-Type-Options: nosniff` set.
- [ ] `X-Frame-Options: DENY` or `SAMEORIGIN` (prevents clickjacking).
- [ ] `Strict-Transport-Security` set (HSTS).
- [ ] `Referrer-Policy` set.

### CORS
- [ ] CORS origins whitelisted (no `*` for credentialed requests).
- [ ] CORS methods restricted to needed ones.
- [ ] CORS headers minimal.

### Dependencies
- [ ] Dependencies pinned (no floating versions in production).
- [ ] `npm audit` / `pip audit` / `go vet` passes.
- [ ] No known vulnerable dependencies.
- [ ] Unused dependencies removed.

## OWASP Top 10 quick check

1. **Injection**: Parameterized queries? No dynamic SQL/commands?
2. **Broken Auth**: Strong password storage? Session management?
3. **Sensitive Data Exposure**: Encryption at rest and in transit?
4. **XXE**: XML parsers disable external entities?
5. **Broken Access Control**: Per-resource authz? No IDOR?
6. **Security Misconfiguration**: Default configs secure? Error messages generic?
7. **XSS**: Output encoded? CSP set?
8. **Insecure Deserialization**: No untrusted deserialization?
9. **Known Vulnerabilities**: Dependencies audited?
10. **SSRF**: Internal URLs not fetched from external input?

## Secrets checklist
- [ ] No `.env` files committed (check `.gitignore`).
- [ ] No hardcoded API keys, tokens, or passwords.
- [ ] Secrets loaded from env vars or secret manager.
- [ ] `git diff --cached` checked for secrets before commit.

## Red Flags
- `eval()` or `exec()` with any input.
- String-concatenated SQL.
- `shell=True` with subprocess.
- `*` in CORS origin with credentials.
- Secrets in source code or logs.
- MD5 or SHA1 for password hashing.
- No auth on a data-modifying endpoint.
- Error messages that reveal stack traces or internal info.

---
name: api-and-interface-design
description: Contract-first API design. Hyrum's Law, One-Version Rule, versioning, and backward compatibility. Use when designing public APIs, library interfaces, or service contracts.
user-invocable: false
---

# API and Interface Design

Design interfaces as contracts. Every public surface is a commitment.

## Core principles

### Contract-first
- Define the interface before implementing.
- The interface is the contract: inputs, outputs, errors, behavior.
- Document non-obvious behavior (side effects, ordering guarantees, idempotency).
- Once published, the contract is hard to change. Design carefully.

### Hyrum's Law
> With a sufficient number of users, every observable behavior of your system will be depended on by someone.

- Anything visible (return value, error message, timing, order) becomes a dependency.
- Minimize observable surface. Only expose what's intentionally part of the contract.
- Internal details should not leak into the public interface.

### One-Version Rule
- Internal code should depend on one version of a dependency.
- Don't let different modules use different versions of the same library.
- For published libraries: semantic versioning. Breaking changes = major version bump.

### Backward compatibility
- New versions must not break existing consumers.
- Additive changes (new fields, new endpoints) are safe.
- Breaking changes (removed fields, changed types, changed behavior) require:
  - Major version bump (for published APIs).
  - Migration path (see deprecation-and-migration skill).
  - Notice period.

## Interface design checklist

### Inputs
- [ ] Required vs optional fields are explicit.
- [ ] Types are precise (not `any`, not `string` when it should be `UUID`).
- [ ] Validation rules documented (format, range, length).
- [ ] Default values documented.
- [ ] Error behavior for invalid input documented.

### Outputs
- [ ] Response shape is stable and documented.
- [ ] Nullable fields are explicit.
- [ ] Error responses have a consistent shape.
- [ ] Pagination strategy defined (cursor, offset, limit).
- [ ] No internal implementation details leaked.

### Errors
- [ ] Error codes are stable and documented.
- [ ] Error messages are actionable (tell the consumer what to do).
- [ ] HTTP status codes used correctly (4xx = client error, 5xx = server error).
- [ ] No stack traces or internal info in error responses.

### Versioning
- [ ] Version in URL (`/v1/`) or header (`Accept: application/vnd.api+json;version=1`).
- [ ] Old version supported during migration period.
- [ ] Version deprecation communicated.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "We'll document the API later" | The API IS the documentation. Design it first. |
| "It's an internal API, no need for contracts" | Internal APIs become external. Write the contract. |
| "We can change it, we control all consumers" | You don't. And future-you will suffer. |
| "The error message is obvious" | Document it. Obvious to you isn't obvious to consumers. |
| "We'll add versioning when we need it" | Add it now. Retrofitting versioning is painful. |
| "Nullable is implied" | Make it explicit. Implication = ambiguity = bugs. |

## Verification

- [ ] Interface defined before implementation.
- [ ] All fields have types and validation rules.
- [ ] Error responses are consistent and documented.
- [ ] No internal details in public surface.
- [ ] Versioning strategy defined.
- [ ] Backward compatibility plan exists.
- [ ] Pagination, filtering, sorting defined (if applicable).

## Red Flags

- Implementing before defining the interface.
- `any` types or untyped string fields.
- Error responses with stack traces.
- No versioning for a public API.
- Internal implementation details in responses.
- No documentation of nullable/optional fields.
- Breaking changes without a migration path.

---
name: deprecation-and-migration
description: Code-as-liability. Safe deprecation paths, migration plans, and removal schedules. Use when removing features, migrating APIs, or cleaning up legacy code.
user-invocable: false
---

# Deprecation and Migration

Code is liability. Remove it safely, on a schedule, with migration paths.

## Principle

Every line of code is a maintenance cost. Unused code, deprecated APIs, and legacy patterns accumulate until they block progress. Deprecate deliberately, migrate safely, remove on schedule.

## Deprecation lifecycle

### 1. Mark deprecated
- Add `@deprecated` annotation (JS/TS), `@Deprecated` (Java/Python), or deprecation notice in docs.
- Include: what to use instead, when this will be removed, link to migration guide.
- Log a deprecation warning when the deprecated path is used (runtime visibility).

### 2. Migration path
- Document the replacement clearly.
- Provide a migration guide: old -> new mapping, code examples.
- If the API changed: provide a compatibility shim if feasible.
- If the behavior changed: document the difference explicitly.

### 3. Notice period
- Keep the deprecated code working during the notice period.
- Minimum: one release cycle. Recommended: two.
- Announce the deprecation in release notes, changelogs, and (if applicable) runtime warnings.

### 4. Remove
- After the notice period, remove the deprecated code.
- Remove tests for the deprecated code.
- Update docs to remove references.
- Note the removal in release notes.

## Migration strategies

### Strangler fig pattern
- New functionality goes to the new system.
- Old functionality stays until fully replaced.
- Gradually route calls from old to new.
- Remove old system when no calls remain.

### Expand-contract pattern
- **Expand**: add the new API/field alongside the old one.
- **Migrate**: move consumers to the new API/field.
- **Contract**: remove the old API/field.

### Feature flag migration
- Put new behavior behind a feature flag.
- Roll out to a subset of users.
- Monitor for issues.
- Remove the flag (and old code) when stable.

## Deprecation checklist

- [ ] `@deprecated` annotation with reason and replacement.
- [ ] Runtime warning when deprecated path is used.
- [ ] Migration guide written.
- [ ] Removal date/schedule defined.
- [ ] Release notes updated.
- [ ] Consumers identified and notified.
- [ ] Compatibility shim provided (if feasible).

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "Nobody uses this old code" | Verify with usage tracking. Don't guess. |
| "I'll remove it now, it's obviously unused" | Deprecate first. Someone might depend on it. |
| "The migration guide isn't needed, it's obvious" | Obvious to you. Write it for the person who isn't you. |
| "I'll keep the old code just in case" | That's how code rot starts. Remove on schedule. |
| "The shim is too much work" | Shims enable gradual migration. Worth the effort. |
| "We'll deprecate someday" | "Someday" never comes. Set a date. |

## Verification

- [ ] Deprecated code has `@deprecated` annotation.
- [ ] Replacement is documented.
- [ ] Migration guide exists.
- [ ] Removal date is set and communicated.
- [ ] Runtime warnings fire on deprecated path usage.
- [ ] No new code uses the deprecated path.

## Red Flags

- Removing code without a deprecation period.
- No migration guide for a breaking change.
- No runtime warning for deprecated paths.
- Keeping deprecated code indefinitely "just in case".
- New code using deprecated paths.
- No removal schedule.

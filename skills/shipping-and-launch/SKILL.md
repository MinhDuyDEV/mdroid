---
name: shipping-and-launch
description: Pre-launch checklists and staged rollouts. Use before deploying to production to verify readiness and plan safe rollout.
user-invocable: false
---

# Shipping and Launch

Ship safely with checklists and staged rollouts. A failed launch costs more than a delayed one.

## Pre-launch checklist

### Code readiness
- [ ] All verification gates pass (typecheck, lint, test, build).
- [ ] Code review completed (no unresolved critical issues).
- [ ] No TODOs or stubs in shipped code paths.
- [ ] No debug logging or console output in production paths.
- [ ] No hardcoded secrets, keys, or credentials.

### Test readiness
- [ ] Unit tests pass and cover new code paths.
- [ ] Integration tests pass.
- [ ] E2E tests pass on staging.
- [ ] Edge cases tested (empty, null, boundary, concurrent).
- [ ] Error paths tested.
- [ ] Performance tests pass (if applicable).

### Operational readiness
- [ ] Monitoring and alerting configured.
- [ ] Dashboards updated.
- [ ] On-call runbook written or updated.
- [ ] Rollback plan documented and tested.
- [ ] Feature flags configured (for staged rollout).
- [ ] Rate limits and quotas set (if applicable).

### Documentation readiness
- [ ] API docs updated (if API change).
- [ ] Changelog updated.
- [ ] Migration guide written (if breaking change).
- [ ] ADR written (if architectural decision).
- [ ] User-facing docs updated (if behavior change).

### Communication
- [ ] Release notes written.
- [ ] Stakeholders notified.
- [ ] Support team briefed (if user-facing change).
- [ ] Deploy window scheduled (low-traffic if risky).

## Staged rollout

### Stage 1: Internal (canary)
- Deploy to internal users or a canary environment.
- Monitor: error rate, latency, user feedback.
- Duration: 1-24 hours.

### Stage 2: Small percentage
- Roll out to 1-5% of users (via feature flag).
- Monitor: error rate, latency, conversion, support tickets.
- Duration: 1-3 days.

### Stage 3: Larger percentage
- Roll out to 25-50% of users.
- Monitor same metrics.
- Duration: 1-2 days.

### Stage 4: Full rollout
- Roll out to 100%.
- Monitor for 24 hours.
- Keep feature flag for emergency rollback.

### Rollback triggers
- Error rate exceeds threshold (e.g., >1% above baseline).
- Latency p95 exceeds SLO.
- Critical user-facing bug reported.
- Data integrity issue.

On any trigger: roll back immediately. Investigate, fix, re-roll out.

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "It worked in staging, prod will be fine" | Staging != prod. Monitor and stage the rollout. |
| "We'll fix issues after launch" | No. Fix before launch. Post-launch fixes are hotfixes. |
| "Full rollout is faster" | Faster = riskier. Stage it. |
| "Monitoring can wait" | Unmonitored launches are unfixable. Set up monitoring first. |
| "The checklist is too long" | Each item prevents a class of failure. Don't skip. |
| "We don't need a rollback plan" | Every launch needs a rollback plan. Always. |

## Verification

- [ ] All pre-launch checklist items verified.
- [ ] Staged rollout plan defined.
- [ ] Monitoring and alerting active.
- [ ] Rollback plan documented and tested.
- [ ] On-call runbook updated.
- [ ] Communication sent to stakeholders.

## Red Flags

- Launching without monitoring.
- Full rollout without staging.
- No rollback plan.
- Unresolved critical issues in review.
- Debug output in production code.
- No feature flag for emergency rollback.
- Launching during high-traffic period (for risky changes).

## References

- `references/definition-of-done.md` - Project-wide "done" bar (correctness, quality, integration, documentation, ship-readiness).
- `references/security-checklist.md` - Pre-launch secrets and security verification.

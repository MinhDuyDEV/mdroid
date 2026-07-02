---
name: observability-and-instrumentation
description: Structured logging, RED metrics, OpenTelemetry tracing, and symptom-based alerting. Use when instrumenting services for production observability.
user-invocable: false
---

# Observability and Instrumentation

Make systems observable. You can't fix what you can't see.

## Three pillars

### 1. Structured logging
- Log in structured format (JSON), not free text.
- Include: timestamp, level, message, request_id, user_id, duration, error.
- Log levels: DEBUG (dev), INFO (lifecycle), WARN (degraded), ERROR (failed).
- Don't log secrets. Don't log full payloads. Log enough to investigate.

### 2. RED metrics (for services)
- **R**ate: requests per second.
- **E**rrors: error rate (failed requests / total).
- **D**uration: latency distribution (p50, p95, p99).
- Expose via `/metrics` endpoint (Prometheus format) or send to metrics service.

### 3. Distributed tracing
- Trace every request end-to-end.
- Use OpenTelemetry spans: service -> operation -> duration -> status.
- Propagate trace context across service boundaries.
- Sample: 100% for errors, sampled for success (reduce cost).

## Instrumentation checklist

For each service:
- [ ] Structured JSON logging with request_id correlation.
- [ ] RED metrics exposed (rate, errors, duration).
- [ ] Distributed tracing on every external request.
- [ ] Health check endpoint (`/health` or `/ready`).
- [ ] Error tracking integration (Sentry, etc.).

For each endpoint:
- [ ] Log: method, path, status, duration, request_id.
- [ ] Metric: counter (requests), histogram (latency), gauge (in-flight).
- [ ] Span: operation name, attributes, status.

## Symptom-based alerting

Alert on symptoms (user-visible problems), not causes:
- **Alert**: "error rate > 1% for 5 minutes" (symptom: users see errors).
- **Don't alert**: "CPU > 80%" (cause: might be fine, might not).

Alert rules:
- Error rate exceeds threshold.
- Latency p95 exceeds SLO.
- Uptime check fails.
- Saturation approaching limit (disk, memory, connections).

## On-call questions

Design observability so an on-call engineer can answer:
1. Is the system working right now? (health check)
2. Is the system fast enough? (latency metrics)
3. Are users seeing errors? (error rate)
4. Where is the bottleneck? (tracing)
5. What changed recently? (deploy markers in metrics/traces)

## Common Rationalizations

| Rationalization | Rebuttal |
|---|---|
| "Logs are enough, no need for metrics" | Logs tell you what happened. Metrics tell you what's happening. You need both. |
| "Tracing is too expensive" | Sample. 100% for errors, 10% for success. Cost is manageable. |
| "We'll add observability after launch" | No. Unobservable systems in production are unfixable. |
| "Free-text logs are fine" | Structured logs are searchable and parseable. Free text is not. |
| "We don't need alerting yet" | You need it before users complain, not after. |

## Verification

- [ ] Structured JSON logging with correlation IDs.
- [ ] RED metrics exposed for every service.
- [ ] Distributed tracing on external requests.
- [ ] Health check endpoint.
- [ ] Alert rules on symptoms (error rate, latency, uptime).
- [ ] No secrets in logs.
- [ ] Deploy markers in metrics/traces.

## Red Flags

- Free-text logs without structure.
- No request_id correlation.
- Alerting on causes (CPU, memory) instead of symptoms (errors, latency).
- No tracing for multi-service requests.
- Logging secrets or full payloads.
- No health check endpoint.

## References

- `references/observability-checklist.md` - On-call questions, RED/USE metrics, tracing, logging, alerting, dashboard checklists.

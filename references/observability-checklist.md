# Observability Checklist

> On-call questions, RED/USE metrics, tracing. Pulled in by observability-and-instrumentation skill.

## On-call questions

An on-call engineer should be able to answer these within 5 minutes:

1. **Is the system working right now?**
   - Health check endpoint (`/health` or `/ready`).
   - Uptime monitor (external probe).

2. **Is the system fast enough?**
   - Latency p50, p95, p99 metrics.
   - SLO defined (e.g., p95 < 200ms).

3. **Are users seeing errors?**
   - Error rate metric (errors / total requests).
   - Error alert threshold (e.g., > 1% for 5 min).

4. **Where is the bottleneck?**
   - Distributed tracing (which service/operation is slow).
   - Resource metrics (CPU, memory, disk, network).

5. **What changed recently?**
   - Deploy markers in metrics/traces.
   - Recent deploy log or changelog.

## RED metrics (services)

For every service:
- **R**ate: requests per second (counter).
- **E**rrors: error count/rate (counter).
- **D**uration: latency distribution (histogram: p50, p95, p99).

Expose via `/metrics` (Prometheus format) or send to metrics service.

## USE metrics (resources)

For every resource (CPU, memory, disk, network):
- **U**tilization: percentage of capacity used (gauge).
- **S**aturation: queue length / pending work (gauge).
- **E**rrors: error count (counter).

## Tracing checklist
- [ ] Every external request has a trace span.
- [ ] Trace context propagated across service calls.
- [ ] Spans include: operation name, service, duration, status, attributes.
- [ ] Sampling: 100% for errors, sampled for success.
- [ ] Trace visualization tool configured (Jaeger, Zipkin, Tempo).

## Logging checklist
- [ ] Structured JSON logs (not free text).
- [ ] Correlation ID (`request_id` or `trace_id`) in every log.
- [ ] Log levels used correctly (DEBUG, INFO, WARN, ERROR).
- [ ] No secrets in logs (passwords, tokens, keys, PII).
- [ ] Log retention configured (not infinite, not zero).

## Alerting checklist
- [ ] Alerts on symptoms (error rate, latency, uptime), not causes (CPU, disk).
- [ ] Alert thresholds defined with SLOs.
- [ ] Alert routing configured (PagerDuty, Slack, email).
- [ ] No alert fatigue (tune thresholds to reduce false positives).
- [ ] Runbook linked in every alert.

## Dashboard checklist
- [ ] Service overview dashboard (RED metrics).
- [ ] Resource dashboard (USE metrics).
- [ ] Error dashboard (error rate, top errors, error trends).
- [ ] Deploy marker overlay on all dashboards.
- [ ] SLO dashboard (current vs target for each SLO).

## Symptom-based alerting rules
- Error rate > 1% for 5 minutes.
- Latency p95 > SLO for 10 minutes.
- Uptime check fails for 2 consecutive checks.
- Disk saturation > 90% for 30 minutes.
- Memory saturation approaching limit.

## Red Flags
- No health check endpoint.
- Free-text logs without structure.
- No correlation ID across services.
- Alerts on CPU/memory (causes) instead of errors/latency (symptoms).
- No tracing for multi-service requests.
- Secrets in logs.
- No runbook linked in alerts.
- No deploy markers on dashboards.

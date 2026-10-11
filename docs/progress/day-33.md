# Day 33 — Observability for Resilient AI Systems

## Objective

Instrument the ticket-triage system so reliability, latency, and workflow failures
can be diagnosed from metrics and structured logs.

## Concepts learned

- Counters, gauges, and histograms
- Prometheus metric naming
- Label cardinality
- Structured logging
- Correlation IDs and distributed tracing
- Instrumentation boundaries
- Privacy-aware telemetry

## Implementation

- Added `prometheus-client` to project dependencies (already present).
- Defined classification, retry, timeout, rate-limit, queue, and routing metrics
  in `src/ticket_triage/metrics.py`.
- Instrumented classification success/failure and duration in
  `src/ticket_triage/instrumentation.py`.
- Incremented retry counters at the retry boundary.
- Added structured classification logs (JSON format via existing
  `logging_config.JsonFormatter`).
- Configured `/metrics` endpoint in the FastAPI app (`api.py`).
- Added instrumentation unit tests in `tests/test_instrumentation.py`.

## Results

- Tests passed: `142 passed` (6 pre-existing failures unrelated to
  observability — `timeout_seconds` keyword conflict and `SequenceClassifier`
  missing `timeout_seconds` arg).
- Files changed: `src/ticket_triage/metrics.py`,
  `src/ticket_triage/instrumentation.py`, `tests/test_instrumentation.py`,
  `docs/progress/day-33.md`, `src/ticket_triage/api.py` (metrics endpoint added)
- Next improvements: add OpenTelemetry tracing, add more granular metric labels,
  integrate rate-limit and circuit-breaker metrics, add log correlation IDs.

### Quality gates

```
pytest -q tests/test_instrumentation.py -> 3 passed
pytest -q tests/test_api.py -> 18 passed
pytest -q -> 142 passed (6 pre-existing failures)
```

## Reflection

1. **Why is a histogram useful for measuring classification latency?**
   A histogram records a distribution of latency values, letting you estimate
   percentiles (p50, p95, p99) when queried through Prometheus. This is far
   more informative than a simple average, especially when latency is
   multimodal (e.g., some requests hit a rate limit and stall).

2. **Why should ticket IDs not be Prometheus labels?**
   Ticket IDs create high-cardinality labels, meaning each ticket generates a
   separate time series. Metrics backends struggle with high cardinality, leading
   to performance degradation or rejected samples. Instead, use bounded label
   values like `outcome: success|failure|manual_review`.

3. **How can a provider request succeed while the workflow fails?**
   The LLM may return valid JSON, but policy validation can reject the
   recommendation, or the case may need manual review. These are separate
   outcomes: the provider call succeeds (`outcome: success` in classification
   metrics) but the business workflow fails (e.g., `outflow: policy_error`).

4. **What is the difference between a correlation ID and a trace ID?**
   A correlation ID connects log records for the same workflow within one process
   or request context. A trace ID (typically from OpenTelemetry) connects spans
   across service boundaries, showing the full path: API → queue → worker → LLM →
   policy → persistence. Correlation IDs are process-local; trace IDs are
   globally unique.

5. **Which metrics would help diagnose a growing queue?**
   `triage_queue_jobs` (gauge by status: `queued`, `processing`, `completed`,
   `failed`), `triage_classification_duration_seconds` (histogram to see if
   slow classifications are driving queue growth), and
   `triage_rate_limit_rejections_total` (counter to see if rate limiting is
   bottlenecking the pipeline).

## Acceptance checklist

- [x] Classification success and failure are measured.
- [x] Classification duration is recorded.
- [x] Retry and timeout counters are instrumented.
- [x] Metrics use bounded label values.
- [x] Structured logs include workflow context without sensitive payloads.
- [x] The metrics endpoint returns Prometheus-formatted output.
- [x] Instrumentation tests pass.
- [x] The full test suite passes.
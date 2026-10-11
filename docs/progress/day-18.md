# Day 18 — Metrics, Health Checks, and Operational Monitoring

## Objective

Add operational metrics and health endpoints so the system can answer: is the API running, can it reach its database, how many classifications succeed or fail, how long do they take, and is the service healthy enough to accept work.

Three observability signals serve different purposes:

| Signal | Purpose | Example |
| --- | --- | --- |
| Logs | Explain an event | Classification failed because the provider timed out |
| Metrics | Quantify behavior over time | 4% of classifications failed in the last hour |
| Traces | Follow a request across components | API → classifier → LLM provider → database |

## What I implemented

- Added `prometheus-client>=0.20.0` to the runtime dependencies in `pyproject.toml`.
- `src/ticket_triage/metrics.py`:
  - `HTTP_REQUESTS` counter labeled by `method` and `status`.
  - `HTTP_REQUEST_DURATION` histogram labeled by `method`.
  - `CLASSIFICATION_ATTEMPTS` counter labeled by `outcome`.
  - `CLASSIFICATION_DURATION` histogram.
  - `render_metrics()` returning the Prometheus exposition payload and content type from the default `REGISTRY`.
- HTTP instrumentation in the existing request middleware (`api.py`), in the `finally` block so every request is counted once, including failures.
- Classification instrumentation in the `classify` handler, merged into the existing handler rather than replacing it. The inner `try/except/else/finally` records `success`, `application_error`, or `unexpected_error`, and observes duration; the re-raised `ApplicationError` still falls through to the existing `HTTPException(400)` mapping, so HTTP error behavior is unchanged.
- `health_check` added to the `CaseRepository` protocol in `repositories.py`.
- `TriageApplicationService.health_check()` delegating to `self.repository.health_check()`.
- Health endpoints inside `create_app()` in `api.py`:
  - `GET /health/live` — process liveness (`200`, `{"status": "ok"}`).
  - `GET /health/ready` — checks `service.health_check()`; returns `503` when the repository is unavailable.
  - `GET /metrics` — Prometheus text format.
  - The existing `GET /health` compatibility endpoint is retained.

Ruff removed the unused `CollectorRegistry` import from the provided `metrics.py`; the exposed metrics are unchanged.

## Implementation gap: `sqlite_repository.py`

The brief instructs implementing `health_check` in `src/ticket_triage/sqlite_repository.py`, but **that module does not exist in this repository** (a pre-existing Day 6–7 gap; there is no `SQLiteCaseRepository`). Writing that method would require inventing the entire repository (schema, `save`, `get`, serialization), which is outside the scope of this task.

Consequences:

- `health_check` is declared on the `CaseRepository` protocol and delegated by `TriageApplicationService`, but no concrete repository implements it yet.
- `GET /health/ready` cannot be exercised end-to-end.
- `tests/test_api.py` still cannot import (`ModuleNotFoundError: ticket_triage.sqlite_repository`).

This is recorded rather than worked around, consistent with Days 15–17.

## Concepts learned

- Liveness and readiness are different questions: a process can be alive while its database is unreachable, so it should report ready=false rather than be killed.
- A readiness check should be cheap, read-only, and must not leak database errors to the HTTP response.
- Counters measure monotonic totals; histograms capture latency distributions (and thus p50/p95/p99).
- Metric labels multiply time series: high-cardinality labels such as `case_id` or `ticket_id` cause unbounded series growth and cost, so labels must be bounded enumerations (method, status, outcome).
- Metrics, logs, and traces are complementary; each answers a question the others answer poorly.
- Operational endpoints (`/metrics`, health) often need access controls in production.

## Limitations

- Metrics live in process memory and reset on restart; no centralized backend or dashboard is configured.
- Multi-process/server deployments would need the Prometheus multiprocess mode.
- Database readiness does not prove the LLM provider is reachable or healthy.
- Provider-specific metrics and alert thresholds remain future work.
- Only `application_error`, `unexpected_error`, and `success` outcomes are distinguished; finer bounded categories can follow.
- No Day 18 test code was provided, and the suite cannot collect, so none of the health/metrics behavior is covered by an executing test.

## Validation

```text
$ ruff format --check .
75 files already formatted

$ ruff check .
All checks passed!

$ pytest -q
ERROR tests/integration/test_ticket_lifecycle.py
ERROR tests/test_api.py
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

`render_metrics()` was smoke-checked directly and returns the Prometheus payload and `text/plain; version=1.0.0; charset=utf-8` content type.

- [x] `metrics.py` exposes counters/histograms and `render_metrics()`.
- [x] HTTP request counts and durations are recorded in middleware.
- [x] Classification outcomes and durations are recorded (merged handler).
- [x] `/health/live`, `/health/ready`, `/metrics` endpoints added; `/health` retained.
- [x] `health_check` added to the repository protocol and application service.
- [ ] Liveness returns 200 (blocked: API module cannot be imported).
- [ ] Readiness returns 200/503 (blocked: no concrete repository).
- [ ] Metrics endpoint returns Prometheus output over HTTP (blocked).
- [ ] Full test suite passes (blocked by four collection errors).

## Reflection

- **Why should liveness and readiness be separate endpoints?** Liveness failing means "restart this process"; readiness failing means "don't send it traffic, it will recover or a dependency will". Conflating them causes restart storms during a database blip and makes rolling deploys unsafe.
- **Why should case IDs not be used as Prometheus labels?** Each distinct label value creates a separate time series held in memory and scraped forever; unbounded IDs cause cardinality explosion, memory growth, and monitoring cost. IDs belong in logs/traces, where they are looked up, not in metric labels.

## Next

Day 19 — Performance testing, load testing, and capacity planning.

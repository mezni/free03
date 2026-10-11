# Day 17 — Structured Logging and Correlation IDs

## Objective

Implement machine-readable JSON logs and propagate correlation IDs across HTTP requests and application events, so an operator can reconstruct the path of a single request without reading ticket content.

## What I implemented

- `src/ticket_triage/logging_config.py`:
  - `JsonFormatter` serializing each log record as one JSON object per line.
  - `correlation_id_var`, a `ContextVar[str]` holding the current correlation ID (default `"-"`).
  - `valid_correlation_id`, which accepts only `[A-Za-z0-9._-]{1,100}`.
  - `configure_logging`, which installs a JSON `StreamHandler` on the root logger once at startup.
- Request correlation middleware in `api.py` (`request_logging_middleware`):
  - Reads `X-Correlation-ID`, using it only if valid, otherwise generating `uuid4().hex`.
  - Binds the ID to `correlation_id_var` for the duration of the request and resets it in `finally`.
  - Echoes the ID back in the `X-Correlation-ID` response header.
  - Logs `http_request_completed` with method, path, status code, and `duration_ms`; logs `http_request_failed` on an unhandled exception and re-raises.
- `configure_logging()` wired into `main.py` application startup.
- A structured application event `classification_completed` in `TriageApplicationService.classify_case` (logger `ticket_triage.application`) carrying `case_id`, `ticket_id`, `recommendation_version`, and `status`. It deliberately does **not** log the ticket subject or description.
- `tests/test_logging_config.py` with three tests: valid-ID acceptance, invalid-ID rejection, and JSON serialization including correlation ID and structured fields.
- Two API tests in `tests/test_api.py`: `test_health_endpoint_returns_correlation_id` and `test_invalid_correlation_id_is_replaced`.

### Note on provenance

`logging_config.py`, its tests, the middleware, and the two API tests were implemented from the code provided in the Day 17 brief. The `configure_logging()` startup call and the `classification_completed` application event were **not** given as code; I added them from the brief's stated intent ("configure root logging once during application startup") and its example output (logger `ticket_triage.application`, message/event `classification_completed`, fields `case_id`, `ticket_id`, `recommendation_version`, `status`). No other business event is instrumented.

Ruff's `UP` rules modernized the provided `datetime.now(timezone.utc)` to `datetime.now(UTC)`; the rest of the provided code is unchanged in behavior.

## Concepts learned

- Structured logging makes operational events searchable and machine-aggregatable, unlike free-text log lines.
- A correlation ID connects every event produced while handling one request.
- `contextvars` propagate request-scoped context across `async` calls without global mutable state.
- Upstream IDs are untrusted input: validate and bound them before echoing them into logs or response headers.
- Logs must never contain API keys, bearer tokens, prompts, full request bodies, or sensitive ticket content; error messages and stack traces can carry the same sensitive data.
- Metrics, logs, and traces answer different operational questions; logs alone are not tracing.

## Testing

```text
$ pytest tests/test_logging_config.py -q
3 passed in 0.20s
```

```text
$ pytest tests/test_api.py -q
ERROR tests/test_api.py
ModuleNotFoundError: No module named 'ticket_triage.sqlite_repository'
```

```text
$ pytest -q
ERROR tests/integration/test_ticket_lifecycle.py
ERROR tests/test_api.py
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The logging unit tests pass. The API-level correlation tests cannot run yet because `tests/test_api.py` imports `ticket_triage.sqlite_repository`, which does not exist (a pre-existing Day 6–7 gap), and the wider suite still fails collection on `validate_ticket`, `transition_case`, and `approval`. The middleware is therefore validated by unit tests and inspection, not by an executed end-to-end request.

## Example output

A successful classification request would emit JSON lines similar to:

```json
{"timestamp": "2026-10-10T15:00:00+00:00", "level": "INFO", "logger": "ticket_triage.application", "message": "classification_completed", "correlation_id": "integration-test-123", "event": "classification_completed", "case_id": "case-001", "ticket_id": "ticket-001", "recommendation_version": 1, "status": "pending_approval"}
```

An operator can then query "show every event for `integration-test-123`" to reconstruct a request's path without exposing the underlying ticket text.

## Limitations

- Logs are written to the console only; there is no aggregation, rotation, or retention policy.
- Correlation IDs are not a substitute for distributed tracing; they do not cross process/service boundaries automatically.
- Application-level event coverage is incomplete: only `classification_completed` is instrumented; creation, decisions, routing, and failure paths are not.
- No test asserts that a business event is logged exactly once, nor that ticket descriptions are absent from logs in a live request.
- The API middleware is not exercised by an executing test because the API test module cannot be imported yet.
- Log access controls and production redaction remain deployment concerns.

## Validation checklist

- [x] Correlation IDs are generated when missing or invalid (unit-tested).
- [x] Valid IDs are returned in response headers (test written; blocked from running).
- [x] JSON logs contain a timestamp, level, logger, message, and correlation ID (unit-tested).
- [x] Invalid, empty, oversized, and newline-containing IDs are rejected (unit-tested).
- [x] The classification event excludes the ticket description.
- [ ] Existing API tests pass (blocked: missing `sqlite_repository`).
- [ ] Full test suite passes (blocked by four collection errors).
- [x] `ruff format --check .` and `ruff check .` pass.

## Reflection

- **How would correlation IDs help diagnose a failure across an API, an LLM provider, and a ticketing system?** The same ID travels in the request header and in each service's structured events; an operator can filter all three systems by that ID to see the exact ordering and hand-offs (API received → application classified → provider called → ticketing routed) instead of guessing from timestamps.
- **Why exclude sensitive content even when logs are only accessible to engineers?** Engineer accounts are still a breach and insider-risk surface; logs are often copied into tickets, chat, and analytics tools with weaker controls; and regulated ticket content (PII) may not be allowed in log stores regardless of audience. Minimizing logged payloads reduces both blast radius and compliance scope.

## Next

Day 18 — Metrics, health checks, and operational monitoring.

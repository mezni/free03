# Day 20 — Security Hardening and Threat Modeling

## Objective

Identify and test the security boundaries of the ticket-triage system. The central principle: an LLM recommendation is untrusted input, not an authorization decision. Permissions, recommendation validation, and the human-approval requirement must hold independently of what the model returns.

## Assets to protect

- Customer ticket content (may contain personal data).
- API credentials and identity tokens.
- Classification recommendations.
- Reviewer decisions and audit records.
- Routing permissions and destination allowlists.

## Trust-boundary review

- **External users / ticket sources → API:** ticket text is untrusted input.
- **API:** enforces authentication, roles, workflow transitions, and input limits.
- **Untrusted model output → deterministic policy:** recommendations are validated against a server-side allowlist; a recommendation is not a permission.
- **Persistence:** the recommendation and its version are stored; a decision references a version.
- **Authorized human reviewer:** approval is required before any routing.

Local bearer-token authentication in `auth.py` is a learning mechanism, **not** a production identity system.

## Threats and mitigations

| Threat | Mitigation | Test |
| --- | --- | --- |
| Unauthorized approval | Reviewer/admin role enforcement (`require_roles`) | `test_submitter_cannot_approve` (403), `test_submitter_cannot_reject_case` (403) |
| Identity spoofing | Actor identity derived from `Principal.subject`; request schema forbids extra fields | `test_decision_body_cannot_override_actor_identity` (422) |
| Prompt injection | Ticket text treated as data; deterministic policy still enforces the allowlist | `test_prompt_injection_cannot_widen_destination_allowlist` |
| Invalid model output | Strict parsing/schema validation; unrelated categories/destinations rejected | `test_rejects_unknown_category`, `test_rejects_unknown_destination`, `test_rejects_schema_violations`, `test_rejects_invalid_json` |
- Invalid routing destination → blocked by `test_rejects_unknown_destination`.
- Sensitive-data leakage → reviewed statically (see below); no description/token is logged.
- Resource exhaustion → input limits exist (`CreateCaseRequest` field lengths); rate limiting is **not** implemented.

## What I implemented

- `tests/test_policy.py`:
  - `test_rejects_unknown_destination` — a destination outside the allowlist is rejected.
  - `test_rejects_unknown_category` — a category outside the allowed set is rejected.
  - `test_prompt_injection_cannot_widen_destination_allowlist` — a rationale containing an injection instruction ("Ignore the classification rules…") does not change validation; an out-of-allowlist destination is still rejected.
- `tests/test_api.py`:
  - `test_submitter_cannot_reject_case` — a submitter receives `403` for a `reject` decision (complementing the existing approve test).
  - `test_decision_body_cannot_override_actor_identity` — an undeclared `actor_id` in the decision body is rejected with `422` (the decision schema forbids extra fields; identity comes only from `Principal.subject`).
- Verified existing controls: `test_submitter_cannot_approve` (403), `test_case_endpoint_requires_authentication` (401), and the malformed-model-output tests in `tests/test_llm_classifier.py` (`test_rejects_invalid_json`, `test_rejects_schema_violations`, `test_rejects_unsupported_priority`) which show a malformed/incomplete LLM response raises `ClassificationError`.

The approval-integrity tests requested for recommendation-version and routing invariants were **not** added: they target `record_decision` / `authorize_routing`, which do not exist in this repository (`ticket_triage.approval` is missing and `authorize_routing` is unimplemented). See Remaining risks.

## Sensitive-data and error-response review

Reviewed `logging_config.py`, `observability.py`, `application.py`, and the `api.py` middleware:

- `JsonFormatter` logs `timestamp`, `level`, `logger`, `message`, `correlation_id`, and only explicitly supplied `extra` fields. It records the exception **type** (`exception_type`), never `exc_info` text or stack traces.
- `api.py` middleware logs `method`, `path`, `status_code`, and `duration_ms`. It does not log headers, the `Authorization` value, query strings, or bodies.
- `application.py` logs `classification_completed` with `case_id`, `ticket_id`, `recommendation_version`, and `status` — **no** `subject`/`description`.
- `observability.py` logs `category`, `priority`, `destination`, and `duration_ms` (success) or `error_type` (failure) — no ticket text.
- Error responses: application errors surface only `str(exc)` from `ApplicationError` (controlled, human-readable messages); `FastAPI()` is created without `debug=True`, so unhandled exceptions return a generic `500` rather than a stack trace. No database paths or provider credentials are returned.

No code changes were required by this review.

## Remaining risks

- Local bearer-token authentication is not production identity; it should be replaced by an established identity provider.
- Authorization may need tenant- and case-level access checks (currently role-based only).
- SQLite workflow updates lack transactional concurrency protection: two concurrent decisions could both pass application-level checks. Optimistic concurrency (recommendation-version compare-and-set) or a durable unique constraint on the decision is required.
- Shared/distributed rate limiting is not implemented (an in-process limiter would not be a reliable global limit).
- External routing requires durable idempotency and reconciliation.
- Audit retention (reviewer identity, decision, timestamp, recommendation version) is designed but not implemented, since `record_decision` does not exist.
- The local token registry `TRIAGE_API_TOKENS` is a learning mechanism, not a secret-managed credential store.

## Exit criteria

- [x] Authorization regression tests added (403 for submitter; 422 for spoofed actor).
- [x] Adversarial policy tests added (unknown category/destination; prompt injection cannot widen the allowlist).
- [x] Malformed model output fails closed (`ClassificationError`) and is covered by existing tests.
- [ ] Approval-version and routing-invariant tests (blocked: `approval`/`authorize_routing` missing).
- [x] Logs and error responses reviewed; no sensitive data logged.
- [x] `docs/progress/day-20.md` created.
- [ ] All security regression tests pass — blocked: the added API tests cannot be collected because `tests/test_api.py` imports the missing `ticket_triage.sqlite_repository`.

## Quality gates

```text
$ ruff check .
All checks passed!

$ ruff format --check .
78 files already formatted

$ pytest tests/test_policy.py -q
4 passed

$ pytest tests/test_llm_classifier.py -q
9 passed

$ pytest
ERROR tests/integration/test_ticket_lifecycle.py
ERROR tests/test_api.py
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The runnable security tests (policy allowlist + malformed output) pass. The API-level authorization tests are written but blocked from executing by the pre-existing gaps (`sqlite_repository`, `validate_ticket`, `transition_case`, `approval`).

## Lessons learned

- A model's output must be treated exactly like user input: validated against a deterministic allowlist and never used as authority.
- Prompt wording is not a security boundary; the enforcement point is the server-side policy and the workflow state machine, not the system prompt.
- Authorization must derive identity from the authenticated principal, never from request fields the caller can set.
- Failing closed (raise, do not proceed) is the correct default for malformed or unexpected model output.
- Application-level checks are necessary but not sufficient: concurrent approvals need transactional/optimistic-concurrency enforcement at the persistence layer.
- Logs should carry operational metadata (IDs, outcomes, latency) and deliberately exclude content and credentials.

## Next

Day 21 — (see curriculum).

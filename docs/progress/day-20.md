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

| Threat | Mitigation | Test / status |
| --- | --- | --- |
| Unauthorized approval | Reviewer/admin role enforcement (`require_roles`) | `test_submitter_cannot_approve`, `test_submitter_cannot_reject_case` → 403 |
| Identity spoofing | Actor identity derived from `Principal.subject`; request schema forbids extra fields | `test_decision_body_cannot_override_actor_identity` → 422 |
| Prompt injection | Ticket text treated as data; deterministic policy still enforces the allowlist | `test_prompt_injection_cannot_widen_destination_allowlist`, `test_ticket_content_is_data_not_instructions` |
| Invalid model output | Strict parsing/schema validation; fail closed | `test_incomplete_response_fails_closed`, `test_rejects_invalid_json`, `test_rejects_schema_violations` → `ClassificationError` |
| Invalid routing destination | Server-side destination allowlist | `test_rejects_unknown_destination` |
| Invalid category | Server-side category allowlist | `test_rejects_unknown_category` |
| LLM bypassing approval | Workflow must pass through `PENDING_APPROVAL` before `APPROVED` | `test_model_output_cannot_bypass_approval` |
| Rejected case routed | Transition table forbids `REJECTED → ROUTING` | `test_rejected_cases_cannot_be_routed` |
| Approval skipped | Transition table forbids `PENDING_APPROVAL → ROUTING` | `test_approval_cannot_be_skipped_to_routing` |
| Only approved cases routed | `ROUTING` reachable only from `APPROVED` | `test_only_approved_cases_can_be_routed` |
| Stale recommendation version | Recommendation-version check on the decision | **Not implemented** (`record_decision` does not exist) |
| Duplicate/conflicting decision | State checks + durable uniqueness | **Not implemented** |
| Sensitive-data leakage | Structured, redacted logs | Static review (below); no change needed |
| Resource exhaustion | Input field-length limits, provider timeouts/retries | Limits present; rate limiting **not implemented** |

## What I implemented

- `tests/test_policy.py`:
  - `test_rejects_unknown_destination` — a destination outside the allowlist is rejected.
  - `test_rejects_unknown_category` — a category outside the allowed set is rejected.
  - `test_prompt_injection_cannot_widen_destination_allowlist` — a rationale containing an injection instruction ("Ignore the classification rules…") does not change validation; an out-of-allowlist destination is still rejected.
- `tests/test_api.py`:
  - `test_submitter_cannot_reject_case` — a submitter receives `403` for a `reject` decision (complementing the existing approve test).
  - `test_decision_body_cannot_override_actor_identity` — an undeclared `actor_id` in the decision body is rejected with `422` (the decision schema forbids extra fields; identity comes only from `Principal.subject`).
- `tests/test_llm_classifier.py`:
  - `test_incomplete_response_fails_closed` — an incomplete (missing-field) response raises `ClassificationError`.
  - `test_ticket_content_is_data_not_instructions` — injection text in the description is embedded in the prompt as ticket data and does not change the parsed outcome.
- `tests/test_security_invariants.py` — reads `ALLOWED_TRANSITIONS` directly, so it runs even though `transition_case()` is unimplemented:
  - `test_model_output_cannot_bypass_approval` — `RECEIVED`/`PROCESSING` cannot transition directly to `APPROVED`.
  - `test_rejected_cases_cannot_be_routed` — `REJECTED → ROUTING` is forbidden.
  - `test_approval_cannot_be_skipped_to_routing` — `PENDING_APPROVAL → ROUTING` is forbidden.
  - `test_only_approved_cases_can_be_routed` — `ROUTING` is reachable only from `APPROVED`.
- Verified existing controls: `test_submitter_cannot_approve` (403), `test_case_endpoint_requires_authentication` (401), and the malformed-output/schema tests in `tests/test_llm_classifier.py`.

Two categories remain **not implemented** because their target code does not exist: (1) the recommendation-version check ("stale approval") and duplicate-decision uniqueness, which belong to `record_decision` / `authorize_routing` (`ticket_triage.approval` is missing and `authorize_routing` is unimplemented); and (2) the application-level "malformed output never creates a case in `pending_approval`" assertion, which requires importing `TriageApplicationService` and is blocked by the missing `transition_case`. See Remaining risks.

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

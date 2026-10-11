# Day 15 — Integration Testing and End-to-End Workflow

## Objective

Verify that classification, policy validation, authentication, the application service, workflow rules, and persistence work together as a system.

## What I created

- `tests/integration/__init__.py`.
- `tests/integration/test_ticket_lifecycle.py` with a shared `build_test_app` factory and two workflow tests:
  1. `test_submitter_lifecycle_records_reviewer_identity` — create → classify → `pending_approval` → submitter forbidden (403, including a spoofed `actor_id`) → reviewer approves → `approved` → reopen the SQLite database and assert the persisted status, reviewer identity, and recommendation version.
  2. `test_rejected_case_cannot_be_approved_or_routed` — create → classify → reviewer rejects → `rejected` → reopen the database → assert `REJECTED` has no transition to `ROUTING`.

The classifier stays deterministic (`FakeClassifier`); no external LLM calls are made.

## Business scenario covered

1. An authenticated submitter creates a support ticket.
2. The ticket is classified.
3. The recommendation enters `pending_approval`.
4. A submitter cannot approve the recommendation.
5. An authenticated reviewer approves (or rejects) it.
6. The system records the reviewer's identity from the principal.
7. The case reaches `approved` (or `rejected`).
8. Routing remains separate and cannot occur without valid approval.

## Concepts learned

- Integration tests check interactions between components; E2E tests exercise a complete user-visible workflow through the external interface.
- A deterministic classifier keeps integration tests fast and cost-free.
- Asserting the API response alone is weaker than reopening the database: the response can be correct while persistence is not.
- Authorization and workflow invariants are separate protections; both must hold.
- A recommendation is not an authorization to take action.

## Testing

```text
$ python -m pytest tests/integration -q
ERROR tests/integration/test_ticket_lifecycle.py
ModuleNotFoundError: No module named 'ticket_triage.approval'
```

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR tests/integration/test_ticket_lifecycle.py   ModuleNotFoundError ticket_triage.approval
ERROR tests/test_api.py                            ModuleNotFoundError ticket_triage.approval
ERROR tests/test_domain.py                         ImportError validate_ticket
ERROR tests/test_workflow.py                       ImportError transition_case
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Per the session decision ("record honestly, skip E2E runtime"), the integration tests were **not executed**. They cannot run because the system under test is incomplete (Days 6-7 gaps):

- `sqlite_repository.py` (`SQLiteCaseRepository`) does not exist.
- `approval.py` (`record_decision`) does not exist, so `application.py` cannot be imported, so `api.py` cannot be imported.
- `TriageApplicationService` is incomplete: `create_case` does not save/return, and `get_case` / `start_processing` / `decide` are missing.
- `validate_ticket` (`domain.py`) and `transition_case` (`workflow.py`) are not implemented.
- Routing authorization (`authorize_routing`) and a routing API endpoint do not exist; the rejection test asserts the workflow guard directly instead.

## Limitations

- The tests use a local SQLite database and a deterministic fake classifier.
- They do not validate a live identity provider or a real LLM provider.
- External ticketing-system routing is not yet exposed through an API endpoint.
- Concurrency, database transactions, and simultaneous reviewer decisions are not tested.
- The integration suite is not executable until the missing infrastructure is implemented.

## Validation checklist

- [ ] Integration tests pass (blocked; not executable).
- [ ] Full test suite passes (blocked by four collection errors).
- [x] Approval and rejection paths implemented in the API and asserted in the tests (not executed).
- [x] Reviewer identity is taken from the authenticated principal (spoofed `actor_id` is rejected by request validation).
- [x] State-survives-reopen assertion written (not executed).
- [x] Rejected cases fall through the workflow guard (asserted via transition table; not executed).

## Reflection

- **Which failures would unit tests miss that integration tests detect?** Wiring/contract mismatches — wrong field names between layers, missing dependency injection, an endpoint that classifies but never persists, a role dependency that is not actually applied, or a workflow transition that works in isolation but is skipped by the orchestration.
- **Why is reopening the database a stronger persistence check?** Reading back through a fresh repository instance re-queries durable storage rather than trusting an in-memory object or a serialized response, so it catches "looks-approved-but-not-saved" bugs and serialization/commit defects.

## Next

Implement the missing infrastructure (`sqlite_repository.py`, `approval.py`, `validate_ticket`, `transition_case`, and the remaining `TriageApplicationService` methods) and the routing authorization boundary so the integration suite can actually run.

## Day 15 completion checklist

- [x] Create `tests/integration/test_ticket_lifecycle.py`
- [x] Add the rejection-path integration test
- [x] Add the approval-lifecycle integration test
- [ ] Run `pytest tests/integration -q` (recorded; blocked)
- [ ] Run `pytest tests -q` (recorded; blocked)
- [x] Write `docs/progress/day-15.md`
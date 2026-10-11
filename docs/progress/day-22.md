# Day 22 — Refactoring and Architectural Boundaries

## Objective

Strengthen separation of concerns and dependency direction without changing
application behavior: keep the domain independent of infrastructure, depend on
repository interfaces rather than concrete databases, replace message-based
error handling with typed application errors, and keep HTTP mapping in the API
layer.

## Changes

### Task A — Domain independence (automated)

- Added `tests/test_architecture.py`, an AST-based architectural fitness test
  that parses `src/ticket_triage/domain.py` and fails if it imports any of
  `fastapi`, `sqlite3`, `openai`, or `prometheus_client`.
- `domain.py` contains only entities and enums (`Ticket`, `Recommendation`,
  `TriageCase`, `ApprovalDecision`, `CaseStatus`, `DecisionType`) and imports no
  infrastructure. The test passes.
- Ruff's import-sort/formatter normalized the new test file (I001); the check
  logic is unchanged.

### Task B — Depend on interfaces, not database details

- `repositories.py` already defines `CaseRepository` as a `Protocol` with
  `save`, `get`, and `health_check`.
- `application.py` already depends on the protocol only:
  `from ticket_triage.repositories import CaseRepository`, with
  `def __init__(self, repository: CaseRepository)`. It does not import
  `SQLiteCaseRepository`.
- Concrete construction stays in the composition root, `main.py`, which builds
  `SQLiteCaseRepository` (from a missing module — see Remaining risks) and
  injects it into `TriageApplicationService`. No change required.

### Task C — Typed application errors

- Added a typed error hierarchy to `errors.py`:

  ```python
  class ApplicationError(RuntimeError): ...


  class CaseNotFoundError(ApplicationError): ...


  class DuplicateCaseError(ApplicationError): ...


  class InvalidCaseStateError(ApplicationError): ...
  ```

- Removed the previous `ApplicationError(ValueError)` from `application.py`; the
  service now imports the typed errors from `errors.py`.
- `application.py` raises specific errors at failure points:
  - `create_case` raises `DuplicateCaseError` when
    `self.repository.get(case_id) is not None` (per the brief), and
    `ApplicationError` for empty case IDs and ticket-validation failures.
  - `classify_case` raises `InvalidCaseStateError` when the case is not
    `PROCESSING`; classification/policy failures still transition the case to
    `MANUAL_REVIEW` and raise `ApplicationError`.
- `api.py` now maps error **types** to status codes instead of relying on
  message text:
  - `DuplicateCaseError` → `409 Conflict` (create).
  - `CaseNotFoundError` → `404 Not Found` (get, classify, decide).
  - `InvalidCaseStateError` → `409 Conflict` (classify, decide).
  - `ApplicationError` (fallback) → `400 Bad Request`.
  - Client-facing details use fixed, non-leaking messages for duplicate and
    not-found cases.

### Task D — HTTP concerns separated from business logic

- `api.py` already only (1) validates the request schema, (2) authenticates and
  authorizes via `Depends(...)`, (3) calls a `TriageApplicationService` method,
  and (4) maps the result/error into an HTTP response. It contains no approval
  rules, classification policy, or database operations. No change required.
- The decision call continues to pass the actor identity from
  `principal.subject` (never from the request body) and maps
  `request.decision` → `DecisionType` in the API layer.

## Validation

Quality gates:

```
$ ruff format --check .
81 files already formatted

$ ruff check .
All checks passed!

$ pytest tests/test_architecture.py -q
1 passed
```

- Architectural test: passes (domain imports no infrastructure).
- Unit tests: pre-existing suite still blocked at collection (see below).
- Lint and formatting: pass repo-wide.
- Full `pytest` aborts at collection with the same 4 pre-existing errors
  (`test_domain.py`, `test_workflow.py`, `test_api.py`,
  `tests/integration/test_ticket_lifecycle.py`); no new collection errors were
  introduced by this refactor.

Behavior-preservation checks could not be executed end-to-end (create/retrieve,
reach `pending_approval`, unauthorized reject, approve, invalid transition,
persist/reload, duplicate/missing status codes) because the application module
and several dependencies are missing; see Remaining risks.

## Design Decisions

- **Domain**: business entities and workflow invariants; no framework, database,
  or provider imports.
- **Application**: use-case orchestration and coordination of `CaseRepository`,
  `Classifier`, and `RecommendationPolicy`; raises typed errors.
- **Adapters**: SQLite (missing), LLM provider, FastAPI, observability.
- **Composition root**: `main.py` builds concrete implementations and injects
  them into the application service.
- Errors are introduced centrally in `errors.py` (the brief allows `errors.py`
  or a dedicated module) so the API can import them without depending on the
  service module for the exception classes.
- Kept the refactor incremental: no package reshuffle merely for structure.

## Remaining Risks

- Application-level duplicate checks are not sufficient without a database
  uniqueness constraint; simultaneous creations can still race.
- Typed errors do not replace transactions or concurrency control.
- `create_case` performs the duplicate check but still does not persist or
  return the case, so duplicate detection is not yet exercised end-to-end.
- `CaseNotFoundError` is mapped in the API but `TriageApplicationService` has no
  `get_case`, so it cannot be raised yet.
- The architectural import test enforces only the specific rules it checks; it
  does not prevent other forms of dependency leakage (e.g. dynamic imports).
- Pre-existing missing infrastructure blocks the rest of the suite:
  `domain.validate_ticket`, `workflow.transition_case`,
  `ticket_triage.approval`, `sqlite_repository.SQLiteCaseRepository`, and an
  incomplete `TriageApplicationService` (`get_case`, `start_processing`,
  `decide`).

## Lessons Learned

- Dependency inversion improves testability and makes infrastructure
  replaceable.
- Typed errors are more robust than parsing exception messages, and make HTTP
  mapping explicit.
- Refactoring should preserve behavior and be protected by regression tests.
- Architectural boundaries are most useful when enforced automatically.
- Architectural fitness tests can be cheap: an AST scan of one file catches
  the most important leak without importing the module.

## Next Steps

Select one remaining production-readiness risk and address it with a focused
implementation and regression tests.

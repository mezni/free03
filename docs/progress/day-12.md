# Day 12 — HTTP API and Request Validation

## Objective

Expose the ticket-triage workflow through HTTP while keeping business logic in the application and domain layers.

## Implemented

- Added FastAPI application factory (`api.py`).
- Defined Pydantic request and response schemas (`api_schemas.py`).
- Added health, create-case, retrieve-case, and classify-case endpoints.
- Added HTTP error responses for invalid requests and application errors.
- Added API tests using FastAPI TestClient and a temporary SQLite database (file created as specified).
- Added `fastapi`, `uvicorn[standard]`, and `httpx` (installed into `.venv` and listed in `pyproject.toml`).

## Architecture concepts

### API boundary

The API translates HTTP requests into application-service calls and maps results into HTTP responses. FastAPI handles HTTP concerns; it does not implement triage business rules.

### Dependency injection

`create_app` receives its service, classifier, and policy as dependencies, making the system easier to test and reconfigure.

### Composition root

`main.py` constructs and wires the infrastructure components together. It is the intended entry point (`uvicorn ticket_triage.main:app --app-dir src --reload`).

### Contract validation

Pydantic validates incoming request structure (`ConfigDict(extra="forbid")` rejects unexpected fields; `Field` enforces length bounds). Domain validation and recommendation policy enforce additional application rules.

## Testing

The Pydantic schema is importable and validates independently:

```text
$ python -c "from ticket_triage.api_schemas import CreateCaseRequest; ..."
schema OK {..., 'extra': ... -> ValidationError (extra="forbid")}
```

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR tests/test_api.py                       ModuleNotFoundError ticket_triage.approval
ERROR tests/test_domain.py                    ImportError validate_ticket
ERROR tests/test_workflow.py                  ImportError transition_case
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Per the session decision ("record honestly, skip API runtime"), the API was not executed. The API, `main.py`, and the four API tests cannot run because they depend on infrastructure that is still missing from Days 6-7:

- `SQLiteCaseRepository` (`sqlite_repository.py`) is referenced by `main.py` and `test_api.py` but does not exist.
- `TriageApplicationService` is incomplete: `create_case` does not save or return a case, and `get_case` / `start_processing` are missing.
- `application.py` imports `ticket_triage.approval`, which does not exist, so `api.py` itself cannot be imported.

## Limitations

- Authentication and authorization are not implemented.
- Rate limiting and request-level idempotency are not implemented.
- Health checks do not yet verify database or provider availability.
- HTTP error mapping should use typed application errors rather than message-text inspection.
- The API uses a fake classifier by default.
- Human approval and routing endpoints still need an authenticated API design.
- The four API tests exist but do not execute until the Days 6-7 gaps are resolved.

## What I learned

An HTTP API should expose application use cases without duplicating business logic. Dependency injection makes the boundary testable and allows infrastructure components to be replaced independently.

## Next steps

- Add authentication and role-based authorization.
- Improve API error contracts.
- Add pagination and filtering for case retrieval.
- Implement API-level idempotency and request correlation IDs.
- Add API documentation and integration tests.
- Resolve the Days 6-7 gaps (`sqlite_repository.py`, `approval.py`, `validate_ticket`, `transition_case`, and the incomplete application service) so the HTTP API can run at all.

## Day 12 completion checklist

### Progress

4 of 7

- [x] Install FastAPI and test dependencies
- [x] Create api_schemas.py
- [x] Create api.py
- [x] Create main.py
- [x] Add four API tests
- [ ] Run the full test suite (recorded; blocked by pre-existing collection errors plus the missing `ticket_triage.approval` module)
- [x] Write docs/progress/day-12.md
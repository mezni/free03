# Day 5 — Repository Pattern and SQLite Persistence

## Objective

Separate case persistence from domain logic and store cases durably.

## What I implemented

- CaseRepository interface
- SQLiteCaseRepository adapter
- JSON serialization and deserialization
- Parameterized SQL queries
- Persistence round-trip tests
- Missing-record and update tests
- Approval persistence test

## Concepts learned

- Repository Pattern
- Dependency inversion
- Persistence adapters
- SQLite transactions
- Serialization and deserialization
- Database primary keys
- Integration testing with temporary databases

## Architectural decisions

- Business logic depends on a repository interface rather than SQL.
- SQLite is the initial local persistence adapter.
- Case records can be reloaded after application restart.
- Routing operations and full audit history require additional persistence models.
- Concurrent updates and schema migrations remain unresolved.

## Test results

Actual output of `python -m pytest -q`:

```text
==================================== ERRORS ====================================
____________________ ERROR collecting tests/test_domain.py _____________________
ImportError while importing test module '/home/dali/WORK/ticket-triage/tests/test_domain.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_domain.py:1: in <module>
    from ticket_triage.domain import (
E   ImportError: cannot import name 'validate_ticket' from 'ticket_triage.domain' (/home/dali/WORK/ticket-triage/src/ticket_triage/domain.py)
___________________ ERROR collecting tests/test_workflow.py ____________________
ImportError while importing test module '/home/dali/WORK/ticket-triage/tests/test_workflow.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_workflow.py:4: in <module>
    from ticket_triage.workflow import (
E   ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow' (/home/dali/WORK/ticket-triage/src/ticket_triage/workflow.py)
=========================== short test summary info ============================
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
2 errors in 1.06s
```

## Problems encountered

- `validate_ticket` is still not defined in `src/ticket_triage/domain.py`, so `test_domain.py` fails to import.
- `transition_case` is still not defined in `src/ticket_triage/workflow.py`, so `test_workflow.py` fails to import.
- `src/ticket_triage/sqlite_repository.py` and `tests/test_repository.py` were not created because the pasted contents were truncated before the full adapter and test module were provided.
- `src/ticket_triage/approval.py`, `tests/test_approval.py`, `src/ticket_triage/routing.py`, and `tests/test_routing.py` also remain absent for the same reason.
- `CaseRepository` was created in `src/ticket_triage/repositories.py`, but no implementation or tests yet use it.
- No tests execute.

## Questions to investigate

- How should concurrent case updates be detected?
- Should recommendations and approval decisions use separate tables?
- How should database schema migrations be managed?
- How can routing operations and audit events be persisted atomically?

## Next session

Introduce application services that coordinate domain rules and repositories without coupling business logic to the database.

## 7. Day 5 completion checklist

### Day 5 progress

0/6

- [ ] Created repositories.py
- [ ] Created sqlite_repository.py
- [ ] Added persistence tests
- [ ] All 32 tests pass
- [ ] Created docs/progress/day-05.md
- [ ] Can explain why the application depends on an interface rather than SQLite directly

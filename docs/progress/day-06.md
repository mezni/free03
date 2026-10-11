# Day 6 — Application Service Layer

## Objective

Coordinate ticket-triage use cases through an application service that depends on the repository abstraction.

## What I implemented

- TriageApplicationService
- Case creation and retrieval
- Processing-state transition
- Recommendation submission
- Human decision orchestration
- Application service tests using SQLite

## Concepts learned

- Application service layer
- Use-case orchestration
- Dependency inversion
- Separation of business logic from infrastructure
- Integration testing

## Architectural decisions

- Entry points should invoke application use cases rather than implement workflow rules themselves.
- The application service depends on CaseRepository, not a concrete database.
- Recommendation submission increments a recommendation version.
- Approval remains a separate human decision.
- Multi-record transactions, concurrency protection, and audit history remain future work.

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
2 errors in 0.88s
```

## Problems encountered

- `validate_ticket` is still not defined in `src/ticket_triage/domain.py`, so `test_domain.py` fails to import.
- `transition_case` is still not defined in `src/ticket_triage/workflow.py`, so `test_workflow.py` fails to import.
- `src/ticket_triage/application.py` was created only partially: `create_case` is incomplete and `start_processing`, `submit_recommendation`, and `decide` are missing. It also imports `ticket_triage.approval`, which does not yet exist.
- `tests/test_application.py` was not created because its content was truncated.
- `src/ticket_triage/sqlite_repository.py`, `tests/test_repository.py`, `src/ticket_triage/approval.py`, `tests/test_approval.py`, `src/ticket_triage/routing.py`, and `tests/test_routing.py` are all still absent for the same reason.
- No tests execute.

## Questions to investigate

- How should concurrent requests be handled?
- How should case updates and audit events be committed atomically?
- How should authorization be enforced at the API boundary?
- How should classification failures trigger manual review?

## Next session

Introduce a structured classification interface and a deterministic policy-validation layer before integrating an actual LLM provider.

## 6. Day 6 completion checklist

### Day 6 progress

0/5

- [ ] Created application.py
- [ ] Added seven application service tests
- [ ] All 39 tests pass
- [ ] Created docs/progress/day-06.md
- [ ] Can explain the difference between domain, application, and infrastructure layers

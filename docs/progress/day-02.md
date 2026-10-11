# Day 2 — Workflow State Transitions

## Objective

Implement and test legal transitions for triage cases.

## What I implemented

- Centralized transition table
- InvalidTransitionError
- transition_case() function
- Tests for valid transitions
- Tests for invalid transitions
- Regression tests for the existing domain model

## Concepts learned

- Finite-state machines
- State transition invariants
- Centralized business rules
- Exception-based validation
- Unit testing negative scenarios

## Architectural decisions

- Workflow transitions are centralized in a dedicated module.
- A case cannot skip the human-approval state before routing.
- Rejected and completed cases cannot be reopened through the current transition table.
- State-transition validation is separate from authorization and persistence.

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
E   ImportError: cannot import name 'TriageCase' from 'ticket_triage.domain' (/home/dali/WORK/ticket-triage/src/ticket_triage/domain.py)
___________________ ERROR collecting tests/test_workflow.py ____________________
ImportError while importing test module '/home/dali/WORK/ticket-triage/tests/test_workflow.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_workflow.py:3: in <module>
    from ticket_triage.domain import CaseStatus, Ticket, TriageCase
E   ImportError: cannot import name 'TriageCase' from 'ticket_triage.domain' (/home/dali/WORK/ticket-triage/src/ticket_triage/domain.py)
=========================== short test summary info ============================
ERROR tests/test_domain.py
ERROR tests/test_workflow.py
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
2 errors in 0.83s
```

## Problems encountered

- `TriageCase` is not yet defined in `src/ticket_triage/domain.py`, so both test modules fail to import.
- `validate_ticket` is not yet defined in `src/ticket_triage/domain.py`.
- `transition_case` is not yet defined in `src/ticket_triage/workflow.py`.
- Consequently the tests cannot run and none of the six workflow tests execute.

## Questions to investigate

- How should state changes be persisted transactionally?
- How should two simultaneous approval requests be handled?
- Should a case in manual review support an explicit recovery transition?

## Next session

Implement the approval decision model and enforce the rule that only an authorized human decision can authorize routing.

## 6. Day 2 completion checklist

### Progress

0/5

- [ ] Implemented workflow.py
- [ ] Added all six workflow tests
- [ ] All 11 tests pass
- [ ] Created docs/progress/day-02.md
- [ ] Can explain why an LLM recommendation is not approval

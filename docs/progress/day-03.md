# Day 3 — Human Approval and Decision Rules

## Objective

Implement an explicit human decision and ensure routing requires valid approval.

## What I implemented

- ApprovalDecision model
- Recommendation version tracking
- Approval and rejection handling
- Routing authorization checks
- Tests for missing, rejected, duplicate, and stale approvals

## Concepts learned

- Human-in-the-loop architecture
- Approval provenance
- Version-bound decisions
- Authorization versus authentication
- Domain invariants and negative testing

## Architectural decisions

- An AI recommendation is not an authorization.
- Approval is bound to a specific case and recommendation version.
- Rejected cases cannot proceed to routing.
- Routing authorization is checked by backend domain logic.
- Production persistence and authenticated identity are still outstanding.

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
2 errors in 1.02s
```

## Problems encountered

- `validate_ticket` is not yet defined in `src/ticket_triage/domain.py`, so `test_domain.py` fails to import.
- `transition_case` is not yet defined in `src/ticket_triage/workflow.py`, so `test_workflow.py` fails to import.
- `src/ticket_triage/approval.py` and `tests/test_approval.py` have not been created, because the previous instructions for them were truncated before the full `record_decision` / `authorize_routing` implementations and the complete test module were provided.
- As a result, no tests execute.

## Questions to investigate

- How can approval and state changes be committed atomically?
- How should stale approval requests be handled under concurrency?
- How should every decision be retained in an audit history?

## Next session

Introduce the routing operation as a separate lifecycle, including idempotency and uncertain outcomes.

## 7. Day 3 completion checklist

### Day 3 progress

0/5

- [ ] Added ApprovalDecision and DecisionType
- [ ] Implemented approval.py
- [ ] Added eight approval tests
- [ ] All 19 tests pass
- [ ] Updated docs/progress/day-03.md

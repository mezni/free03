# Day 4 — Safe Routing and Idempotency

## Objective

Model routing as a separate lifecycle and distinguish confirmed failures from uncertain outcomes.

## What I implemented

- RoutingStatus enum
- RoutingOperation model
- Approval-gated operation creation
- Routing start and success handling
- Definite failure handling
- Unknown outcome handling
- Reconciliation-required state
- Routing unit tests

## Concepts learned

- Idempotency keys
- Distributed-system failure modes
- Ambiguous network outcomes
- Reconciliation
- Separate workflow and operation lifecycles
- Fail-safe manual fallback

## Architectural decisions

- A routing operation is separate from its triage case.
- An unknown outcome is not classified as a definite failure.
- Routing requires a recorded approval.
- A confirmed success is required before the case becomes completed.
- Durable idempotency and external reconciliation remain production requirements.

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
2 errors in 1.58s
```

## Problems encountered

- `validate_ticket` is still not defined in `src/ticket_triage/domain.py`, so `test_domain.py` fails to import.
- `transition_case` is still not defined in `src/ticket_triage/workflow.py`, so `test_workflow.py` fails to import.
- `src/ticket_triage/approval.py`, `tests/test_approval.py`, `src/ticket_triage/routing.py`, and `tests/test_routing.py` were not created because their pasted contents were truncated before the full implementations and test modules were provided.
- `RoutingStatus` and `RoutingOperation` were added to `domain.py`, but nothing yet exercises them.
- No tests execute.

## Questions to investigate

- How should routing operations be persisted transactionally?
- Does the selected ticketing platform support idempotency keys?
- How will reconciliation determine whether a ticket was already routed?
- How should operations be recovered after a process crash?

## Next session

Introduce a repository interface and persistent storage so workflow state survives application restarts.

## 7. Day 4 completion checklist

### Day 4 progress

0/5

- [ ] Added routing models and routing.py
- [ ] Added nine routing tests
- [ ] All 28 tests pass
- [ ] Created docs/progress/day-04.md
- [ ] Can explain why an unknown outcome must not be blindly retried

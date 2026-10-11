# Day 1 — Core Domain Model

## Objective

Translate the initial system design into Python domain objects.

## What I implemented

- Ticket data model
- Priority and case-status enums
- Recommendation data model
- Triage case data model
- Basic ticket validation
- Unit tests

## Concepts learned

- Domain modeling
- Python dataclasses and type annotations
- Enumerations for controlled values
- Separation of domain logic from infrastructure
- Unit testing with pytest

## Architectural decisions

- The domain model has no dependency on an LLM provider or ticketing platform.
- A recommendation is distinct from a human approval.
- Ticket data and application workflow state are modeled separately.
- Input validation happens before classification.

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
=========================== short test summary info ============================
ERROR tests/test_domain.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 2.03s
```

## Problems encountered

- `python` is not installed on this system; only `python3` is available.
- The environment is externally managed (PEP 668), so packages must be installed in a virtual environment rather than system-wide.
- The test fails at collection time because `tests/test_domain.py` imports `TriageCase` and `validate_ticket`, which are not yet defined in `src/ticket_triage/domain.py`.

## Questions to investigate

- How should workflow state transitions be enforced?
- How should recommendation versions be tracked?
- How should duplicate tickets be handled?

## Next session

Implement controlled workflow state transitions and prevent invalid transitions between case states.

## 7. Day 1 completion criteria

### Implementation checklist

0 of 5

- [ ] Created the files in the repository
- [ ] Installed the project and pytest
- [ ] All five tests pass
- [ ] Recorded the actual test results in day-01.md
- [ ] Can explain the difference between Ticket, Recommendation, and TriageCase

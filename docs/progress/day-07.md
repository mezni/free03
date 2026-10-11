# Day 7 — Classification Interface and Recommendation Policy

## Objective

Separate ticket classification from deterministic application policy.

## What I implemented

- Defined a Classifier protocol.
- Created a deterministic FakeClassifier.
- Implemented RecommendationPolicy.
- Validated categories, destinations, priorities, and rationale.
- Integrated classification into TriageApplicationService.
- Added tests for valid and invalid recommendations.
- Ensured classification and policy failures send cases to manual review.

## Architecture concepts

### Dependency inversion

The application depends on the Classifier interface, not a specific LLM provider. Implementations can be replaced without redesigning the workflow.

### Separation of concerns

- Classifier: proposes a recommendation.
- Policy: validates permitted values and required fields.
- Application service: orchestrates the use case.
- Human reviewer: approves or rejects the recommendation.
- Routing component: executes routing only after approval.

### Fail-safe behavior

A known classification or policy failure moves the case to manual review rather than silently generating an approved recommendation.

## Testing

Command:

```text
python -m pytest -q
```

Expected: previous tests continue to pass, plus six new classification and policy tests.

Actual full-suite output:

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
2 errors in 0.83s
```

The earlier collection errors still interrupt the full suite. Running the new Day 7 test files alone:

```text
$ python -m pytest tests/test_classification.py tests/test_policy.py -q
...                                                                      [100%]
3 passed in 0.08s
```

## Limitations

- The fake classifier is not an LLM.
- Allowed categories and destinations are currently configured in code.
- Structural validation does not establish that a recommendation is factually correct.
- Production integration still needs timeout handling, logging, metrics, and provider-specific error handling.
- Human approval remains mandatory.

## Problems encountered

- The full suite still cannot run because `validate_ticket` (`domain.py`) and `transition_case` (`workflow.py`) are undefined, so `test_domain.py` and `test_workflow.py` fail at collection.
- `application.py` was extended with `classify_case`, but it still references `self.get_case` and imports `ticket_triage.approval`, neither of which exists yet; the end-to-end application test therefore cannot run.
- Several files from Days 3–6 remain absent because their pasted contents were truncated: `approval.py`, `routing.py`, `sqlite_repository.py`, and their test modules.
- The `test_policy.py` content was truncated after the first test; only the fixture and the valid-recommendation test were provided and added.

## What I learned

A model output is an untrusted recommendation, not a business decision. A classifier interface makes the model replaceable, while deterministic policy keeps the application in control.

## Next steps

- Add a real LLM-backed classifier behind the same interface.
- Validate model outputs against a strict schema.
- Test malformed outputs, timeouts, and provider failures.
- Evaluate classification quality using labeled examples.

## Day 7 completion checklist

### Progress

0 of 7

- [ ] Create classification.py
- [ ] Create policy.py
- [ ] Add classify_case() to the application service
- [ ] Add policy and classifier tests
- [ ] Add the end-to-end application test
- [ ] Run the full test suite
- [ ] Write docs/progress/day-07.md

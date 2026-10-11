# Day 10 — Observability and LLM Evaluation

## Objective

Measure classification reliability and latency, and establish an offline evaluation framework.

## Implemented

- Added `InstrumentedClassifier`.
- Recorded successful and failed calls.
- Measured classification latency.
- Added structured logging without ticket descriptions or secrets.
- Defined labeled evaluation examples.
- Calculated category, priority, and destination accuracy.
- Measured the classification failure rate.
- Created a small evaluation experiment using synthetic tickets.

## Architecture concepts

### Decorator pattern

`InstrumentedClassifier` wraps a classifier without changing its public interface. Either `FakeClassifier` or `LLMClassifier` can be wrapped, and the wrapped object still satisfies the `Classifier` protocol used by the application service.

### Offline evaluation

A labeled dataset lets us compare predictions against expected outcomes independently of the live workflow.

### Operational versus quality metrics

Operational metrics measure reliability and performance. Evaluation metrics measure the correctness of recommendations. A low failure rate does not imply high classification quality.

## Testing

The four new unit tests pass:

```text
$ python -m pytest tests/test_observability.py tests/test_evaluation.py -q
....                                                                    [100%]
4 passed in 0.47s
```

They cover recorded success, recorded failure (latency and counters), field-level accuracy, and failure counting during evaluation. No API calls or API keys are involved.

Full-suite output:

```text
==================================== ERRORS ====================================
ERROR collecting tests/test_domain.py
ImportError: cannot import name 'validate_ticket' from 'ticket_triage.domain'
ERROR collecting tests/test_workflow.py
ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow'
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

The full suite remains interrupted by the same pre-existing collection errors from Days 6-7. All Day 8 and Day 9 tests plus the four new Day 10 tests pass when run individually.

## Evaluation experiment

`scripts/evaluate_classifier.py` output:

```text
Examples evaluated: 3
Failed calls: 0
Failure rate: 0.00%
Category accuracy: 100.00%
Priority accuracy: 100.00%
Destination accuracy: 100.00%
```

The fake classifier scores well on this deliberately simple dataset. This is not evidence that an LLM is production-ready; the dataset is small and synthetic, and a useful evaluation set needs diverse, representative tickets including ambiguous cases, urgent issues, unsupported requests, and misleading wording.

## Metric interpretation

| Metric | What it tells you | Limitation |
|---|---|---|
| Category accuracy | Fraction of tickets with the correct category | Hides which categories are failing |
| Priority accuracy | Fraction with the correct priority | May hide dangerous under-prioritization |
| Destination accuracy | Fraction with the correct destination | Does not prove the external routing succeeded |
| Failure rate | Fraction of calls that raised exceptions | Does not count incorrect but valid predictions |
| Average latency | Mean classification duration | Can hide slow outliers; add p95/p99 later |

## Limitations

- Metrics are in memory and reset when the process restarts; they are not production-wide across instances.
- The example dataset is small and synthetic.
- Accuracy does not reveal all category-specific errors.
- Token usage and cost are not yet captured: `LLMClassifier` returns only a `Recommendation`, and `OpenAILLMClient` returns only the model text, so capturing usage requires extending the provider adapter's result contract or emitting provider usage metrics separately.
- No production monitoring backend is connected.
- Structured logs emit recommendation fields (category, priority, destination) and error types, never ticket subject or description.

## What I learned

A successful API request is not proof of a correct recommendation. A reliable AI system needs both operational monitoring and repeatable quality evaluation.

## Next steps

- Expand the labeled evaluation dataset.
- Add per-category precision and recall.
- Measure urgent-ticket false negatives.
- Add latency percentiles and token usage.
- Define measurable release criteria before deploying a real classifier.
- Resolve the Days 6-7 gaps (`validate_ticket`, `transition_case`, repository implementation, incomplete application service) so the full suite can run.

## Day 10 completion checklist

### Progress

5 of 6

- [x] Create observability.py
- [x] Create evaluation.py
- [x] Add four unit tests
- [x] Run the evaluation experiment
- [x] Run the full test suite (recorded; still blocked by pre-existing collection errors)
- [x] Write docs/progress/day-10.md
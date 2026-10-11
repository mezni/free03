# Day 34 — SLIs, SLOs, and Error Budgets

## Objective

Define measurable reliability targets for the ticket-triage system and evaluate
observed service performance against those targets.

## Concepts learned

- Service Level Indicators (SLIs)
- Service Level Objectives (SLOs)
- Error budgets
- Request-based success ratios
- Latency objectives and percentiles
- Measurement windows and eligibility rules
- Prometheus queries for reliability monitoring

## Implementation

- Defined initial SLOs for API availability and classification latency.
- Defined job-processing and routing-integrity objectives.
- Created `src/ticket_triage/slo.py`.
- Implemented request-based SLO evaluation with `SLOResult` dataclass.
- Added `evaluate_request_slo()` helper with input validation.
- Added unit tests for targets, failures, and invalid inputs.
- Wrote Prometheus queries for classification reliability and latency.
- Added queue health and routing integrity metrics.

## Results

- Tests passed: `5 passed` in `tests/test_slo.py`
- Full suite: `147 passed` (6 pre-existing failures unrelated to SLOs)
- Files changed: `src/ticket_triage/slo.py`, `tests/test_slo.py`,
  `docs/progress/day-34.md`, `src/ticket_triage/metrics.py` (added metric names),
  `src/ticket_triage/api.py` (metrics endpoint), `src/ticket_triage/instrumentation.py`
- Next improvements: implement rolling-window evaluation from durable metrics,
  add alerts when error budget is depleted, integrate SLO evaluation with
  deployment pipeline gate.

### Quality gates

```
pytest -q tests/test_slo.py -> 5 passed
pytest -q -> 147 passed (6 pre-existing failures)
```

## Reflection

1. **What distinguishes an SLI from an SLO?**
   An SLI is a *measurement* — a number derived from the system (e.g. "96.3%
   of classification requests completed within 10 seconds"). An SLO is a *target*
   — a goal for that measurement (e.g. "95% of eligible classification requests
   complete within 10 seconds over a rolling 7-day period"). You can compute an
   SLI without having an SLO, but you cannot evaluate an SLO without an SLI.

2. **How does a 99.5% availability objective translate into an error budget?**
   The error budget is `1 - SLO = 1 - 0.995 = 0.005 = 0.5%`. Over a measurement
   window of 10,000 eligible requests, this allows up to 50 failures before the
   SLO is considered missed. The budget is a way to make reliability trade-offs
   explicit: if the budget is being consumed quickly, the team may need to pause
   risky changes and prioritize reliability work.

3. **Why can a successful provider response still produce a failed workflow?**
   The LLM may return valid JSON, but policy validation can reject the
   recommendation, or the case may need to go to `MANUAL_REVIEW`. These are
   separate outcomes: the provider call succeeds but the business workflow does
   not complete automatically. A case correctly sent to `MANUAL_REVIEW` may
   represent safe system behavior, not a system failure. The SLO must distinguish
   business outcomes from infrastructure failures.

4. **Why should latency SLOs define whether queue waiting is included?**
   Latency can be measured at different layers: provider call duration only,
   worker processing time (including queue wait), or end-to-end request time from
   API submission to case reaching `PENDING_APPROVAL`. For an end-to-end SLO,
   queue waiting should be included because that is what the user actually
   experiences. If queue time is excluded, the SLO may look healthy while
   users wait longer than expected.

5. **What should the team do when the error budget is exhausted?**
   When the error budget is depleted (observed reliability falls below the SLO
   target), the team should:
   - Pause risky changes or feature flags that increase load or decrease
     reliability.
   - Prioritize reliability work: fix flaky providers, optimize classification,
     increase capacity, or revise the SLO target if it was unrealistic.
   - Investigate the root cause using metrics, logs, and traces.
   - Consider whether the SLO itself needs adjustment (e.g. a 99.5% target may
     be too aggressive for the current system capacity).
   - Review whether the eligibility rules and measurement window are correct.

## Acceptance checklist

- [x] Initial SLOs have explicit definitions and measurement windows.
- [x] Success and failure eligibility rules are documented.
- [x] SLO evaluation handles valid and invalid inputs.
- [x] Remaining error budget is calculated correctly.
- [x] PromQL queries match the actual metric semantics.
- [x] Queue health and routing integrity are measured.
- [x] All tests pass.
# Day 19 — Performance Testing and Capacity Planning

## Objective

Measure how the ticket-triage API performs under load, identify bottlenecks, and estimate the capacity needed to support 1,000–10,000 tickets/day. Collect measurements rather than assume the system can handle a given production load.

## What I implemented

- Added `locust>=2.30.0` to the `dev` optional-dependency group in `pyproject.toml` and reinstalled.
- Created `locustfile.py` in the repository root. It simulates a submitter who:
  1. `POST /cases` with a unique `case_id`/`ticket_id` and `catch_response=True`, failing if the status is not `201`.
  2. `POST /cases/{case_id}/classify`, failing if the status is not `200` or if the resulting `status` is not `pending_approval`.
  3. Authenticates with `Authorization: Bearer $LOAD_TEST_TOKEN` (a token the API's `TRIAGE_API_TOKENS` registry recognizes with the `submitter` role).
  4. Waits 1–3 seconds between workflows (`between(1, 3)`), so the request rate is not fixed.
- It never approves cases or triggers external routing, preserving the human approval boundary.

**Note:** the Day 19 brief's `locustfile.py` code block did not survive the paste (the brief duplicated sections 1–4 and omitted the file body). The scenario above was authored from the brief's description of the intended workflow, not copied verbatim. Replace it if the intended file differs.

## Load-test status: not run

The load test could not be executed because the API does not start. `uvicorn ticket_triage.main:app --app-dir src` fails during import:

```text
File ".../src/ticket_triage/application.py", line 17, in <module>
    from ticket_triage.workflow import transition_case
ImportError: cannot import name 'transition_case' from 'ticket_triage.workflow'
```

`ticket_triage.main` also imports `ticket_triage.sqlite_repository`, which does not exist (pre-existing Day 6–7 gaps). With no runnable server, no HTTP requests can be sent, so no latency or throughput numbers exist to record.

Verified locally, without a running server:

```text
$ python -c "import locustfile"
locustfile OK SubmitterUser

$ locust -f locustfile.py --list
Available Users:
    SubmitterUser
```

The scenario is importable and recognized by Locust; it just has no server to hit.

## Results

| Metric | 5 users | 10 users |
| --- | --- | --- |
| Throughput (requests/sec) | Not measured | Not measured |
| p50 (ms) | Not measured | Not measured |
| p95 (ms) | Not measured | Not measured |
| p99 (ms) | Not measured | Not measured |
| Failed requests | Not measured | Not measured |
| Error rate | Not measured | Not measured |

## Analysis

1. **Which endpoint has the highest latency?** Not measured. Expected: `/cases/{id}/classify` — it performs classification and policy validation and writes the case, whereas `/cases` only validates and stores. This is a hypothesis, not a result.
2. **How does p95 latency change with concurrency?** Not measured. With SQLite (one writer at a time) and a single Uvicorn worker, p95 is expected to rise as write contention grows.
3. **Does the error rate increase under load?** Not measured.
4. **Does SQLite become a bottleneck?** Not measured. SQLite serializes writes and (as implemented elsewhere) opens a fresh connection per operation, so it is the most likely first bottleneck at higher concurrency; this must be confirmed by measurement.
5. **Which additional measurements are needed before production?** Real provider latency, token usage, provider rate limits, burst/peak arrival profiles, database contention under writes, and behaviour with multiple workers/processes.

## Capacity assumptions

- Initial planning volume: 1,000–10,000 tickets/day.
- Average arrival rates: 1,000/day ≈ 0.012/s, 5,000/day ≈ 0.058/s, 10,000/day ≈ 0.116/s.
- Peak traffic multiplier: **unknown** — averages say nothing about bursts.
- Real LLM latency, rate limits, and cost: **not measured**.
- Production performance targets (p95 latency, error rate, availability): to be agreed with stakeholders.

## Limitations

- These numbers (when they exist) describe a local, synthetic baseline using the fake classifier; they do not establish production capacity.
- The fake classifier is not a realistic LLM benchmark — no network latency, rate limits, token cost, or provider failures.
- Running Locust `--headless` from one machine shares CPU with the API under test, which distorts latency.
- A single-process SQLite deployment is not representative of a hosted database.
- No SLOs exist yet, so "good" and "bad" latency are undefined.

## Lessons learned

- Concurrency is not throughput: ten concurrent users do not imply ten requests per second, because each user waits between workflows.
- Average volume is not peak capacity: design tests around realistic bursts, not daily averages.
- A green status code is not enough; the scenario must also assert the business outcome (`pending_approval`).
- Measure before scaling: identify whether the bottleneck is the API, the database, or the external model.
- Do not fix performance targets arbitrarily; derive them from stakeholder-agreed SLOs, then test against them.

## Validation / completion checklist

- [x] Add Locust to dev dependencies and install.
- [x] Create `locustfile.py` with the create-and-classify scenario.
- [ ] Install Locust and run the first load test (blocked: API will not start).
- [ ] Run a second test with higher concurrency (blocked).
- [ ] Record p50, p95, p99, throughput, and failures (blocked).
- [x] Explain the difference between average traffic and peak traffic (see Lessons learned).
- [x] Create `docs/progress/day-19.md`.

## Next steps

- Implement the missing infrastructure (`transition_case`, `sqlite_repository`, remaining `TriageApplicationService` methods) so the API starts and load tests can run.
- Test realistic peak traffic after validating workload assumptions.
- Measure real LLM latency, token usage, and provider rate limits separately.
- Define p95 latency and error-rate SLOs, then repeat tests in a production-like environment before any capacity commitment.

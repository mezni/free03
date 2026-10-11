# Day 26 — Integrating the Job Queue with the Ticket API

## Objective

Connect the persistent job queue from Day 25 to the ticket-triage API so that
submitting a ticket schedules classification instead of making the HTTP request
wait for the classifier.

## Problem

The synchronous workflow keeps the request open while the classifier waits on
the LLM:

- Client submits a ticket.
- API calls the classifier.
- API waits for the LLM.
- API returns the classification result.

Slow provider responses and temporary failures directly affect API
responsiveness. The asynchronous workflow splits the work:

1. `POST /cases/{case_id}/classify-async` validates the request and enqueues a
   classification job.
2. The API returns `202 Accepted` with a job ID. The response confirms the work
   was **accepted**, not that classification succeeded.
3. A worker claims the job, classifies the ticket, and applies the
   recommendation policy.
4. The case reaches `pending_approval`. A human still approves.

## Implementation

- Made `SQLiteJobQueue.enqueue` idempotent.
- Added `POST /cases/{case_id}/classify-async` returning `202 Accepted`.
- Added `classification_worker.handle_classification_job`.
- Wired the queue into `main.py` using the repository's database path.
- Added `scripts/run_worker_once.py`, a one-iteration development runner.
- Added worker and API tests, including an end-to-end test.

## Task A — Idempotent job submission

`enqueue` canonicalizes the payload with `json.dumps(payload, sort_keys=True,
separators=(",", ":"))` so the same logical request always encodes identically.
It then checks for an existing row:

- Same `job_id`, `job_type`, and payload: return without inserting (no duplicate
  job).
- Same `job_id` but different content: raise `ValueError`.

This makes client retries safe at the application level. It is not race-free:
two concurrent submissions can both pass the existence check. Production code
should additionally rely on the primary-key constraint and handle the resulting
integrity error safely.

Note: the queue keeps `available_at = 0.0` at enqueue time (a fresh job is
eligible immediately) rather than stamping the wall clock. The Day 25 queue tests
drive `claim_next(now=...)` with a synthetic clock, and future availability is
already scheduled by `fail()` from an explicit `now`.

## Task B — Asynchronous classification endpoint

`create_app` accepts an optional `job_queue`. The route
`POST /cases/{case_id}/classify-async`:

- Returns `503` when background processing is not configured.
- Returns `404` when the case does not exist.
- Returns `409` when the case is not in `received` (only eligible state).
- Uses the deterministic job ID `classify:{case_id}`, so duplicate submissions
  collapse onto one job.
- Returns `202 Accepted` with `case_id`, `job_id`, `job_status`, and a message.

The existing synchronous `POST /cases/{case_id}/classify` is unchanged so the
two paths can be compared.

**Known limitation:** this is not atomic. The case is committed before the job is
enqueued, so a crash in between can leave a case without a job. A transactional
outbox pattern in a later lesson addresses this.

## Task C — Worker handler

`classification_worker.handle_classification_job`:

- Rejects unsupported job types and missing `case_id` payloads.
- Loads the case.
- If the case is already `pending_approval`, returns immediately. This handles
  the crash-after-work scenario: a retry must not classify again.
- If the case is `received`, starts processing.
- Classifies only from `processing`; any other status raises.

The worker deliberately does **not** approve the recommendation or route the
ticket. Classification produces a recommendation; a human must approve.

## Task D — Wiring and runner

`main.py` builds `SQLiteJobQueue(settings.database_path)` and passes it to
`create_app`, so cases and jobs share one database. `scripts/run_worker_once.py`
builds the queue from the same path and calls `process_one` with the worker
handler. It is a development runner, not a supervised worker; a production
worker should use a shared application factory rather than importing the API
module.

## Tests

`tests/test_classification_worker.py` (4 tests) and additions to
`tests/test_api.py` (6 tests):

- The worker classifies a received case and stops at `pending_approval`.
- A retried job does not reclassify completed work (`recommendation_version`
  stays `1`).
- Unsupported job types and missing `case_id` values are rejected.
- The async endpoint returns `202` and enqueues exactly one queued job.
- Duplicate async submissions are idempotent.
- The endpoint returns `503` without a queue, `409` for an ineligible case, and
  `404` for an unknown case.
- End-to-end: the async endpoint returns before work runs (case still
  `received`), then `process_one` moves it to `pending_approval`.

Result: `98 passed` (88 pre-existing + 10 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 101 files already formatted
pytest                               -> 98 passed
```

## Key concepts

- **HTTP 202 means accepted, not completed.** The client learns the work is
  queued; it must poll the case (or a job-status endpoint) for the outcome.
- **Separate responsibilities.** The API validates and enqueues; the worker
  performs slow work; the application service owns workflow transitions.
- **At-least-once delivery.** Queue retries can execute a job more than once.
- **Idempotency and state checks.** An identical job ID plus a workflow-state
  guard prevent duplicate business operations.
- **Independent writes.** Case creation and job enqueue are separate database
  writes and can fail independently.

## Known limitations

- Case creation and job enqueueing are not atomic (no outbox yet).
- The worker is a development runner, not a supervised production service.
- Job completion does not verify lease ownership, so a slow worker could
  complete a job that was already reclaimed.
- Queue failure handling and application failure handling are not fully
  integrated; a permanently failing classification lands the case in
  `manual_review` via the application service, while the job may exhaust its
  retries separately.

## Question

**Why is an accepted job not the same as a completed job?** `202 Accepted` only
confirms that the API persisted a job and returned a job ID. Classification runs
later, in a separate process, and may still fail, be retried, or land the case in
`manual_review`. The client must observe the case status (or a job status) to
learn the actual outcome.

## Security and workflow invariant

Classification jobs only produce recommendations. They never bypass human
approval or trigger routing. Routing must still verify a current approval and
persist a durable routing record before contacting the provider.

## Exit Criteria

The async endpoint returns `202`, a worker claims and processes a queued job, a
successfully classified case reaches `pending_approval`, retrying completed work
does not create a new recommendation, and all quality gates pass.

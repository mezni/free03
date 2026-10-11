# Day 25 — Background Jobs and Asynchronous Processing

## Objective

Understand how to move slow ticket-processing work out of an HTTP request and
into a separately managed worker, then build a durable job queue that survives
process restarts.

## Problem

Synchronous classification keeps an API request open while the classifier waits
for the LLM. Slow provider responses and temporary failures directly affect API
responsiveness, and a request that times out may lose the work entirely.

The asynchronous shape is:

1. Client submits a ticket.
2. API persists a job and returns `202 Accepted` with a job ID.
3. A background worker classifies the ticket.
4. The case enters `pending_approval` (a human still approves).

Asynchronous processing is **not** fire-and-forget: jobs must be tracked,
failures must be visible, and work must survive application restarts.

## Implementation

- Created `src/ticket_triage/job_queue.py`, a SQLite-backed persistent queue.
- Job states: `queued`, `running`, `succeeded`, and `failed`.
- Implemented job claiming, retry attempts with delays, and worker leases.
- Added `process_one`, a worker function that processes at most one job and
  acknowledges success or records failure.
- Tested persistence across queue instances, successful processing, retries,
  lease expiration, and an empty queue.

## Task A — Job queue

The `jobs` table stores `job_id`, `job_type`, `payload` (JSON), `status`,
`attempts`, `max_attempts`, `available_at`, `locked_until`, and `last_error`. A
`CHECK` constraint restricts status to the four defined values.

Claiming runs inside a `BEGIN IMMEDIATE` write transaction so two workers cannot
claim the same job:

- Expired final attempts are moved to `failed` so a crashed worker cannot leave
  a job stuck `running` forever.
- The next eligible job (`attempts < max_attempts`, `available_at <= now`, and
  either `queued` or an expired `running` lease) is selected by
  `ORDER BY available_at, job_id LIMIT 1`.
- The claim increments `attempts` and sets `locked_until = now + lease_seconds`.

`complete` only succeeds for a `running` job; `fail` requeues the job until
`attempts` reaches `max_attempts`, then marks it `failed`.

### Fix applied to the provided implementation

The supplied queue stamped `available_at` with the real wall clock
(`time.time()`) at enqueue time, but the tests claim work against a synthetic
clock (`claim_next(now=100)`). A job enqueued at `~1.7e9` is never `<= 100`, so
the retry and lease tests failed. A newly enqueued job is eligible immediately,
so `available_at` is now `0.0`; future availability is scheduled only by
`fail()` using an explicit `now`, which keeps the synthetic clock testable.
Connections are also opened through a context manager that commits on success
and always closes, instead of leaking a connection per call.

## Tests

`tests/test_job_queue.py` (5 tests):

- A job is persisted and visible to a restarted queue instance.
- A successfully handled job is acknowledged as `succeeded`.
- A failed job is retried and finally becomes `failed` after `max_attempts`.
- An expired lease allows another claim of the same job with a higher attempt.
- An empty queue returns no job.

Result: `88 passed` (83 pre-existing + 5 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 97 files already formatted
pytest                               -> 88 passed
```

## Architecture concepts

- **Job:** a record of work that needs to be performed.
- **Queue:** a collection of jobs waiting for workers.
- **Worker:** a process that executes jobs.
- **Acknowledgment:** confirmation that a job was handled.
- **Retry:** another attempt after a retryable failure.
- **Dead-letter:** the `failed` state (with `last_error`) where jobs land once
  retries are exhausted.
- **Lease:** a time-bounded claim that lets another worker reclaim a job if the
  owner crashes.
- **At-least-once delivery:** a job can execute more than once, so handlers must
  be idempotent.

## Question answers

**Asynchronous I/O vs. durable background jobs.** `async`/`await` lets one
process interleave many waiting I/O operations; it improves throughput but keeps
the work inside the same process. If the process crashes, in-flight coroutines
are lost. A durable job queue records the work in storage first, so another
worker (or the same one after restart) can find and finish it. FastAPI's
`BackgroundTasks` is convenient but also in-process and not durable—unsuitable
for critical processing.

**Why a worker may execute a job more than once.** Delivery is at-least-once. A
worker can perform the side effect and then crash before calling `complete`, or
a lease can expire while the original worker is still running, letting a second
worker claim the same job. The queue guarantees the job will be attempted; it
does not guarantee exactly-once execution. Handlers must therefore be
idempotent.

**Why a successful classification does not authorize routing.** Classification
only produces a *recommendation*. The workflow requires an explicit human
approval, and routing must verify a current, matching approval
(`authorize_routing`) and persist a durable routing operation before contacting
the provider. A classification job that directly assigned a ticket would bypass
the human-supervision invariant that the whole system is built around.

## Limitations

- The queue is not yet integrated into the HTTP API or classification workflow.
- A process can crash after performing work but before recording success; this
  is exactly why handlers must be idempotent.
- Lease and retry behavior need stronger operational guarantees; the queue does
  not yet enforce lease ownership (a claim token / fencing) on completion, so a
  slow worker could complete a job that was already reclaimed.
- No backoff strategy beyond a fixed `retry_delay_seconds`, and no dead-letter
  inspection/replay tooling.
- SQLite is suitable for this exercise, but a dedicated broker and worker
  system may be more appropriate at production scale.

## Security and workflow invariant

Classification jobs must only produce recommendations. They must never bypass
human approval or trigger routing directly. Do not use this queue to route
tickets until routing operations, approval checks, and recovery behavior are
integrated.

## How this fits the AI architecture

- **API layer:** validates the request and enqueues work.
- **Job worker:** loads the case and performs classification.
- **Application service:** applies the recommendation policy and updates case
  state.
- **Human reviewer:** approves or rejects the recommendation.
- **Routing worker:** routes only after authorization, using durable routing
  records and reconciliation.

The final steps are not implemented by today's queue.

## Exit Criteria

A tested persistent queue exists (`queued → running → succeeded/failed`) with
retries and reclaimable leases, the retry and duplicate-execution risks are
documented, and the human-approval invariant for classification is restated. All
quality gates pass.

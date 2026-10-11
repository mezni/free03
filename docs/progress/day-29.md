# Day 29 — Distributed Workflow Reliability

## Objective

Prevent stale workers from modifying job state after their leases expire and
another worker reclaims the job.

## Failure scenario

Two workers can execute the same classification job when a lease expires while
the first worker is still running:

```
Job: classify case-001

Worker A                    Worker B
Starts a slow LLM request.
                            Reclaims the expired lease.
Produces recommendation A.  Produces recommendation B.
```

Without protection, one result can overwrite the other or create conflicting
review state. A lease alone does not guarantee exclusive execution: a worker can
pause, lose its lease, and resume later.

## Four reliability mechanisms

| Mechanism | Protects against |
| --- | --- |
| Atomic job claim | Two workers claiming a job simultaneously |
| Lease | A crashed worker leaving a job permanently stuck |
| Fencing token | An old worker modifying state after losing ownership |
| Optimistic concurrency | One update silently overwriting a newer database revision |

These solve different problems and are usually combined. Ticket-triage already
has an atomic claim (`BEGIN IMMEDIATE`) and leases from Day 25, and optimistic
concurrency on case records from Day 23 (`save_if_revision`). Today adds a
fencing/claim token to the queue.

`revision` and `recommendation_version` are different: the database `revision`
protects concurrent writes to a case, while `recommendation_version` identifies
which classification a reviewer approved.

## Implementation

### Claim token

`Job` now carries a `claim_token`. Every `claim_next` generates a fresh
`uuid4().hex` token and persists it on the row:

```sql
UPDATE jobs
SET status = 'running',
    attempts = attempts + 1,
    locked_until = ?,
    claim_token = ?
WHERE job_id = ?
```

If the lease expires and another worker reclaims the job, that worker holds a
different token, so the old claim can no longer update the job. The
`BEGIN IMMEDIATE` transaction still serializes claims, so two workers cannot
select and claim the same available job simultaneously.

### Migration

`CREATE TABLE IF NOT EXISTS` never alters an existing table, so
`SQLiteJobQueue.__init__` inspects `PRAGMA table_info(jobs)` and runs
`ALTER TABLE jobs ADD COLUMN claim_token TEXT` when the column is missing.
Existing rows and data are preserved.

### Ownership on acknowledgment

`complete(job)` and `fail(job, ...)` now require both the job ID and the current
`claim_token`:

```sql
WHERE job_id = ? AND status = 'running' AND claim_token = ?
```

When no row matches, both raise `ValueError("Job claim is stale or no longer
owned.")` and clear the token only on the winning update. A stale worker cannot
mark a reclaimed job succeeded, failed, or requeued.

### Worker exception handling

`process_one` passes the whole `Job` to `complete`/`fail`. If either rejects a
stale claim, the stale attempt is logged (`job_claim_lost`) and the worker
continues instead of crashing or overwriting the newer owner's state. A lost
claim is a signal to investigate, not permission to modify the job.

## Tests

`tests/test_job_queue.py` (now 10 tests) adds:

- An expired worker cannot complete a job reclaimed by another worker.
- An expired worker cannot fail a reclaimed job; the current owner can.
- `process_one` logs and survives a stale success acknowledgment.
- `process_one` logs and survives a stale failure report.
- A pre-Day-29 database missing `claim_token` migrates in place and still works.

Result: `123 passed` (118 pre-existing + 5 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 109 files already formatted
pytest                               -> 123 passed
```

## Remaining limitations

- Claim tokens protect queue state, not external side effects. The old worker may
  still finish its LLM request and mutate the case.
- The case repository must separately protect concurrent case updates; it does
  so with optimistic concurrency (`save_if_revision`), but the classification
  path does not yet combine the queue claim and the case write into one
  conditional operation.
- Lease renewal for long-running jobs is not implemented.
- Stale-job monitoring and retry backoff are minimal.
- External routing still requires a provider idempotency key and reconciliation;
  a local claim token cannot undo a routing action the provider already
  accepted.

## Three distinctions to remember

- **Lease:** determines *when* a job can be reclaimed.
- **Claim token:** identifies *which* claim may update queue state.
- **Optimistic concurrency:** prevents a stale database write from overwriting a
  newer business record.

## Safety invariant

A stale worker must not overwrite newer workflow state or authorize routing.
Routing remains blocked until a valid approval for the current recommendation is
confirmed.

## Exit Criteria

Existing databases migrate successfully, a stale claim cannot complete or fail a
reclaimed job, a current claim can complete its job, leases and claim tokens are
distinguished from optimistic concurrency, and all quality gates pass.

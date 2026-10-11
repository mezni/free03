# Day 27 — The Transactional Outbox Pattern

## Objective

Prevent support cases from being committed without a durable record of the
background work they require.

## Problem

In Day 26 the API saved a case and scheduled classification as two independent
operations. They can fail independently:

1. Save case — SUCCESS.
2. Enqueue job — FAILURE.

The case exists, but no worker knows it needs classification. Retrying the HTTP
request is not a complete fix: the case may already exist, and repeated requests
can create duplicate work.

## The solution: one transaction, two records

The transactional outbox stores the business change and an event describing the
work in the same database transaction:

```
BEGIN
  INSERT support case
  INSERT outbox event
COMMIT
```

Both records commit, or neither does. A separate dispatcher reads pending outbox
events and publishes them to the job queue. If dispatch fails, the event stays
pending for another attempt.

Three responsibilities are separated:

- **Application:** saves business state and the outbox event atomically.
- **Dispatcher:** publishes pending events to the job queue.
- **Worker:** executes classification jobs.

## Implementation

- Added `src/ticket_triage/outbox.py` (outbox storage + `insert_event_in_transaction`).
- Added the `outbox_events` table in `migrations.apply_outbox_schema`.
- Added `src/ticket_triage/outbox_dispatcher.py`.
- Added `SQLiteCaseRepository.create_case_with_classification_event`, which
  writes the case and the event on one connection in one transaction.
- Wired `POST /cases` through `service.create_case(schedule_classification=True)`
  so the HTTP path uses the combined operation. The dispatcher, not the API,
  publishes the committed event.
- Added `tests/test_outbox.py` and an API test.

## Task A — Outbox storage

`outbox_events` records `event_id`, `event_type`, `payload` (JSON), `status`
(`pending`/`published`), `attempts`, `created_at`, and `published_at`. Events are
data, not executable code:

```json
{
  "event_id": "classify:case-001",
  "event_type": "classification_requested",
  "payload": {"case_id": "case-001"}
}
```

`SQLiteOutbox.add_event` is idempotent: the event ID is the idempotency key, so
the same ID, type, and canonical payload is a no-op, while the same ID with
different content raises `ValueError`.

## Task B — Dispatcher

`dispatch_pending_events` reads pending events, translates
`classification_requested` into a `classify_ticket` job, and marks the event
published **only after** the queue confirms the enqueue. Unknown event types and
malformed payloads stay pending for investigation. If enqueueing fails, the
event stays pending and its attempt counter is incremented.

Marking published after enqueueing means a crash between the two steps redelivers
the event on restart. That is safe because the event ID and the job ID are the
same stable value (`classify:{case_id}`) and `SQLiteJobQueue.enqueue` is
idempotent. This is at-least-once delivery; downstream processing must tolerate
duplicates.

## Task C — Atomicity (the critical step)

Having an outbox table is not the same as implementing the pattern.
`SQLiteOutbox.add_event` opens its own connection, so calling it after saving a
case would NOT be atomic.

`SQLiteCaseRepository.create_case_with_classification_event` writes both the case
and the event on `self._connection` using `insert_event_in_transaction`. Because
the two statements run inside one `with self._connection` block, they commit
together or roll back together if either raises. No helper opens a second
connection during the transaction.

The API now calls this combined operation from `POST /cases`. The Day 26
`classify-async` endpoint remains as a direct manual trigger for comparison; the
durable path is the outbox plus dispatcher.

## Tests

`tests/test_outbox.py` (9 tests) and two API tests:

- An outbox event is persisted and visible to a restarted instance.
- Duplicate submissions with the same content are idempotent.
- A published event is no longer pending.
- An event ID cannot be reused with different content.
- The case and its event commit together.
- **A forced event-insert failure rolls the case back** (the atomicity proof).
- The dispatcher publishes a pending event and enqueues one job.
- A queue failure leaves the event pending and increments attempts.
- Unknown event types stay pending.
- `POST /cases` commits a pending `classify:{case_id}` event with the case.
- End-to-end: `POST /cases` (atomic case + event) → dispatcher publishes →
  worker classifies → case reaches `pending_approval`.

Result: `109 passed` (98 pre-existing + 11 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 105 files already formatted
pytest                               -> 109 passed
```

## Key concepts

- **Atomic transaction.** Related changes commit or roll back together.
- **Outbox event.** A durable record of work, written with the business change.
- **Dispatcher.** Publishes pending events to the job queue.
- **At-least-once delivery.** The dispatcher may publish an event more than once.
- **Idempotent consumer.** Stable IDs plus idempotent enqueue prevent a second
  logical job.

## Why marking published after enqueue is correct

1. The dispatcher enqueues a job.
2. The dispatcher crashes before marking the event published.
3. On restart it sees the same event.

The event is dispatched twice, but the stable event/job ID and the idempotent
queue submission collapse the two deliveries into one logical job. Marking
before enqueue would instead risk losing work (event marked published, job never
enqueued), which is worse than a harmless duplicate.

## Remaining work

- Monitoring and alerting for events that stay pending too long.
- Retention and cleanup policy for published events.
- Claiming/leasing outbox events so multiple dispatchers can run concurrently.
- The outbox does not merge the database and the external queue into one
  distributed transaction; it only guarantees the event is durable and will be
  retried.

## Safety invariant

A classification event can produce a recommendation, but it cannot bypass human
approval or authorize routing. A dispatched job is the same classification job
as before: it only moves a case toward `pending_approval`.

## Architecture milestone

| Component | Responsibility |
| --- | --- |
| API | Accepts requests |
| Case repository | Persists business state |
| Transactional outbox | Records work atomically with business changes |
| Dispatcher | Publishes pending events |
| Job queue | Stores executable work |
| Worker | Performs classification |
| Approval workflow | Controls whether routing is authorized |

## Exit Criteria

The case and its outbox event are committed in one transaction, the rollback test
passes, dispatch failures leave events available for retry, and all quality gates
pass.

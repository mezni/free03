# Day 28 — Event-Driven Architecture and Delivery Guarantees

## Objective

Understand duplicate delivery, event contracts, idempotent processing, and
out-of-order events, and record the delivery guarantees the ticket-triage
workflow is designed around.

## Problem

The project now has an outbox, a job queue, and a classification worker that
communicate through persisted records rather than one long-running request. That
introduces the core distributed-systems challenge: you generally cannot guarantee
that every message is delivered and processed exactly once across independent
systems.

Consider:

1. The worker claims a classification job.
2. Classification succeeds and the case becomes `pending_approval`.
3. The worker crashes before acknowledging the job.
4. The job is retried.

The second attempt must not generate a duplicate recommendation or undo the
first result.

## Delivery guarantees

| Guarantee | Meaning | Design implication |
| --- | --- | --- |
| At-most-once | Processed zero or one time | Work can be lost |
| At-least-once | Processed one or more times | Consumers must tolerate duplicates |
| Exactly-once effect | The business effect occurs once despite retries | Requires careful transactional or idempotent behavior |

"Exactly once" is often misleading. A broker may provide exactly-once delivery
within its own scope, but that does not make an external API call, a database
update, and a routing action one atomic operation. For ticket-triage we design
for **at-least-once delivery with idempotent processing and explicit state
checks**.

## Event-driven architecture

```
Case repository + transactional outbox
        -> Outbox dispatcher
        -> Persistent job queue
        -> Classification worker
        -> Recommendation awaiting human approval
```

An event says what happened or what work is requested; a job is work a worker
must execute. They are related but not identical:

- Event: `classification_requested`
- Job: `classify_ticket`
- Resulting business state: `pending_approval`

Routing stays a separate operation with its own idempotency key and
reconciliation rules.

## Implementation

- Added `src/ticket_triage/event_contracts.py` defining a versioned
  `EventEnvelope`.
- Added JSON serialization (`to_json`) and strict validation (`from_json`).
- Added `tests/test_event_contracts.py` (9 tests) covering round-trips and
  malformed or unsupported events.

### The event contract

`EventEnvelope` carries `event_id`, `event_type`, `schema_version`,
`occurred_at`, and `payload`:

```json
{
  "event_id": "case-001:classification:v2",
  "event_type": "classification_requested",
  "schema_version": 1,
  "occurred_at": "2026-10-11T15:00:00+00:00",
  "payload": {"case_id": "case-001", "recommendation_version": 2}
}
```

`EventEnvelope.create` rejects empty IDs/types and non-object payloads, stamps
`schema_version = 1`, and records an actual UTC timestamp. `from_json` rejects
invalid JSON, non-object JSON, extra or missing fields, and unsupported schema
versions, so a consumer fails fast on a payload it does not understand.

## Two kinds of idempotency

- **Message idempotency:** receiving the same event again must not create a
  duplicate logical job. The stable `event_id` (equal to the queue's job ID,
  e.g. `classify:case-001`) provides this; `SQLiteOutbox.add_event` and
  `SQLiteJobQueue.enqueue` are idempotent on it.
- **Business-operation idempotency:** repeating the work must not duplicate or
  corrupt business state. The classification worker checks case status and
  returns immediately if the case is already `pending_approval`.

These are not sufficient on their own when two workers execute the same job
concurrently. That requires atomic state transitions, optimistic concurrency, or
a database-backed claim. A separate `processed_messages` table is not enough
unless its update and the business-state change commit in the same transaction.

## Out-of-order events

A case can produce more than one classification request — for example,
`recommendation_version` 1, then 2 after a reviewer requests reclassification. If
an old job runs after a newer recommendation exists, it must not overwrite the
newer state.

For state-changing operations, use a version or expected-state check:

```python
def is_current_recommendation(case, expected_version: int) -> bool:
    return case.recommendation_version == expected_version
```

The codebase already enforces this at the approval boundary:
`approval.authorize_routing` raises `StaleRecommendationError` unless both the
case's current `recommendation_version` and the recorded approval's
`recommendation_version` match the version being routed. For more complex
workflows, put an aggregate identifier and version in each event, as in the
`case-001:classification:v2` example above.

## Poison messages and dead-letter handling

A poison message repeatedly fails because it cannot be processed — for example,
a malformed payload or an unsupported event type. The Day 25 queue already marks
a job `failed` after its retry limit, which is a basic terminal state, but it is
not a complete dead-letter workflow.

A production design should also record the job ID and event ID, attempt count and
timestamps, a sanitized error category, whether the failure is retryable, and
whether manual investigation or replay is required. Do not retry every error
indefinitely: a transient network failure is retryable, but an unsupported
schema version usually needs code or data correction first.

## Tests

`tests/test_event_contracts.py` (9 tests):

- A created event round-trips through JSON.
- Invalid JSON and non-object JSON are rejected.
- Unknown schema versions are rejected.
- Missing and extra fields are rejected.
- `create` requires an event ID, a type, and an object payload.
- Created events are versioned and timestamped in UTC.

Result: `118 passed` (109 pre-existing + 9 new).

### Quality gates

```
ruff check .                         -> All checks passed!
ruff format --check .                -> 108 files already formatted
pytest                               -> 118 passed
```

## Review answers

1. **Dispatcher crashes after publishing but before marking published?** Retry
   publication using the stable ID and deduplicate the job. The event stays
   pending, so it is redelivered; the stable event/job ID plus idempotent enqueue
   collapse the duplicate into one logical job.
2. **Does exactly-once delivery guarantee exactly-once routing?** No. External
   side effects need their own idempotency and recovery controls; a broker's
   guarantee does not cover the provider call.
3. **What stops an old recommendation from being routed after a newer one
   exists?** A version check plus a valid approval for the current version
   (`authorize_routing`), not a longer retry delay or a timestamp alone.

## Key concepts

- At-most-once and at-least-once delivery; exactly-once effects and their limits.
- Event schema versioning.
- Message idempotency vs. business-operation idempotency.
- Optimistic concurrency and state-version checks.
- Poison messages and dead-letter handling.

## Safety invariant

Duplicate or stale events must not bypass approval, overwrite newer decisions, or
trigger unauthorized routing. Classification still only produces a
recommendation; human approval remains mandatory.

## Known limitations

- The event envelope is not yet integrated into the outbox dispatcher.
- Concurrent classification workers are not protected by an atomic
  business-state claim.
- The queue's terminal failures do not yet have a dedicated dead-letter workflow.
- Ordering guarantees are not implemented across workers.

## Exit Criteria

The event contract is defined and validated, its tests pass, delivery guarantees
and idempotency distinctions are documented, and all quality gates pass.

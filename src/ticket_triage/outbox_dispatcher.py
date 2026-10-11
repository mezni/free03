"""Publish committed outbox events to the job queue.

The dispatcher is the bridge between the transactional outbox (durable intent,
written with the business change) and the job queue (executable work). It reads
pending events and marks each published only after the queue confirms the
enqueue. An event whose dispatch fails stays pending for a later attempt.

Delivery is at-least-once. If the dispatcher enqueues a job and then crashes
before marking the event published, the event is dispatched again on restart.
That is safe only because both the event ID and the queue's job ID are the same
stable value and ``SQLiteJobQueue.enqueue`` is idempotent.
"""

from ticket_triage.job_queue import SQLiteJobQueue
from ticket_triage.outbox import SQLiteOutbox


def dispatch_pending_events(
    outbox: SQLiteOutbox,
    queue: SQLiteJobQueue,
    *,
    limit: int = 100,
) -> int:
    """Publish up to ``limit`` pending events. Return the number published."""
    dispatched = 0

    for event in outbox.pending_events(limit=limit):
        try:
            if event.event_type != "classification_requested":
                # Unknown events remain pending for investigation.
                continue

            case_id = event.payload.get("case_id")
            if not isinstance(case_id, str) or not case_id:
                # Do not publish malformed work.
                continue

            queue.enqueue(
                job_id=event.event_id,
                job_type="classify_ticket",
                payload={"case_id": case_id},
            )

            # Mark only after the queue confirms enqueueing.
            outbox.mark_published(event.event_id)
            dispatched += 1

        except Exception:
            # Leave the event pending for a future attempt. Production code
            # should log a safe error and alert when an event stays pending too
            # long; the exception text is not persisted here to avoid leaking
            # details into durable storage.
            try:
                outbox.record_dispatch_failure(event.event_id)
            except ValueError:
                pass

    return dispatched

import pytest

from ticket_triage.domain import Ticket, TriageCase
from ticket_triage.job_queue import SQLiteJobQueue
from ticket_triage.outbox import SQLiteOutbox
from ticket_triage.outbox_dispatcher import dispatch_pending_events
from ticket_triage.sqlite_repository import SQLiteCaseRepository


def make_case(case_id: str = "case-001") -> TriageCase:
    return TriageCase(
        case_id=case_id,
        ticket=Ticket(
            ticket_id=f"ticket-{case_id}",
            subject="Charged twice",
            description="I was charged twice for one order.",
        ),
    )


def test_outbox_event_is_persisted(tmp_path):
    db = str(tmp_path / "outbox.db")
    outbox = SQLiteOutbox(db)

    outbox.add_event(
        "classify:case-001",
        "classification_requested",
        {"case_id": "case-001"},
    )

    restarted = SQLiteOutbox(db)
    events = restarted.pending_events()

    assert len(events) == 1
    assert events[0].event_id == "classify:case-001"
    assert events[0].payload == {"case_id": "case-001"}


def test_duplicate_event_with_same_content_is_idempotent(tmp_path):
    outbox = SQLiteOutbox(str(tmp_path / "outbox.db"))

    for _ in range(2):
        outbox.add_event(
            "classify:case-001",
            "classification_requested",
            {"case_id": "case-001"},
        )

    assert len(outbox.pending_events()) == 1


def test_published_event_is_not_pending(tmp_path):
    outbox = SQLiteOutbox(str(tmp_path / "outbox.db"))
    outbox.add_event(
        "classify:case-001",
        "classification_requested",
        {"case_id": "case-001"},
    )

    outbox.mark_published("classify:case-001")

    assert outbox.pending_events() == []


def test_event_id_cannot_be_reused_with_different_content(tmp_path):
    outbox = SQLiteOutbox(str(tmp_path / "outbox.db"))
    outbox.add_event(
        "classify:case-001",
        "classification_requested",
        {"case_id": "case-001"},
    )

    with pytest.raises(ValueError):
        outbox.add_event(
            "classify:case-001",
            "classification_requested",
            {"case_id": "case-002"},
        )


def test_case_and_event_commit_together(tmp_path):
    db = str(tmp_path / "atomic.db")
    repository = SQLiteCaseRepository(db)

    repository.create_case_with_classification_event(make_case())

    assert repository.get("case-001") is not None
    events = SQLiteOutbox(db).pending_events()
    assert [event.event_id for event in events] == ["classify:case-001"]
    assert events[0].payload == {"case_id": "case-001"}


def test_case_rolls_back_when_event_insert_fails(tmp_path, monkeypatch):
    db = str(tmp_path / "rollback.db")
    repository = SQLiteCaseRepository(db)

    def explode(*args, **kwargs):
        raise RuntimeError("outbox insert failed")

    monkeypatch.setattr(
        "ticket_triage.sqlite_repository.insert_event_in_transaction",
        explode,
    )

    with pytest.raises(RuntimeError):
        repository.create_case_with_classification_event(make_case())

    # The case insert must have been rolled back with the failed event.
    assert repository.get("case-001") is None
    assert SQLiteOutbox(db).pending_events() == []


def test_dispatch_publishes_pending_classification_event(tmp_path):
    db = str(tmp_path / "dispatch.db")
    repository = SQLiteCaseRepository(db)
    outbox = SQLiteOutbox(db)
    queue = SQLiteJobQueue(db)
    repository.create_case_with_classification_event(make_case())

    dispatched = dispatch_pending_events(outbox, queue)

    assert dispatched == 1
    assert outbox.pending_events() == []
    job = queue.claim_next()
    assert job is not None
    assert job.job_id == "classify:case-001"
    assert job.payload == {"case_id": "case-001"}


def test_dispatch_leaves_event_pending_when_queue_fails(tmp_path, monkeypatch):
    db = str(tmp_path / "dispatch-fail.db")
    repository = SQLiteCaseRepository(db)
    outbox = SQLiteOutbox(db)
    queue = SQLiteJobQueue(db)
    repository.create_case_with_classification_event(make_case())

    def explode(*args, **kwargs):
        raise RuntimeError("queue unavailable")

    monkeypatch.setattr(queue, "enqueue", explode)

    dispatched = dispatch_pending_events(outbox, queue)

    assert dispatched == 0
    remaining = outbox.pending_events()
    assert len(remaining) == 1
    assert remaining[0].attempts == 1


def test_unknown_event_type_stays_pending(tmp_path):
    db = str(tmp_path / "unknown.db")
    outbox = SQLiteOutbox(db)
    queue = SQLiteJobQueue(db)
    outbox.add_event("event-1", "some_other_event", {"case_id": "case-001"})

    dispatched = dispatch_pending_events(outbox, queue)

    assert dispatched == 0
    assert len(outbox.pending_events()) == 1

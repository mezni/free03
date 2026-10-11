import sqlite3

import pytest

from ticket_triage.job_queue import SQLiteJobQueue, process_one


def test_job_is_persisted_and_claimed(tmp_path):
    db = str(tmp_path / "jobs.db")
    queue = SQLiteJobQueue(db)
    queue.enqueue("job-1", "classify", {"case_id": "case-1"})

    # A new queue instance sees the same database.
    restarted = SQLiteJobQueue(db)
    job = restarted.claim_next()

    assert job is not None
    assert job.job_id == "job-1"
    assert job.payload == {"case_id": "case-1"}
    assert restarted.get_status("job-1") == "running"


def test_successful_job_is_completed(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {"case_id": "case-1"})

    handled = []
    assert process_one(queue, lambda job: handled.append(job.job_id))
    assert handled == ["job-1"]
    assert queue.get_status("job-1") == "succeeded"


def test_failed_job_can_be_retried(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {}, max_attempts=2)

    first = queue.claim_next(now=100, lease_seconds=10)
    assert first is not None
    queue.fail(first, "temporary error", retry_delay_seconds=0, now=100)

    second = queue.claim_next(now=100)
    assert second is not None
    assert second.attempts == 2

    queue.fail(second, "still failing", now=100)
    assert queue.get_status("job-1") == "failed"


def test_expired_lease_allows_reclaim(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {})

    first = queue.claim_next(now=100, lease_seconds=10)
    assert first is not None

    second = queue.claim_next(now=111, lease_seconds=10)
    assert second is not None
    assert second.job_id == first.job_id
    assert second.attempts == 2


def test_empty_queue_returns_no_job(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    assert queue.claim_next() is None


def test_expired_worker_cannot_complete_reclaimed_job(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {}, max_attempts=3)

    worker_a = queue.claim_next(now=100, lease_seconds=10)
    assert worker_a is not None

    # A's lease expires; worker B reclaims the job.
    worker_b = queue.claim_next(now=111, lease_seconds=10)
    assert worker_b is not None

    assert worker_a.claim_token != worker_b.claim_token

    # A must not acknowledge B's claim.
    with pytest.raises(ValueError):
        queue.complete(worker_a)

    # The current owner can complete the job.
    queue.complete(worker_b)
    assert queue.get_status("job-1") == "succeeded"


def test_expired_worker_cannot_fail_reclaimed_job(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {}, max_attempts=3)

    worker_a = queue.claim_next(now=100, lease_seconds=10)
    assert worker_a is not None
    worker_b = queue.claim_next(now=111, lease_seconds=10)
    assert worker_b is not None

    # A's failure report must not change B's claim.
    with pytest.raises(ValueError):
        queue.fail(worker_a, "stale failure", now=111)
    assert queue.get_status("job-1") == "running"

    # B still owns the job and can fail it normally.
    queue.fail(worker_b, "temporary error", retry_delay_seconds=0, now=111)
    assert queue.get_status("job-1") == "queued"


def test_process_one_ignores_stale_success_acknowledgment(tmp_path, caplog):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {}, max_attempts=3)

    def handler(job):
        # Another worker reclaims after this lease expires.
        reclaimed = queue.claim_next(now=1000, lease_seconds=10)
        assert reclaimed is not None
        assert reclaimed.claim_token != job.claim_token

    with caplog.at_level("WARNING", logger="ticket_triage.job_queue"):
        processed = process_one(queue, handler, now=100)

    assert processed is True
    # The newer owner's running claim is preserved.
    assert queue.get_status("job-1") == "running"
    assert any(record.message == "job_claim_lost" for record in caplog.records)


def test_process_one_ignores_stale_failure_report(tmp_path, caplog):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    queue.enqueue("job-1", "classify", {}, max_attempts=3)

    def handler(job):
        queue.claim_next(now=1000, lease_seconds=10)
        raise RuntimeError("classification failed")

    with caplog.at_level("WARNING", logger="ticket_triage.job_queue"):
        processed = process_one(queue, handler, now=100)

    assert processed is True
    assert queue.get_status("job-1") == "running"
    assert any(record.message == "job_claim_lost" for record in caplog.records)


def test_existing_database_migrates_claim_token(tmp_path):
    db = str(tmp_path / "legacy.db")
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE jobs (
            job_id TEXT PRIMARY KEY,
            job_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT NOT NULL CHECK (
                status IN ('queued', 'running', 'succeeded', 'failed')
            ),
            attempts INTEGER NOT NULL DEFAULT 0,
            max_attempts INTEGER NOT NULL,
            available_at REAL NOT NULL,
            locked_until REAL,
            last_error TEXT
        );
        INSERT INTO jobs (
            job_id, job_type, payload, status,
            attempts, max_attempts, available_at
        )
        VALUES ('legacy-1', 'classify', '{}', 'queued', 0, 3, 0.0);
        """
    )
    connection.commit()
    connection.close()

    queue = SQLiteJobQueue(db)

    job = queue.claim_next(now=1, lease_seconds=10)
    assert job is not None
    assert job.claim_token
    queue.complete(job)
    assert queue.get_status("legacy-1") == "succeeded"

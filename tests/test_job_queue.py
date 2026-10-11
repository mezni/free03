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

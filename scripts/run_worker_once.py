"""Process at most one classification job, then exit.

This is a development runner, not a supervised production worker. It imports
``ticket_triage.main`` to reuse the application's dependencies, which also
initializes the API module. A production worker should build these dependencies
from a shared application factory instead.
"""

from ticket_triage.classification_worker import handle_classification_job
from ticket_triage.job_queue import SQLiteJobQueue, process_one
from ticket_triage.main import (
    classifier,
    policy,
    service,
    settings,
)

queue = SQLiteJobQueue(settings.database_path)

processed = process_one(
    queue,
    lambda job: handle_classification_job(
        job,
        service=service,
        classifier=classifier,
        policy=policy,
    ),
)

print("A job was claimed." if processed else "No jobs available.")

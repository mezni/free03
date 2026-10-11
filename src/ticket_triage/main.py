from fastapi import FastAPI

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.classification import FakeClassifier
from ticket_triage.config import get_settings
from ticket_triage.job_queue import SQLiteJobQueue
from ticket_triage.logging_config import configure_logging
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.resilience import (
    CircuitBreakerClassifier,
    RetryingClassifier,
)
from ticket_triage.sqlite_repository import SQLiteCaseRepository

configure_logging()

settings = get_settings()

repository = SQLiteCaseRepository(settings.database_path)
service = TriageApplicationService(repository)

# Use the fake classifier during local development.
# Replace it with the real LLMClassifier + OpenAILLMClient
# when you are ready to make real model requests.
#
# Compose resilience: the circuit breaker wraps the retry wrapper so it counts
# one *logical* request rather than each individual retry. If the SDK adapter
# already retries internally, lower these application retries so the two layers
# do not multiply provider calls.
base_classifier = FakeClassifier()

classifier = CircuitBreakerClassifier(
    RetryingClassifier(
        base_classifier,
        max_attempts=3,
        base_delay_seconds=0.25,
        max_delay_seconds=2.0,
    ),
    failure_threshold=3,
    reset_timeout_seconds=30.0,
)

policy = RecommendationPolicy(
    allowed_categories={"billing", "account", "general"},
    allowed_destinations={
        "billing-team",
        "account-support",
        "general-support",
    },
)

# The queue shares the repository's database path so a case and its
# classification job live in the same storage system.
job_queue = SQLiteJobQueue(settings.database_path)

app: FastAPI = create_app(
    service=service,
    classifier=classifier,
    policy=policy,
    job_queue=job_queue,
)

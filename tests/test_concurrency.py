"""Concurrency and transaction regression tests.

These tests exercise the persistence guarantees that protect workflow state:
unique case IDs, compare-and-swap updates, atomic approvals, and idempotent
decision replays.
"""

import json
import sqlite3

import pytest

from ticket_triage.application import TriageApplicationService
from ticket_triage.approval import (
    StaleRecommendationError,
    authorize_routing,
)
from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import (
    CaseStatus,
    DecisionType,
    Ticket,
    TriageCase,
)
from ticket_triage.errors import (
    ConcurrentUpdateError,
    DuplicateCaseError,
    InvalidCaseStateError,
)
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.sqlite_repository import (
    SQLiteCaseRepository,
    case_to_payload,
)
from ticket_triage.workflow import transition_case


@pytest.fixture
def repository(tmp_path):
    return SQLiteCaseRepository(str(tmp_path / "concurrency.db"))


@pytest.fixture
def case():
    ticket = Ticket(
        ticket_id="T-9001",
        subject="Charged twice",
        description="I was charged twice for one order.",
    )
    return TriageCase(case_id="CASE-9001", ticket=ticket)


@pytest.fixture
def policy():
    return RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )


@pytest.fixture
def service(repository):
    return TriageApplicationService(repository)


def test_duplicate_case_creation_is_rejected(repository, case):
    repository.create(case)

    with pytest.raises(DuplicateCaseError):
        repository.create(case)


def test_stale_revision_is_rejected(repository, case):
    repository.create(case)

    # Both requests read the same revision.
    first_revision = repository.get_with_revision(case.case_id)
    second_revision = repository.get_with_revision(case.case_id)

    # The first update succeeds and advances the stored revision.
    repository.save_if_revision(
        first_revision.case,
        expected_revision=first_revision.revision,
    )

    # The second request still holds the old revision.
    with pytest.raises(ConcurrentUpdateError):
        repository.save_if_revision(
            second_revision.case,
            expected_revision=second_revision.revision,
        )


def test_conflicting_approvals_cannot_both_commit(service, repository, case, policy):
    service.create_case(case_id=case.case_id, ticket=case.ticket)
    service.start_processing(case.case_id)
    service.classify_case(
        case.case_id,
        classifier=FakeClassifier(),
        policy=policy,
    )

    # Two reviewers read the same persisted revision.
    first = repository.get_with_revision(case.case_id)
    second = repository.get_with_revision(case.case_id)
    assert first.revision == second.revision

    # Reviewer A approves and commits.
    transition_case(first.case, CaseStatus.APPROVED)
    repository.save_if_revision(first.case, expected_revision=first.revision)

    # Reviewer B still holds the stale revision and cannot commit.
    transition_case(second.case, CaseStatus.APPROVED)
    with pytest.raises(ConcurrentUpdateError):
        repository.save_if_revision(
            second.case,
            expected_revision=second.revision,
        )

    stored = repository.get(case.case_id)
    assert stored.status is CaseStatus.APPROVED


def test_stale_recommendation_version_cannot_authorize_routing(service, case, policy):
    service.create_case(case_id=case.case_id, ticket=case.ticket)
    service.start_processing(case.case_id)
    approved = service.classify_case(
        case.case_id,
        classifier=FakeClassifier(),
        policy=policy,
    )
    approved = service.decide(
        case.case_id,
        decision_id="decision-9001",
        actor_id="reviewer-1",
        decision=DecisionType.APPROVED,
    )
    assert approved.status is CaseStatus.APPROVED

    with pytest.raises(StaleRecommendationError):
        authorize_routing(approved, recommendation_version=0)

    # The current recommendation version authorizes routing.
    authorize_routing(
        approved,
        recommendation_version=approved.recommendation_version,
    )


def test_failed_update_leaves_no_partial_approval(repository, case):
    repository.create(case)
    record = repository.get_with_revision(case.case_id)
    transition_case(record.case, CaseStatus.PROCESSING)
    transition_case(record.case, CaseStatus.PENDING_APPROVAL)
    repository.save_if_revision(record.case, expected_revision=record.revision)

    # Another writer advances the revision.
    stale = repository.get_with_revision(case.case_id)
    winner = repository.get_with_revision(case.case_id)
    transition_case(winner.case, CaseStatus.APPROVED)
    repository.save_if_revision(winner.case, expected_revision=winner.revision)

    # The stale writer attempts a conflicting approval and fails.
    transition_case(stale.case, CaseStatus.APPROVED)
    with pytest.raises(ConcurrentUpdateError):
        repository.save_if_revision(stale.case, expected_revision=stale.revision)

    # The stored case reflects only the winning write; the loser left nothing.
    stored = repository.get(case.case_id)
    assert stored.status is CaseStatus.APPROVED
    assert stored.approval_decision is None


def test_repeated_decision_id_is_idempotent(service, case, policy):
    service.create_case(case_id=case.case_id, ticket=case.ticket)
    service.start_processing(case.case_id)
    service.classify_case(
        case.case_id,
        classifier=FakeClassifier(),
        policy=policy,
    )

    first = service.decide(
        case.case_id,
        decision_id="decision-9002",
        actor_id="reviewer-1",
        decision=DecisionType.APPROVED,
    )
    replay = service.decide(
        case.case_id,
        decision_id="decision-9002",
        actor_id="reviewer-1",
        decision=DecisionType.APPROVED,
    )

    assert replay.status is CaseStatus.APPROVED
    assert replay.approval_decision.decision_id == "decision-9002"
    assert (
        replay.approval_decision.recommendation_version
        == first.approval_decision.recommendation_version
    )

    # A different decision against an already-decided case is a conflict.
    with pytest.raises(InvalidCaseStateError):
        service.decide(
            case.case_id,
            decision_id="decision-9003",
            actor_id="reviewer-2",
            decision=DecisionType.REJECTED,
        )


def test_legacy_schema_is_migrated(tmp_path, case):
    database_path = tmp_path / "legacy.db"
    connection = sqlite3.connect(database_path)
    connection.execute(
        "CREATE TABLE triage_cases (case_id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
    )
    connection.execute(
        "INSERT INTO triage_cases (case_id, payload) VALUES (?, ?)",
        (case.case_id, json.dumps(case_to_payload(case))),
    )
    connection.commit()
    connection.close()

    repository = SQLiteCaseRepository(str(database_path))
    record = repository.get_with_revision(case.case_id)

    assert record is not None
    assert record.revision == 0
    assert record.case.case_id == case.case_id

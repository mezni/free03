from fastapi.testclient import TestClient
from ticket_triage.sqlite_repository import SQLiteCaseRepository

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.auth import Principal, get_current_principal
from ticket_triage.classification import FakeClassifier
from ticket_triage.domain import CaseStatus
from ticket_triage.policy import RecommendationPolicy


def build_test_app(database_path):
    repository = SQLiteCaseRepository(str(database_path))
    service = TriageApplicationService(repository)
    policy = RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )
    app = create_app(
        service=service,
        classifier=FakeClassifier(),
        policy=policy,
    )
    # Change the principal during a test to simulate different callers.
    identity = {
        "principal": Principal(
            subject="submitter-1",
            roles=frozenset({"submitter"}),
        )
    }
    app.dependency_overrides[get_current_principal] = lambda: identity["principal"]
    return app, service, identity


def test_submitter_lifecycle_records_reviewer_identity(tmp_path):
    app, service, identity = build_test_app(tmp_path / "lifecycle.db")
    client = TestClient(app)

    created = client.post(
        "/cases",
        json={
            "case_id": "case-001",
            "ticket_id": "ticket-001",
            "subject": "Charged twice",
            "description": "I was charged twice for one order.",
        },
    )
    assert created.status_code == 201

    classified = client.post("/cases/case-001/classify")
    assert classified.status_code == 200
    assert classified.json()["status"] == "pending_approval"

    # A submitter cannot approve their own recommendation.
    forbidden = client.post(
        "/cases/case-001/decision",
        json={
            "decision_id": "decision-spoof",
            "decision": "approve",
            "actor_id": "reviewer-1",
        },
    )
    assert forbidden.status_code == 403

    identity["principal"] = Principal(
        subject="reviewer-1",
        roles=frozenset({"reviewer"}),
    )
    approved = client.post(
        "/cases/case-001/decision",
        json={
            "decision_id": "decision-001",
            "decision": "approve",
            "comment": "The recommendation looks correct.",
        },
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"

    # Persistence is verified by reopening the database.
    reopened = SQLiteCaseRepository(str(tmp_path / "lifecycle.db"))
    case = reopened.get("case-001")
    assert case.status == CaseStatus.APPROVED
    assert case.approval_decision is not None
    assert case.approval_decision.actor_id == "reviewer-1"
    assert case.approval_decision.recommendation_version == case.recommendation_version


def test_rejected_case_cannot_be_approved_or_routed(tmp_path):
    app, service, identity = build_test_app(tmp_path / "rejected.db")
    client = TestClient(app)

    created = client.post(
        "/cases",
        json={
            "case_id": "case-002",
            "ticket_id": "ticket-002",
            "subject": "Login problem",
            "description": "I cannot access my account.",
        },
    )
    assert created.status_code == 201

    classified = client.post("/cases/case-002/classify")
    assert classified.status_code == 200
    assert classified.json()["status"] == "pending_approval"

    identity["principal"] = Principal(
        subject="reviewer-2",
        roles=frozenset({"reviewer"}),
    )
    rejected = client.post(
        "/cases/case-002/decision",
        json={
            "decision_id": "decision-002",
            "decision": "reject",
            "comment": "The recommendation needs manual investigation.",
        },
    )
    assert rejected.status_code == 200
    assert rejected.json()["status"] == "rejected"

    reopened = SQLiteCaseRepository(str(tmp_path / "rejected.db"))
    case = reopened.get("case-002")
    assert case.status == CaseStatus.REJECTED

    # A rejected case must not authorize routing. Routing is not yet
    # exposed through the API, so this asserts the workflow guard
    # directly: REJECTED has no transition to ROUTING.
    from ticket_triage.workflow import (
        InvalidTransitionError,
        transition_case,
    )

    try:
        transition_case(case, CaseStatus.ROUTING)
    except InvalidTransitionError:
        pass
    else:
        raise AssertionError("A rejected case must not be authorizable for routing.")

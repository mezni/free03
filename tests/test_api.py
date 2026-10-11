from fastapi.testclient import TestClient
from ticket_triage.sqlite_repository import SQLiteCaseRepository

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.auth import Principal, get_current_principal
from ticket_triage.classification import FakeClassifier
from ticket_triage.policy import RecommendationPolicy


def make_client(tmp_path):
    repository = SQLiteCaseRepository(str(tmp_path / "api-test.db"))
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
    app.dependency_overrides[get_current_principal] = lambda: Principal(
        subject="test-submitter",
        roles=frozenset({"submitter"}),
    )
    return TestClient(app)


def new_case(case_id: str, ticket_id: str) -> dict:
    return {
        "case_id": case_id,
        "ticket_id": ticket_id,
        "subject": "Charged twice",
        "description": "I was charged twice for one order.",
    }


def test_health_endpoint(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_case_endpoint(tmp_path):
    client = make_client(tmp_path)

    response = client.post("/cases", json=new_case("CASE-701", "T-701"))

    assert response.status_code == 201
    body = response.json()
    assert body["case_id"] == "CASE-701"
    assert body["ticket_id"] == "T-701"
    assert body["status"] == "received"


def test_retrieve_case_endpoint(tmp_path):
    client = make_client(tmp_path)
    client.post("/cases", json=new_case("CASE-702", "T-702"))

    response = client.get("/cases/CASE-702")

    assert response.status_code == 200
    assert response.json()["case_id"] == "CASE-702"
    assert response.json()["status"] == "received"


def test_classify_moves_case_to_pending_approval(tmp_path):
    client = make_client(tmp_path)
    client.post("/cases", json=new_case("CASE-703", "T-703"))

    response = client.post("/cases/CASE-703/classify")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "pending_approval"
    assert body["recommendation"]["category"] == "billing"


def test_case_endpoint_requires_authentication(tmp_path):
    service = TriageApplicationService(
        SQLiteCaseRepository(str(tmp_path / "unauth.db"))
    )
    policy = RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )
    app = create_app(service, FakeClassifier(), policy)
    client = TestClient(app)

    response = client.get("/cases/missing-case")

    assert response.status_code == 401


def test_submitter_cannot_approve(tmp_path):
    client = make_client(tmp_path)
    created = client.post(
        "/cases",
        json={
            "case_id": "case-100",
            "ticket_id": "ticket-100",
            "subject": "Charged twice",
            "description": "I was charged twice for one order.",
        },
    )
    assert created.status_code == 201

    response = client.post(
        "/cases/case-100/decision",
        json={
            "decision_id": "decision-100",
            "decision": "approve",
        },
    )

    assert response.status_code == 403

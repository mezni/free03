from fastapi.testclient import TestClient

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.classification import FakeClassifier
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.sqlite_repository import SQLiteCaseRepository


def make_client(tmp_path):
    repository = SQLiteCaseRepository(
        str(tmp_path / "api-test.db")
    )
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
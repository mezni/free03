from fastapi.testclient import TestClient

from ticket_triage.api import create_app
from ticket_triage.application import TriageApplicationService
from ticket_triage.auth import Principal, get_current_principal
from ticket_triage.classification import FakeClassifier
from ticket_triage.classification_worker import handle_classification_job
from ticket_triage.domain import CaseStatus
from ticket_triage.job_queue import SQLiteJobQueue, process_one
from ticket_triage.policy import RecommendationPolicy
from ticket_triage.sqlite_repository import SQLiteCaseRepository


def make_policy() -> RecommendationPolicy:
    return RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )


def make_client(tmp_path, job_queue=None):
    repository = SQLiteCaseRepository(str(tmp_path / "api-test.db"))
    service = TriageApplicationService(repository)
    app = create_app(
        service=service,
        classifier=FakeClassifier(),
        policy=make_policy(),
        job_queue=job_queue,
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
    app = create_app(
        service=service,
        classifier=FakeClassifier(),
        policy=policy,
    )
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


def test_health_endpoint_returns_correlation_id(tmp_path):
    client = make_client(tmp_path)

    response = client.get(
        "/health",
        headers={"X-Correlation-ID": "integration-test-123"},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == "integration-test-123"


def test_invalid_correlation_id_is_replaced(tmp_path):
    client = make_client(tmp_path)

    response = client.get(
        "/health",
        headers={"X-Correlation-ID": "invalid id with spaces"},
    )

    assert response.status_code == 200
    returned_id = response.headers["X-Correlation-ID"]

    assert returned_id != "invalid id with spaces"
    assert 1 <= len(returned_id) <= 100


def test_submitter_cannot_reject_case(tmp_path):
    client = make_client(tmp_path)
    client.post(
        "/cases",
        json={
            "case_id": "case-101",
            "ticket_id": "ticket-101",
            "subject": "Charged twice",
            "description": "I was charged twice for one order.",
        },
    )

    response = client.post(
        "/cases/case-101/decision",
        json={
            "decision_id": "decision-101",
            "decision": "reject",
        },
    )

    assert response.status_code == 403


def test_decision_body_cannot_override_actor_identity(tmp_path):
    client = make_client(tmp_path)
    client.app.dependency_overrides[get_current_principal] = lambda: Principal(
        subject="reviewer-1",
        roles=frozenset({"reviewer"}),
    )

    response = client.post(
        "/cases/case-200/decision",
        json={
            "decision_id": "decision-200",
            "decision": "approve",
            "actor_id": "reviewer-spoofed",
        },
    )

    assert response.status_code == 422


def test_classify_async_accepts_job_with_202(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    client = make_client(tmp_path, job_queue=queue)
    client.post("/cases", json=new_case("CASE-800", "T-800"))

    response = client.post("/cases/CASE-800/classify-async")

    assert response.status_code == 202
    assert response.json() == {
        "case_id": "CASE-800",
        "job_id": "classify:CASE-800",
        "job_status": "queued",
        "message": "Classification has been accepted for processing.",
    }
    assert queue.get_status("classify:CASE-800") == "queued"


def test_classify_async_is_idempotent(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    client = make_client(tmp_path, job_queue=queue)
    client.post("/cases", json=new_case("CASE-801", "T-801"))

    first = client.post("/cases/CASE-801/classify-async")
    second = client.post("/cases/CASE-801/classify-async")

    assert first.status_code == 202
    assert second.status_code == 202
    assert queue.get_status("classify:CASE-801") == "queued"


def test_classify_async_returns_503_without_queue(tmp_path):
    client = make_client(tmp_path)
    client.post("/cases", json=new_case("CASE-802", "T-802"))

    response = client.post("/cases/CASE-802/classify-async")

    assert response.status_code == 503


def test_classify_async_rejects_case_not_received(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    client = make_client(tmp_path, job_queue=queue)
    client.post("/cases", json=new_case("CASE-803", "T-803"))
    client.post("/cases/CASE-803/classify")

    response = client.post("/cases/CASE-803/classify-async")

    assert response.status_code == 409


def test_classify_async_returns_404_for_unknown_case(tmp_path):
    queue = SQLiteJobQueue(str(tmp_path / "jobs.db"))
    client = make_client(tmp_path, job_queue=queue)

    response = client.post("/cases/missing-case/classify-async")

    assert response.status_code == 404


def test_async_classification_end_to_end(tmp_path):
    database_path = str(tmp_path / "shared.db")
    service = TriageApplicationService(SQLiteCaseRepository(database_path))
    classifier = FakeClassifier()
    policy = make_policy()
    queue = SQLiteJobQueue(database_path)

    app = create_app(
        service=service,
        classifier=classifier,
        policy=policy,
        job_queue=queue,
    )
    app.dependency_overrides[get_current_principal] = lambda: Principal(
        subject="test-submitter",
        roles=frozenset({"submitter"}),
    )
    client = TestClient(app)

    client.post("/cases", json=new_case("CASE-900", "T-900"))
    accepted = client.post("/cases/CASE-900/classify-async")
    assert accepted.status_code == 202

    # The API returned before classification ran: the case is still received.
    assert service.get_case("CASE-900").status == CaseStatus.RECEIVED

    processed = process_one(
        queue,
        lambda job: handle_classification_job(
            job,
            service=service,
            classifier=classifier,
            policy=policy,
        ),
    )
    assert processed is True

    body = client.get("/cases/CASE-900").json()
    assert body["status"] == "pending_approval"
    assert body["recommendation"]["category"] == "billing"

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.api.dependencies import get_db_session


def make_client() -> TestClient:
    return TestClient(create_app())


def test_liveness() -> None:
    response = make_client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness(database_session) -> None:
    response = make_client().get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_reports_database_outage() -> None:
    client = make_client()

    failing = MagicMock()
    failing.execute.side_effect = RuntimeError("connection refused: host=db.internal user=rag")

    client.app.dependency_overrides[get_db_session] = lambda: failing

    response = client.get("/health/ready")

    client.app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"] == "Database is unavailable."
    assert "db.internal" not in response.text
    assert "connection refused" not in response.text


def test_security_headers_present() -> None:
    response = make_client().get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"


def test_openapi_documentation_enabled() -> None:
    client = make_client()

    openapi = client.get("/openapi.json")

    assert openapi.status_code == 200
    assert openapi.json()["info"]["title"] == "rag-system"
    assert openapi.json()["info"]["version"] == "1.0.0"

    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200

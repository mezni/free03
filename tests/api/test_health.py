from fastapi.testclient import TestClient

from src.api.app import create_app


def test_health() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }
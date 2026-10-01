"""Readiness and error response behavior."""

from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from src.api.app import create_app
from src.api.dependencies import get_db_session
from src.api.routes.health import readiness
from src.core.exceptions import (
    GenerationError,
    ProviderTimeoutError,
    RetrievalError,
)


class TestReadiness:
    def test_ready_returns_200(self) -> None:
        client = TestClient(create_app())

        response = client.get("/health/ready")

        assert response.status_code == 200
        assert response.json() == {"status": "ready"}

    def test_ready_uses_db_dependency(self) -> None:
        class FailingSession:
            def execute(self, query):
                raise SQLAlchemyError("connection refused")

            def close(self):
                pass

        client = TestClient(create_app())
        client.app.dependency_overrides[get_db_session] = (
            lambda: iter([FailingSession()])
        )

        response = client.get("/health/ready")

        assert response.status_code == 503
        assert response.json()["detail"] == "Database is unavailable."

    def test_readiness_exception_is_not_leaked(self) -> None:
        class FailingSession:
            def execute(self, query):
                raise RuntimeError(
                    "password=supersecret host=internal.example"
                )

            def close(self):
                pass

        client = TestClient(app=create_app(), raise_server_exceptions=False)
        client.app.dependency_overrides[get_db_session] = (
            lambda: iter([FailingSession()])
        )

        response = client.get("/health/ready")

        assert response.status_code == 503
        assert "supersecret" not in response.text
        assert "password" not in response.text


def _app():
    return create_app()


class TestErrorSanitization:
    def test_provider_timeout_returns_504_with_request_id(self) -> None:
        client = TestClient(_app(), raise_server_exceptions=False)

        @client.app.get("/boom/timeout")
        def boom_timeout():
            raise ProviderTimeoutError("LLM provider request timed out.")

        response = client.get("/boom/timeout")

        assert response.status_code == 504
        body = response.json()
        assert body["error"] == "The upstream service timed out."
        assert "request_id" in body

    def test_retrieval_error_returns_503(self) -> None:
        client = TestClient(_app(), raise_server_exceptions=False)

        @client.app.get("/boom/retrieval")
        def boom_retrieval():
            raise RetrievalError("fail")

        response = client.get("/boom/retrieval")

        assert response.status_code == 503
        body = response.json()
        assert body["error"] == "Retrieval service is temporarily unavailable."
        assert "request_id" in body

    def test_generation_error_returns_502(self) -> None:
        client = TestClient(_app(), raise_server_exceptions=False)

        @client.app.get("/boom/generation")
        def boom_generation():
            raise GenerationError("fail")

        response = client.get("/boom/generation")

        assert response.status_code == 502
        body = response.json()
        assert body["error"] == "Answer generation is temporarily unavailable."
        assert "request_id" in body

    def test_exception_message_is_not_leaked_to_client(self) -> None:
        client = TestClient(_app(), raise_server_exceptions=False)

        @client.app.get("/boom/secret")
        def boom_secret():
            raise GenerationError(
                "Authorization: Bearer sk-or-v1-abc123 failed"
            )

        response = client.get("/boom/secret")

        assert response.status_code == 502
        assert "sk-or-v1-abc123" not in response.text
        assert "Authorization" not in response.text

    def test_request_id_consistent_across_middleware_and_error(
        self,
    ) -> None:
        client = TestClient(_app(), raise_server_exceptions=False)

        @client.app.get("/boom/gen")
        def boom_gen():
            raise GenerationError("fail")

        response = client.get("/boom/gen")

        assert response.headers.get("X-Request-ID")
        assert response.headers["X-Request-ID"] == response.json()[
            "request_id"
        ]
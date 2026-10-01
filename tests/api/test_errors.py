import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.api.errors import RAGAPIError, register_exception_handlers


def _app_with_error() -> FastAPI:
    app = create_app()
    register_exception_handlers(app)

    @app.get("/boom")
    def boom():
        raise RAGAPIError(
            "Retrieval backend unavailable.",
            status_code=503,
        )

    return app


class TestRAGAPIError:
    def test_returns_message_and_status(self) -> None:
        client = TestClient(
            _app_with_error(),
            raise_server_exceptions=False,
        )

        response = client.get("/boom")

        assert response.status_code == 503
        assert response.json() == {
            "error": "Retrieval backend unavailable.",
        }

    def test_defaults_to_500(self) -> None:
        error = RAGAPIError("Something broke.")

        assert error.status_code == 500

    def test_unexpected_errors_are_not_masked(self) -> None:
        app = create_app()
        register_exception_handlers(app)

        @app.get("/crash")
        def crash():
            raise RuntimeError("unhandled")

        client = TestClient(
            app,
            raise_server_exceptions=False,
        )

        response = client.get("/crash")

        assert response.status_code == 500

        # Not converted into the RAGAPIError JSON envelope.
        assert "unhandled" not in response.text
        assert not response.text.strip().startswith("{")

    @pytest.mark.parametrize("path", ["/health"])
    def test_health_still_works_with_handlers_registered(
        self,
        path: str,
    ) -> None:
        client = TestClient(_app_with_error())

        response = client.get(path)

        assert response.status_code == 200
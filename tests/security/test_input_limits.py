"""Client-supplied input must stay within configured bounds.

A query or `top_k` chosen by a client directly drives database load,
prompt size, token consumption, latency, and cost, so both limits are
enforced before any retrieval or generation work happens.
"""

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.api.dependencies import get_rag_service
from src.models.rag import Citation, RAGResponse


class RecordingRAGService:
    """Fails loudly if the endpoint lets an invalid request through."""

    def __init__(self) -> None:
        # Instance attribute, not a class attribute: a class-level list
        # would be shared across tests and hide the real call count.
        self.calls: list = []

    def answer(self, query):
        self.calls.append(query)

        return RAGResponse(
            query=query.query,
            answer="Answer. [SOURCE-1]",
            citations=[
                Citation(
                    citation_id="SOURCE-1",
                    document_id="doc-1",
                    chunk_id="chunk-1",
                    chunk_index=0,
                )
            ],
            model_name="fake-model",
            retrieved_count=1,
        )


@pytest.fixture
def service() -> RecordingRAGService:
    return RecordingRAGService()


@pytest.fixture
def client(service: RecordingRAGService) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_rag_service] = lambda: service

    return TestClient(app)


def _post(client: TestClient, payload: dict):
    return client.post("/rag/query", json=payload)


class TestQueryLength:
    def test_query_too_long(self, client: TestClient) -> None:
        response = _post(client, {"query": "x" * 5001})

        assert response.status_code == 422

    def test_query_at_limit_is_accepted(
        self,
        client: TestClient,
    ) -> None:
        response = _post(client, {"query": "x" * 5000})

        assert response.status_code == 200

    def test_empty_query_rejected(self, client: TestClient) -> None:
        assert _post(client, {"query": ""}).status_code == 422

    def test_query_one_over_limit_rejected(
        self,
        client: TestClient,
    ) -> None:
        assert _post(client, {"query": "x" * 5001}).status_code == 422


class TestTopK:
    def test_top_k_too_large(self, client: TestClient) -> None:
        response = _post(
            client,
            {"query": "test", "top_k": 21},
        )

        assert response.status_code == 422

    @pytest.mark.parametrize("top_k", [0, -1, 21, 10_000])
    def test_out_of_range_top_k_rejected(
        self,
        client: TestClient,
        top_k: int,
    ) -> None:
        response = _post(
            client,
            {"query": "test", "top_k": top_k},
        )

        assert response.status_code == 422

    @pytest.mark.parametrize("top_k", [1, 5, 20])
    def test_in_range_top_k_accepted(
        self,
        client: TestClient,
        top_k: int,
    ) -> None:
        response = _post(
            client,
            {"query": "test", "top_k": top_k},
        )

        assert response.status_code == 200

    def test_candidate_k_cannot_be_injected(
        self,
        client: TestClient,
    ) -> None:
        """Clients must not widen the candidate pool directly."""
        response = _post(
            client,
            {
                "query": "test",
                "top_k": 1,
                "candidate_k": 1000,
            },
        )

        assert response.status_code == 422

    def test_unknown_fields_rejected(
        self,
        client: TestClient,
    ) -> None:
        response = _post(
            client,
            {"query": "test", "filters": {"source": "secret"}},
        )

        assert response.status_code == 422


class TestRejectedRequestsDoNoWork:
    def test_oversized_query_never_reaches_service(
        self,
        client: TestClient,
        service: RecordingRAGService,
    ) -> None:
        _post(client, {"query": "x" * 5001})

        assert service.calls == []

    def test_oversized_top_k_never_reaches_service(
        self,
        client: TestClient,
        service: RecordingRAGService,
    ) -> None:
        _post(client, {"query": "test", "top_k": 999})

        assert service.calls == []

    def test_valid_request_does_reach_service(
        self,
        client: TestClient,
        service: RecordingRAGService,
    ) -> None:
        """Guards the tests above from passing because the service is
        never invoked at all."""
        response = _post(
            client,
            {"query": "test", "top_k": 5},
        )

        assert response.status_code == 200
        assert len(service.calls) == 1
        assert service.calls[0].top_k == 5

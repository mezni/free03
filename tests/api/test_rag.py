from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.api.dependencies import get_rag_service
from src.models.rag import Citation, RAGResponse


class FakeRAGService:
    def answer(self, query):
        return RAGResponse(
            query=query.query,
            answer="The billing policy is described in the source. [SOURCE-1]",
            citations=[
                Citation(
                    citation_id="SOURCE-1",
                    document_id=str(uuid4()),
                    chunk_id=str(uuid4()),
                    chunk_index=0,
                )
            ],
            model_name="fake-model",
            retrieved_count=1,
        )


def test_rag_query() -> None:
    app = create_app()

    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()

    client = TestClient(app)

    response = client.post(
        "/rag/query",
        json={
            "query": "What is the billing policy?",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == ("What is the billing policy?")

    assert body["model_name"] == "fake-model"
    assert body["retrieved_count"] == 1
    assert len(body["citations"]) == 1


def test_rag_query_forwards_top_k() -> None:
    app = create_app()

    rag_service = FakeRAGService()
    seen: list[int] = []

    def override():
        return rag_service

    original_answer = rag_service.answer

    def recording_answer(query):
        seen.append(query.top_k)

        return original_answer(query)

    rag_service.answer = recording_answer

    app.dependency_overrides[get_rag_service] = override

    client = TestClient(app)

    response = client.post(
        "/rag/query",
        json={
            "query": "What is the billing policy?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200
    assert seen == [3]


def test_rag_query_defaults_top_k_to_five() -> None:
    app = create_app()

    seen: list[int] = []

    class RecordingRAGService(FakeRAGService):
        def answer(self, query):
            seen.append(query.top_k)

            return super().answer(query)

    app.dependency_overrides[get_rag_service] = lambda: RecordingRAGService()

    client = TestClient(app)

    response = client.post(
        "/rag/query",
        json={"query": "What is the billing policy?"},
    )

    assert response.status_code == 200
    assert seen == [5]


def test_rag_query_rejects_empty_query() -> None:
    app = create_app()

    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()

    client = TestClient(app)

    response = client.post(
        "/rag/query",
        json={"query": ""},
    )

    assert response.status_code == 422


def test_rag_query_rejects_unknown_field() -> None:
    app = create_app()

    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()

    client = TestClient(app)

    response = client.post(
        "/rag/query",
        json={
            "query": "What is the billing policy?",
            "unexpected": True,
        },
    )

    assert response.status_code == 422


def test_rag_query_rejects_out_of_range_top_k() -> None:
    app = create_app()

    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()

    client = TestClient(app)

    for top_k in (0, 21):
        response = client.post(
            "/rag/query",
            json={
                "query": "What is the billing policy?",
                "top_k": top_k,
            },
        )

        assert response.status_code == 422


def test_openapi_schema_is_generated() -> None:
    app = create_app()

    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    assert "/rag/query" in schema["paths"]
    assert "/health" in schema["paths"]

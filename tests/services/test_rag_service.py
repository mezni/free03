from uuid import uuid4

from src.models.generation import GenerationResponse
from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.services.rag_service import RAGService


class FakeRetrievalPipeline:
    def __init__(self, results):
        self.results = results
        self.queries = []

    def execute(self, query):
        self.queries.append(query)

        return self.results


class FakeGenerationService:
    def __init__(self, answer: str) -> None:
        self.answer_text = answer
        self.calls = []

    def generate(self, query, results):
        self.calls.append((query, results))

        return GenerationResponse(
            answer=self.answer_text,
            model_name="fake-model",
        )


def make_result() -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content="Refunds are issued within 5 days.",
        chunk_index=0,
        score=0.5,
        retrieval_method="vector",
    )


def test_answer_retrieves_then_generates():
    result = make_result()

    pipeline = FakeRetrievalPipeline([result])
    generation = FakeGenerationService("Refunds take 5 days.")

    service = RAGService(
        retrieval_pipeline=pipeline,
        generation_service=generation,
    )

    query = RetrievalQuery(query="Refund window?", top_k=5)

    response = service.answer(query)

    assert response.answer == "Refunds take 5 days."

    assert pipeline.queries == [query]

    assert generation.calls == [
        ("Refund window?", [result]),
    ]


def test_answer_forwards_empty_results_to_generation():
    pipeline = FakeRetrievalPipeline([])
    generation = FakeGenerationService("No context.")

    service = RAGService(
        retrieval_pipeline=pipeline,
        generation_service=generation,
    )

    service.answer(
        RetrievalQuery(query="Refund window?", top_k=5)
    )

    assert generation.calls == [
        ("Refund window?", []),
    ]

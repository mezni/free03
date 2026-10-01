from uuid import uuid4

from src.generation.citations import CitationExtractor
from src.generation.context_builder import ContextBuilder
from src.generation.prompt_builder import PromptBuilder
from src.models.generation import GenerationResponse
from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.services.generation_service import GenerationService
from src.services.grounding_service import GroundingService
from src.services.rag_service import RAGService


def make_result(content: str = "content") -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=0,
        score=0.5,
        retrieval_method="vector",
    )


class FakeRetrievalPipeline:
    def __init__(self, results) -> None:
        self.results = results
        self.queries = []

    def execute(self, query):
        self.queries.append(query)

        return self.results


class FakeLLMProvider:
    model_name = "fake-model"

    def __init__(self, answer: str) -> None:
        self.answer = answer
        self.requests = []

    def generate(self, request):
        self.requests.append(request)

        return GenerationResponse(
            answer=self.answer,
            model_name=self.model_name,
        )


def make_rag_service(
    results,
    answer: str,
):
    pipeline = FakeRetrievalPipeline(results)
    provider = FakeLLMProvider(answer)

    generation = GenerationService(
        llm_provider=provider,
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        citation_extractor=CitationExtractor(),
        grounding_service=GroundingService(),
    )

    service = RAGService(
        retrieval_pipeline=pipeline,
        generation_service=generation,
    )

    return service, pipeline, provider


def test_end_to_end_answer_with_citation():
    result = make_result()

    service, pipeline, _ = make_rag_service(
        [result],
        "Disputes are filed within 30 days. [SOURCE-1]",
    )

    response = service.answer(
        RetrievalQuery(
            query="What is the billing policy?",
            top_k=5,
        )
    )

    assert response.query == "What is the billing policy?"
    assert response.answer
    assert response.retrieved_count == 1
    assert len(response.citations) == 1

    assert response.citations[0].citation_id == "SOURCE-1"
    assert response.citations[0].chunk_id == str(result.chunk_id)


def test_end_to_end_forwards_top_k_to_retrieval():
    service, pipeline, _ = make_rag_service(
        [make_result()],
        "answer [SOURCE-1]",
    )

    query = RetrievalQuery(
        query="What is the billing policy?",
        top_k=3,
    )

    service.answer(query)

    assert pipeline.queries == [query]


def test_end_to_end_citation_maps_to_correct_source():
    first = make_result("first content")
    second = make_result("second content")

    service, _, _ = make_rag_service(
        [first, second],
        "Two answers. [SOURCE-2]",
    )

    response = service.answer(
        RetrievalQuery(query="query", top_k=5)
    )

    assert len(response.citations) == 1
    assert response.citations[0].citation_id == "SOURCE-2"
    assert response.citations[0].chunk_id == str(second.chunk_id)


def test_end_to_end_without_results_skips_provider():
    service, pipeline, provider = make_rag_service([], "unused")

    response = service.answer(
        RetrievalQuery(query="query", top_k=5)
    )

    assert response.retrieved_count == 0
    assert response.citations == []
    assert "could not find relevant information" in response.answer
    assert provider.requests == []


def test_end_to_end_without_citations_reports_none():
    service, _, _ = make_rag_service(
        [make_result()],
        "An answer with no source marker.",
    )

    response = service.answer(
        RetrievalQuery(query="query", top_k=5)
    )

    assert response.retrieved_count == 1
    assert response.citations == []

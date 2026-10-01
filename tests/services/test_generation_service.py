from uuid import uuid4

from src.generation.citations import CitationExtractor
from src.generation.context_builder import ContextBuilder
from src.generation.prompt_builder import PromptBuilder
from src.models.generation import GenerationResponse
from src.models.llm_usage import LLMUsageRecord
from src.models.retrieval import RetrievalResult
from src.observability.metrics import MetricsCollector
from src.services.generation_service import GenerationService
from src.services.grounding_service import GroundingService


def make_result(
    content: str = "Billing disputes are filed within 30 days.",
    chunk_index: int = 0,
) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=uuid4(),
        index_version_id=uuid4(),
        content=content,
        chunk_index=chunk_index,
        score=0.5,
        retrieval_method="vector",
    )


class FakeLLMProvider:
    model_name = "fake-model"

    def __init__(self, answer: str | None = None) -> None:
        self.answer = answer or (
            "The billing policy allows disputes within the specified period. [SOURCE-1]"
        )
        self.requests = []

    def generate(self, request):
        self.requests.append(request)

        return GenerationResponse(
            answer=self.answer,
            model_name=self.model_name,
        )


class TokenReportingLLMProvider(FakeLLMProvider):
    def generate(self, request):
        self.requests.append(request)

        return GenerationResponse(
            answer=self.answer,
            model_name=self.model_name,
            prompt_tokens=1_000,
            completion_tokens=500,
            total_tokens=1_500,
        )


class FakeUsageTracker:
    def __init__(self) -> None:
        self.recorded = []

    def record(self, response, request_id=None):
        usage = LLMUsageRecord(
            provider="openrouter",
            model_name=response.model_name,
            prompt_tokens=response.prompt_tokens or 0,
            completion_tokens=response.completion_tokens or 0,
            total_tokens=response.total_tokens or 0,
            estimated_cost=0.02,
            currency="USD",
        )

        self.recorded.append(usage)

        return usage


def make_service(
    provider: FakeLLMProvider | None = None,
    usage_tracker: FakeUsageTracker | None = None,
    metrics: MetricsCollector | None = None,
) -> GenerationService:
    return GenerationService(
        llm_provider=provider or FakeLLMProvider(),
        context_builder=ContextBuilder(),
        prompt_builder=PromptBuilder(),
        citation_extractor=CitationExtractor(),
        grounding_service=GroundingService(),
        usage_tracker=usage_tracker,
        metrics=metrics,
    )


def test_generation_returns_citations():
    service = make_service()

    response = service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    assert response.citations
    assert response.citations[0].citation_id == "SOURCE-1"


def test_generation_returns_query_and_counts():
    service = make_service()

    response = service.generate(
        query="What is the billing policy?",
        results=[make_result(), make_result(chunk_index=1)],
    )

    assert response.query == "What is the billing policy?"
    assert response.retrieved_count == 2
    assert response.model_name == "fake-model"


def test_generation_citation_points_at_retrieved_chunk():
    result = make_result()

    service = make_service()

    response = service.generate(
        query="What is the billing policy?",
        results=[result],
    )

    citation = response.citations[0]

    assert citation.chunk_id == str(result.chunk_id)
    assert citation.document_id == str(result.document_id)
    assert citation.chunk_index == 0


def test_generation_sends_prebuilt_prompts():
    provider = FakeLLMProvider()

    service = make_service(provider)

    service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    request = provider.requests[0]

    assert "[SOURCE-N]" in request.system_prompt
    assert "[SOURCE-1]" in request.user_prompt
    assert "30 days" in request.user_prompt


def test_generation_omits_citations_when_absent():
    service = make_service(FakeLLMProvider(answer="No citation here."))

    response = service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    assert response.citations == []


def test_generation_returns_fallback_when_no_context():
    provider = FakeLLMProvider()

    service = make_service(provider)

    response = service.generate(
        query="What is the billing policy?",
        results=[],
    )

    assert "could not find relevant information" in response.answer
    assert response.citations == []
    assert response.retrieved_count == 0
    assert provider.requests == []


def test_generation_records_usage_after_provider_call():
    provider = TokenReportingLLMProvider()
    tracker = FakeUsageTracker()

    service = make_service(
        provider,
        usage_tracker=tracker,
    )

    service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    assert len(tracker.recorded) == 1

    usage = tracker.recorded[0]

    assert usage.provider == "openrouter"
    assert usage.prompt_tokens == 1_000
    assert usage.completion_tokens == 500
    assert usage.total_tokens == 1_500


def test_generation_increments_llm_metrics():
    metrics = MetricsCollector()

    service = make_service(
        TokenReportingLLMProvider(),
        usage_tracker=FakeUsageTracker(),
        metrics=metrics,
    )

    service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    assert metrics.get("llm.requests") == 1
    assert metrics.get("llm.prompt_tokens") == 1_000
    assert metrics.get("llm.completion_tokens") == 500
    assert metrics.get("llm.total_tokens") == 1_500
    assert metrics.get_total("llm.estimated_cost") == 0.02


def test_generation_without_context_records_no_usage():
    tracker = FakeUsageTracker()

    service = make_service(usage_tracker=tracker)

    service.generate(
        query="What is the billing policy?",
        results=[],
    )

    assert tracker.recorded == []


def test_generation_without_tracker_still_counts_tokens():
    metrics = MetricsCollector()

    service = make_service(
        TokenReportingLLMProvider(),
        metrics=metrics,
    )

    service.generate(
        query="What is the billing policy?",
        results=[make_result()],
    )

    assert metrics.get("llm.requests") == 1
    assert metrics.get_total("llm.estimated_cost") == 0.0

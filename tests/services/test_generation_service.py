from uuid import uuid4

from src.generation.context_builder import ContextBuilder
from src.models.generation import GenerationResponse
from src.models.retrieval import RetrievalResult
from src.services.generation_service import GenerationService


def make_result(
    document_id,
    chunk_index: int,
    content: str,
) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=uuid4(),
        document_id=document_id,
        index_version_id=uuid4(),
        content=content,
        chunk_index=chunk_index,
        score=0.5,
        retrieval_method="vector",
    )


class FakeLLMProvider:
    model_name = "fake-model"

    def __init__(self) -> None:
        self.requests = []

    def generate(self, request):
        self.requests.append(request)

        return GenerationResponse(
            answer="The answer is in the provided context.",
            model_name=self.model_name,
        )


def test_generation_uses_retrieved_context():
    service = GenerationService(
        llm_provider=FakeLLMProvider(),
        context_builder=ContextBuilder(),
    )

    results = [
        make_result(
            uuid4(),
            0,
            "Billing disputes must be filed within 30 days.",
        ),
    ]

    response = service.generate(
        query="What is the billing policy?",
        results=results,
    )

    assert response.answer
    assert response.model_name == "fake-model"


def test_generation_passes_context_and_query_to_provider():
    provider = FakeLLMProvider()

    service = GenerationService(
        llm_provider=provider,
        context_builder=ContextBuilder(),
    )

    results = [
        make_result(
            uuid4(),
            0,
            "Billing disputes must be filed within 30 days.",
        ),
    ]

    service.generate(
        query="What is the billing policy?",
        results=results,
    )

    assert len(provider.requests) == 1

    request = provider.requests[0]

    assert request.query == "What is the billing policy?"
    assert "30 days" in request.context
    assert "Document:" in request.context


def test_generation_returns_fallback_when_no_context():
    service = GenerationService(
        llm_provider=FakeLLMProvider(),
        context_builder=ContextBuilder(),
    )

    response = service.generate(
        query="What is the billing policy?",
        results=[],
    )

    assert "could not find relevant information" in response.answer
    assert response.model_name == "fake-model"


def test_generation_does_not_call_provider_without_context():
    provider = FakeLLMProvider()

    service = GenerationService(
        llm_provider=provider,
        context_builder=ContextBuilder(),
    )

    service.generate(
        query="What is the billing policy?",
        results=[],
    )

    assert provider.requests == []


def test_generation_calls_provider_when_chunk_content_is_empty():
    """
    A retrieved chunk with no text still yields a provenance header,
    so the context is non-empty and the provider is still called.
    """
    provider = FakeLLMProvider()

    service = GenerationService(
        llm_provider=provider,
        context_builder=ContextBuilder(),
    )

    service.generate(
        query="What is the billing policy?",
        results=[
            make_result(uuid4(), 0, ""),
        ],
    )

    assert len(provider.requests) == 1
    assert "Document:" in provider.requests[0].context
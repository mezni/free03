from src.generation.context_builder import ContextBuilder
from src.models.generation import (
    GenerationRequest,
    GenerationResponse,
)
from src.models.retrieval import RetrievalResult
from src.providers.llm.base import LLMProvider


class GenerationService:
    """Generate answers grounded in retrieved context."""

    def __init__(
        self,
        llm_provider: LLMProvider,
        context_builder: ContextBuilder,
    ) -> None:
        self._llm_provider = llm_provider
        self._context_builder = context_builder

    def generate(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> GenerationResponse:
        context = self._context_builder.build(results)

        if not context:
            return GenerationResponse(
                answer=(
                    "I could not find relevant information "
                    "in the knowledge base."
                ),
                model_name=self._llm_provider.model_name,
            )

        request = GenerationRequest(
            query=query,
            context=context,
        )

        return self._llm_provider.generate(request)

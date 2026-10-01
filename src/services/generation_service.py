import logging

from src.generation.citations import CitationExtractor
from src.generation.context_builder import ContextBuilder
from src.generation.prompt_builder import PromptBuilder
from src.models.generation import (
    GenerationRequest,
    GenerationResponse,
)
from src.models.rag import RAGResponse
from src.models.retrieval import RetrievalResult
from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics
from src.observability.timer import Timer
from src.providers.llm.base import LLMProvider
from src.services.grounding_service import GroundingService

logger = logging.getLogger("rag-system.generation")


class GenerationService:
    """Generate a cited, grounded answer from retrieved context."""

    def __init__(
        self,
        llm_provider: LLMProvider,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        citation_extractor: CitationExtractor,
        grounding_service: GroundingService,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self._llm_provider = llm_provider
        self._context_builder = context_builder
        self._prompt_builder = prompt_builder
        self._citation_extractor = citation_extractor
        self._grounding_service = grounding_service
        self._metrics = metrics or get_metrics()

    def generate(
        self,
        query: str,
        results: list[RetrievalResult],
    ) -> RAGResponse:
        if not results:
            return RAGResponse(
                query=query,
                answer=(
                    "I could not find relevant information "
                    "in the knowledge base."
                ),
                citations=[],
                model_name=self._llm_provider.model_name,
                retrieved_count=0,
            )

        system_prompt = self._prompt_builder.build_system_prompt()

        user_prompt = self._prompt_builder.build_user_prompt(
            query=query,
            results=results,
        )

        request = GenerationRequest(
            query=query,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        self._metrics.increment("generation.requests")

        try:
            with Timer() as timer:
                response: GenerationResponse = (
                    self._llm_provider.generate(request)
                )
        except Exception:
            self._metrics.increment("generation.errors")

            logger.exception(
                "Generation failed",
                extra={
                    "event": "generation.failed",
                    "model": self._llm_provider.model_name,
                },
            )

            raise

        logger.info(
            "Generation completed",
            extra={
                "event": "generation.completed",
                "duration_ms": timer.duration_ms,
                "model": response.model_name,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
            },
        )

        citations = self._citation_extractor.extract(
            answer=response.answer,
            results=results,
        )

        self._grounding_service.validate(
            answer=response.answer,
            citation_count=len(citations),
        )

        return RAGResponse(
            query=query,
            answer=response.answer,
            citations=citations,
            model_name=response.model_name,
            retrieved_count=len(results),
        )
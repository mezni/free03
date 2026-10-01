from src.models.rag import RAGResponse
from src.models.retrieval import RetrievalQuery
from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics
from src.retrieval.pipeline import RetrievalPipeline
from src.services.generation_service import GenerationService


class RAGService:
    """Retrieve relevant context, then generate a grounded answer."""

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
        generation_service: GenerationService,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self._retrieval_pipeline = retrieval_pipeline
        self._generation_service = generation_service
        self._metrics = metrics or get_metrics()

    def answer(
        self,
        query: RetrievalQuery,
    ) -> RAGResponse:
        self._metrics.increment("rag.requests")

        results = self._retrieval_pipeline.execute(query)

        return self._generation_service.generate(
            query=query.query,
            results=results,
        )

import logging

from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics
from src.observability.timer import Timer
from src.retrieval.rerank.base import Reranker
from src.services.retrieval_service import RetrievalService

logger = logging.getLogger("rag-system.retrieval")


class RetrievalPipeline:
    """
    Orchestrates retrieval and reranking.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        reranker: Reranker | None = None,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.reranker = reranker
        self.metrics = metrics or get_metrics()

    def execute(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        self.metrics.increment("retrieval.requests")

        with Timer() as timer:
            candidates = self.retrieval_service.search(request)

            if self.reranker is None:
                results = candidates
            else:
                results = self.reranker.rerank(
                    query=request.query,
                    candidates=candidates,
                    top_k=request.top_k,
                )

        if not results:
            self.metrics.increment("retrieval.empty_results")

        logger.info(
            "Retrieval completed",
            extra={
                "event": "retrieval.completed",
                "duration_ms": timer.duration_ms,
                "retrieved_count": len(results),
            },
        )

        return results
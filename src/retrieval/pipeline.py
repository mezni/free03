import logging

from src.models.query_analysis import QueryAnalysis
from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics
from src.observability.timer import Timer
from src.retrieval.context.base import ContextSelector
from src.retrieval.context.window import ContextWindowService
from src.retrieval.query.base import QueryAnalyzer
from src.retrieval.rerank.base import Reranker
from src.services.retrieval_service import RetrievalService

logger = logging.getLogger("rag-system.retrieval")


class RetrievalPipeline:
    """Orchestrates the advanced retrieval pipeline.

        query
          ↓
        query analysis
          ↓
        hybrid retrieval (candidate pool)
          ↓
        reranking (candidate pool → top_k)
          ↓
        context-window expansion
          ↓
        context selection (max_chunks)

    Every stage is optional and independently testable. Omitting a
    stage must not change the correctness of the remaining ones.

    Tuning knobs default to None, which means "do not impose this
    stage": the request's own top_k drives retrieval and selection.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        query_analyzer: QueryAnalyzer | None = None,
        reranker: Reranker | None = None,
        context_window_service: ContextWindowService | None = None,
        context_selector: ContextSelector | None = None,
        rerank_candidate_k: int | None = None,
        window_size: int = 1,
        max_chunks: int | None = None,
        metrics: MetricsCollector | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.query_analyzer = query_analyzer
        self.reranker = reranker
        self.context_window_service = context_window_service
        self.context_selector = context_selector
        self.rerank_candidate_k = rerank_candidate_k
        self.window_size = window_size
        self.max_chunks = max_chunks
        self.metrics = metrics or get_metrics()

    def execute(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        self.metrics.increment("retrieval.requests")

        analysis = self._analyze(request)

        retrieval_request = request.model_copy(
            update={
                "query": analysis.rewritten_query,
                "filters": analysis.filters,
                "top_k": self._retrieval_depth(request.top_k),
            }
        )

        with Timer() as timer:
            candidates = self.retrieval_service.search(retrieval_request)

            results = self._rerank(
                analysis.rewritten_query,
                candidates,
                request.top_k,
            )

            results = self._expand(results)

            results = self._select(
                results,
                self._context_limit(request.top_k),
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

    def _retrieval_depth(self, top_k: int) -> int:
        """How many candidates to pull before reranking.

        Reranking can only reorder what retrieval returned, so it
        needs a wider pool than the caller's top_k. Never narrower:
        requesting fewer candidates than the caller asked for would
        silently truncate the answer.
        """
        if self.rerank_candidate_k is None:
            return top_k

        return max(top_k, self.rerank_candidate_k)

    def _context_limit(self, top_k: int) -> int:
        """Chunk budget for the final context."""
        if self.max_chunks is None:
            return top_k

        return max(top_k, self.max_chunks)

    def _analyze(
        self,
        request: RetrievalQuery,
    ) -> QueryAnalysis:
        if self.query_analyzer is None:
            # No analyzer configured: pass the query through and keep
            # any filters the caller supplied.
            return QueryAnalysis(
                original_query=request.query,
                rewritten_query=request.query,
                filters=request.filters,
            )

        analysis = self.query_analyzer.analyze(request.query)

        if analysis.filters is None:
            # An analyzer that produces no filters must not silently
            # discard filters the caller already set.
            return analysis.model_copy(update={"filters": request.filters})

        return analysis

    def _rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        top_k: int,
    ) -> list[RetrievalResult]:
        if self.reranker is None:
            return candidates

        return self.reranker.rerank(
            query=query,
            candidates=candidates,
            top_k=top_k,
        )

    def _expand(
        self,
        results: list[RetrievalResult],
    ) -> list[RetrievalResult]:
        if self.context_window_service is None:
            return results

        return self.context_window_service.expand(
            results,
            window=self.window_size,
        )

    def _select(
        self,
        results: list[RetrievalResult],
        max_chunks: int,
    ) -> list[RetrievalResult]:
        if self.context_selector is None:
            return results

        return self.context_selector.select(
            results,
            max_chunks=max_chunks,
        )

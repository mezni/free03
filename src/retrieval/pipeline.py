from typing import Optional

from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.retrieval.rerank.base import Reranker
from src.services.retrieval_service import RetrievalService


class RetrievalPipeline:
    """
    Orchestrates retrieval and reranking.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        reranker: Optional[Reranker] = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.reranker = reranker

    def execute(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        candidates = self.retrieval_service.search(request)

        if self.reranker is None:
            return candidates

        return self.reranker.rerank(
            query=request.query,
            candidates=candidates,
            top_k=request.top_k,
        )
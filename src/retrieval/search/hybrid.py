from src.models.retrieval import RetrievalQuery, RetrievalResult
from src.retrieval.search.base import (
    SearchStrategy,
    reciprocal_rank_fusion,
)


class HybridSearchStrategy(SearchStrategy):
    """
    Combines vector and keyword retrieval using RRF.

    Delegates to the provided vector and keyword strategies,
    then merges their ranked result lists using Reciprocal Rank Fusion.
    """

    def __init__(
        self,
        vector_strategy: SearchStrategy,
        keyword_strategy: SearchStrategy,
        fusion_k: int = 60,
        candidate_multiplier: int = 4,
    ) -> None:
        if fusion_k <= 0:
            raise ValueError("fusion_k must be greater than zero.")

        if candidate_multiplier <= 0:
            raise ValueError(
                "candidate_multiplier must be greater than zero.",
            )

        self.vector_strategy = vector_strategy
        self.keyword_strategy = keyword_strategy
        self.fusion_k = fusion_k
        self.candidate_multiplier = candidate_multiplier

    def search(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        candidate_count = request.candidate_k or (
            request.top_k * self.candidate_multiplier
        )

        candidate_request = request.model_copy(
            update={"top_k": candidate_count},
        )

        vector_results = self.vector_strategy.search(
            candidate_request,
        )

        keyword_results = self.keyword_strategy.search(
            candidate_request,
        )

        fused_results = reciprocal_rank_fusion(
            result_lists=[
                vector_results,
                keyword_results,
            ],
            k=self.fusion_k,
        )

        return fused_results[:candidate_count]
from src.models.retrieval import RetrievalResult
from src.retrieval.rerank.base import Reranker


class SimpleReranker(Reranker):
    """
    Development reranker.

    This implementation preserves the incoming ranking.
    It exists to establish the reranking contract before
    introducing a real reranking model.
    """

    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        top_k: int,
    ) -> list[RetrievalResult]:
        if top_k < 1:
            raise ValueError("top_k must be greater than zero.")

        return [
            candidate.model_copy(
                update={
                    "retrieval_method": "reranked",
                },
            )
            for candidate in candidates[:top_k]
        ]

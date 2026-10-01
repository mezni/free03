from abc import ABC, abstractmethod

from src.models.retrieval import RetrievalResult


class Reranker(ABC):
    """
    Application-level contract for reranking retrieved candidates.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        top_k: int,
    ) -> list[RetrievalResult]:
        """Rerank candidates and return the final top-K results."""
        raise NotImplementedError

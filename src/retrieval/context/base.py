from abc import ABC, abstractmethod

from src.models.retrieval import RetrievalResult


class ContextSelector(ABC):
    """Chooses which ranked results become prompt context.

    Separate from reranking on purpose: reranking decides relevance
    order, context selection decides what actually reaches the prompt.
    Later implementations can weigh token budget, duplicate chunks,
    document diversity, or score thresholds.
    """

    @abstractmethod
    def select(
        self,
        results: list[RetrievalResult],
        max_chunks: int,
    ) -> list[RetrievalResult]:
        raise NotImplementedError
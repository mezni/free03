from src.models.retrieval import RetrievalResult
from src.retrieval.context.base import ContextSelector


class SimpleContextSelector(ContextSelector):
    """Baseline selector: keep the top results in rank order."""

    def select(
        self,
        results: list[RetrievalResult],
        max_chunks: int,
    ) -> list[RetrievalResult]:
        return results[:max_chunks]

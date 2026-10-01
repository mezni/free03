from src.models.query_analysis import QueryAnalysis
from src.retrieval.query.base import QueryAnalyzer


class SimpleQueryAnalyzer(QueryAnalyzer):
    """Baseline analyzer: whitespace normalization only.

    Intentionally trivial. The point is the boundary: a later
    LLM-based analyzer can be substituted without touching the
    retrieval pipeline.
    """

    def analyze(self, query: str) -> QueryAnalysis:
        normalized = " ".join(query.split())

        return QueryAnalysis(
            original_query=query,
            rewritten_query=normalized,
        )

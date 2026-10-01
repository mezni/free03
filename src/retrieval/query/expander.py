from src.models.query_analysis import QueryAnalysis


class QueryExpander:
    """Produce alternative query formulations deterministically.

    Determinism matters: the same analysis must always yield the same
    query list, so retrieval behavior stays reproducible between runs.
    A later LLM-based expander can generate alternatives such as
    "refund policy" or "refund eligibility" without changing any
    surrounding component.
    """

    def expand(self, analysis: QueryAnalysis) -> list[str]:
        queries = [
            analysis.original_query,
            analysis.rewritten_query,
        ]

        return list(dict.fromkeys(queries))

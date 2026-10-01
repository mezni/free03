from src.models.rag import RAGResponse
from src.models.rag_evaluation import RAGEvaluationCase


class CitationEvaluator:
    def evaluate(
        self,
        case: RAGEvaluationCase,
        response: RAGResponse,
    ) -> tuple[float, float]:
        expected = set(case.expected_citations)

        actual = {citation.citation_id for citation in response.citations}

        if not expected and not actual:
            return 1.0, 1.0

        if not actual:
            return 0.0, 0.0

        true_positive = len(expected & actual)

        precision = true_positive / len(actual)

        recall = true_positive / len(expected) if expected else 1.0

        return precision, recall

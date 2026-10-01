from src.models.rag import RAGResponse


class GroundingEvaluator:
    def evaluate(
        self,
        response: RAGResponse,
    ) -> float:
        if not response.answer.strip():
            return 0.0

        if response.retrieved_count == 0:
            return 0.0

        if not response.citations:
            return 0.0

        return 1.0

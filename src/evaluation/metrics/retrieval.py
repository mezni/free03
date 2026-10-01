from src.models.retrieval_evaluation import RetrievalEvaluationResult


class RecallAtK:
    """Calculate Recall@K for a retrieval evaluation result."""

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        k: int,
    ) -> float:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        relevant_ids = set(evaluation.relevant_chunk_ids)
        retrieved_ids = set(evaluation.retrieved_chunk_ids[:k])

        if not relevant_ids:
            return 0.0

        retrieved_relevant = relevant_ids & retrieved_ids

        return len(retrieved_relevant) / len(relevant_ids)
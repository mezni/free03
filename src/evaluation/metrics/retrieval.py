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


class PrecisionAtK:
    """Calculate Precision@K for a retrieval evaluation result."""

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        k: int,
    ) -> float:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        retrieved_ids = evaluation.retrieved_chunk_ids[:k]

        if not retrieved_ids:
            return 0.0

        relevant_ids = set(evaluation.relevant_chunk_ids)
        retrieved_relevant = set(retrieved_ids) & relevant_ids

        return len(retrieved_relevant) / len(retrieved_ids)


class ReciprocalRank:
    """Calculate Reciprocal Rank for a retrieval evaluation result."""

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        k: int,
    ) -> float:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        relevant_ids = set(evaluation.relevant_chunk_ids)

        for rank, chunk_id in enumerate(
            evaluation.retrieved_chunk_ids[:k],
            start=1,
        ):
            if chunk_id in relevant_ids:
                return 1.0 / rank

        return 0.0


class MeanReciprocalRank:
    """Calculate Mean Reciprocal Rank across evaluation results."""

    def calculate(
        self,
        evaluations: list[RetrievalEvaluationResult],
        k: int,
    ) -> float:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        if not evaluations:
            return 0.0

        metric = ReciprocalRank()

        reciprocal_ranks = [
            metric.calculate(evaluation, k)
            for evaluation in evaluations
        ]

        return sum(reciprocal_ranks) / len(reciprocal_ranks)
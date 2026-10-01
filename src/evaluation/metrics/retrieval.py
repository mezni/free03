import math

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

        reciprocal_ranks = [metric.calculate(evaluation, k) for evaluation in evaluations]

        return sum(reciprocal_ranks) / len(reciprocal_ranks)


class ContextRecall:
    """Fraction of relevant chunks that reached the final context.

    Recall@K measures whether retrieval ranked a relevant chunk highly.
    This measures whether it survived into the context the LLM actually
    saw. A pipeline can score perfect Recall@K and still fail here if
    reranking, window expansion, or selection displaced the answer.
    """

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        context_chunk_ids: list[str],
    ) -> float:
        relevant_ids = {str(chunk) for chunk in evaluation.relevant_chunk_ids}

        if not relevant_ids:
            return 0.0

        context_ids = set(context_chunk_ids)

        retrieved_relevant = relevant_ids & context_ids

        return len(retrieved_relevant) / len(relevant_ids)


class ContextPrecision:
    """Fraction of context chunks that are relevant.

    The counterweight to Context Recall. Window expansion deliberately
    adds neighbor chunks that were never independently judged relevant,
    so this metric rises as context grows. A rise in recall paired with
    a fall in precision means the window is padding the prompt.
    """

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        context_chunk_ids: list[str],
    ) -> float:
        if not context_chunk_ids:
            return 0.0

        relevant_ids = {str(chunk) for chunk in evaluation.relevant_chunk_ids}

        context_ids = set(context_chunk_ids)

        return len(relevant_ids & context_ids) / len(context_ids)


class NDCGAtK:
    """Calculate binary Normalized Discounted Cumulative Gain@K."""

    def calculate(
        self,
        evaluation: RetrievalEvaluationResult,
        k: int,
    ) -> float:
        if k <= 0:
            raise ValueError("k must be greater than 0")

        relevant_ids = set(evaluation.relevant_chunk_ids)
        retrieved_ids = evaluation.retrieved_chunk_ids[:k]

        if not relevant_ids:
            return 0.0

        dcg = self._dcg(
            retrieved_ids=retrieved_ids,
            relevant_ids=relevant_ids,
        )

        ideal_count = min(k, len(relevant_ids))

        ideal_retrieved_ids = evaluation.relevant_chunk_ids[:ideal_count]

        ideal_dcg = self._dcg(
            retrieved_ids=ideal_retrieved_ids,
            relevant_ids=relevant_ids,
        )

        if ideal_dcg == 0.0:
            return 0.0

        return dcg / ideal_dcg

    @staticmethod
    def _dcg(
        retrieved_ids,
        relevant_ids,
    ) -> float:
        score = 0.0

        for rank, chunk_id in enumerate(
            retrieved_ids,
            start=1,
        ):
            relevance = 1.0 if chunk_id in relevant_ids else 0.0

            score += relevance / math.log2(rank + 1)

        return score

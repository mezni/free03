import pytest

from src.evaluation.answer.base import AnswerEvaluator
from src.models.rag import Citation, RAGResponse
from src.models.rag_evaluation import (
    RAGEvaluationCase,
    RAGEvaluationResult,
)
from src.services.rag_evaluation_service import RAGEvaluationService


class FakeRAGService:
    def __init__(self, responses: list[RAGResponse]) -> None:
        self._responses = responses
        self.queries: list[str] = []

    def answer(self, query) -> RAGResponse:
        self.queries.append(query.query)

        return self._responses[len(self.queries) - 1]


class FakeAnswerEvaluator(AnswerEvaluator):
    def __init__(self, score: float) -> None:
        self._score = score

    def evaluate(self, case, response) -> float:
        return self._score


class FakeCitationEvaluator:
    def __init__(self, scores: list[tuple[float, float]]) -> None:
        self._scores = scores
        self.calls = 0

    def evaluate(self, case, response) -> tuple[float, float]:
        scores = self._scores[self.calls]
        self.calls += 1

        return scores


class FakeGroundingEvaluator:
    def __init__(self, score: float) -> None:
        self._score = score

    def evaluate(self, response) -> float:
        return self._score


def _response(answer: str) -> RAGResponse:
    return RAGResponse(
        query="ignored",
        answer=answer,
        citations=[
            Citation(
                citation_id="SOURCE-1",
                document_id="doc-1",
                chunk_id="chunk-1",
                chunk_index=0,
            )
        ],
        model_name="test-model",
        retrieved_count=1,
    )


def _case(
    case_id: str = "case-001",
    query: str = "What is the billing dispute policy?",
) -> RAGEvaluationCase:
    return RAGEvaluationCase(
        case_id=case_id,
        query=query,
        reference_answer="Customers can dispute billing charges.",
        expected_citations=["SOURCE-1"],
    )


def _service(
    rag_service,
    answer_score: float = 0.5,
    citation_scores: list[tuple[float, float]] | None = None,
    grounding_score: float = 1.0,
) -> RAGEvaluationService:
    return RAGEvaluationService(
        rag_service=rag_service,
        answer_evaluator=FakeAnswerEvaluator(answer_score),
        citation_evaluator=FakeCitationEvaluator(citation_scores or [(1.0, 1.0)]),
        grounding_evaluator=FakeGroundingEvaluator(grounding_score),
    )


class TestEvaluateCase:
    def test_returns_result_for_case(self) -> None:
        service = _service(FakeRAGService([_response("answer")]))

        result = service.evaluate_case(_case())

        assert isinstance(result, RAGEvaluationResult)
        assert result.case_id == "case-001"

    def test_forwards_case_query_to_rag_service(self) -> None:
        rag_service = FakeRAGService([_response("answer")])

        _service(rag_service).evaluate_case(_case(query="How long is the refund window?"))

        assert rag_service.queries == ["How long is the refund window?"]

    def test_delegates_to_each_evaluator(self) -> None:
        service = _service(
            FakeRAGService([_response("answer")]),
            answer_score=0.25,
            citation_scores=[(0.5, 0.75)],
            grounding_score=0.0,
        )

        result = service.evaluate_case(_case())

        assert result.answer_relevance == 0.25
        assert result.citation_precision == 0.5
        assert result.citation_recall == 0.75
        assert result.grounding == 0.0


class TestEvaluate:
    def test_averages_across_cases(self) -> None:
        rag_service = FakeRAGService([_response("a"), _response("b")])

        service = _service(
            rag_service,
            citation_scores=[(1.0, 1.0), (0.0, 0.0)],
        )

        metrics = service.evaluate([_case("case-001"), _case("case-002")])

        assert metrics.answer_relevance == 0.5
        assert metrics.citation_precision == 0.5
        assert metrics.citation_recall == 0.5
        assert metrics.grounding == 1.0

    def test_empty_case_list_raises(self) -> None:
        service = _service(FakeRAGService([]))

        with pytest.raises(
            ValueError,
            match="At least one evaluation case is required.",
        ):
            service.evaluate([])

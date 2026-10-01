from src.evaluation.answer.base import AnswerEvaluator
from src.evaluation.answer.semantic import SimpleAnswerEvaluator
from src.models.rag import RAGResponse
from src.models.rag_evaluation import RAGEvaluationCase


def _case(reference_answer: str) -> RAGEvaluationCase:
    return RAGEvaluationCase(
        case_id="billing-policy-answer-001",
        query="What is the billing dispute policy?",
        reference_answer=reference_answer,
        expected_citations=["SOURCE-1"],
    )


def _response(answer: str) -> RAGResponse:
    return RAGResponse(
        query="What is the billing dispute policy?",
        answer=answer,
        citations=[],
        model_name="test-model",
        retrieved_count=1,
    )


class TestSimpleAnswerEvaluator:
    def test_implements_answer_evaluator_boundary(self) -> None:
        assert issubclass(
            SimpleAnswerEvaluator,
            AnswerEvaluator,
        )

    def test_answer_sharing_terms_scores_above_zero(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("Customers can dispute billing charges."),
            _response("Customers can dispute billing charges."),
        )

        assert score > 0

    def test_identical_answer_scores_one(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("Customers can dispute billing charges."),
            _response("Customers can dispute billing charges."),
        )

        assert score == 1.0

    def test_unrelated_answer_scores_low(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("Customers can dispute billing charges."),
            _response(
                "The deployment pipeline runs on Kubernetes.",
            ),
        )

        assert score < 0.2

    def test_score_is_recall_of_reference_tokens(self) -> None:
        """Half the reference tokens present -> 0.5, not 1.0."""
        score = SimpleAnswerEvaluator().evaluate(
            _case("alpha beta gamma delta"),
            _response("alpha beta"),
        )

        assert score == 0.5

    def test_matching_is_case_insensitive(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("Customers can dispute billing charges."),
            _response("CUSTOMERS CAN DISPUTE BILLING CHARGES"),
        )

        assert score == 1.0

    def test_empty_answer_scores_zero(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("Customers can dispute billing charges."),
            _response(""),
        )

        assert score == 0.0

    def test_empty_reference_answer_scores_zero(self) -> None:
        score = SimpleAnswerEvaluator().evaluate(
            _case("   "),
            _response("Customers can dispute billing charges."),
        )

        assert score == 0.0


class TestAnswerEvaluatorIsAbstract:
    def test_cannot_be_instantiated(self) -> None:
        try:
            AnswerEvaluator()
        except TypeError:
            return

        raise AssertionError(
            "AnswerEvaluator should be abstract"
        )
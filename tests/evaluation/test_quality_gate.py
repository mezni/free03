from src.evaluation.quality_gate import (
    QualityGate,
    QualityGateConfig,
)
from src.models.rag_evaluation import RAGEvaluationMetrics


def make_gate() -> QualityGate:
    return QualityGate(
        QualityGateConfig(
            min_answer_relevance=0.6,
            min_citation_precision=0.8,
            min_citation_recall=0.8,
            min_grounding=0.8,
        )
    )


def test_quality_gate_passes() -> None:
    metrics = RAGEvaluationMetrics(
        answer_relevance=0.9,
        citation_precision=0.9,
        citation_recall=0.9,
        grounding=0.9,
    )

    result = make_gate().evaluate(metrics)

    assert result.passed is True
    assert result.failures == []


def test_quality_gate_fails() -> None:
    metrics = RAGEvaluationMetrics(
        answer_relevance=0.9,
        citation_precision=0.5,
        citation_recall=0.9,
        grounding=0.9,
    )

    result = make_gate().evaluate(metrics)

    assert result.passed is False
    assert "citation_precision" in result.failures


def test_quality_gate_reports_every_failure() -> None:
    metrics = RAGEvaluationMetrics(
        answer_relevance=0.10,
        citation_precision=0.10,
        citation_recall=0.10,
        grounding=0.10,
    )

    result = make_gate().evaluate(metrics)

    assert result.passed is False
    assert result.failures == [
        "answer_relevance",
        "citation_precision",
        "citation_recall",
        "grounding",
    ]


def test_quality_gate_treats_threshold_as_inclusive() -> None:
    metrics = RAGEvaluationMetrics(
        answer_relevance=0.6,
        citation_precision=0.8,
        citation_recall=0.8,
        grounding=0.8,
    )

    result = make_gate().evaluate(metrics)

    assert result.passed is True


def test_quality_gate_fails_grounding_only() -> None:
    metrics = RAGEvaluationMetrics(
        answer_relevance=0.95,
        citation_precision=0.95,
        citation_recall=0.95,
        grounding=0.20,
    )

    result = make_gate().evaluate(metrics)

    assert result.passed is False
    assert result.failures == ["grounding"]
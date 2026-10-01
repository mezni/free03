from pydantic import BaseModel, ConfigDict, Field

from src.models.rag_evaluation import RAGEvaluationMetrics


class QualityGateConfig(BaseModel):
    """Minimum acceptable RAG evaluation scores.

    These are engineering thresholds used to block regressions in CI.
    They are not universal claims about acceptable RAG quality.
    """

    model_config = ConfigDict(extra="forbid")

    min_answer_relevance: float = Field(ge=0.0, le=1.0)
    min_citation_precision: float = Field(ge=0.0, le=1.0)
    min_citation_recall: float = Field(ge=0.0, le=1.0)
    min_grounding: float = Field(ge=0.0, le=1.0)


class QualityGateResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    passed: bool
    failures: list[str] = Field(default_factory=list)


class QualityGate:
    def __init__(self, config: QualityGateConfig) -> None:
        self._config = config

    def evaluate(
        self,
        metrics: RAGEvaluationMetrics,
    ) -> QualityGateResult:
        failures: list[str] = []

        if metrics.answer_relevance < self._config.min_answer_relevance:
            failures.append("answer_relevance")

        if metrics.citation_precision < self._config.min_citation_precision:
            failures.append("citation_precision")

        if metrics.citation_recall < self._config.min_citation_recall:
            failures.append("citation_recall")

        if metrics.grounding < self._config.min_grounding:
            failures.append("grounding")

        return QualityGateResult(
            passed=not failures,
            failures=failures,
        )
from pydantic import BaseModel, ConfigDict, Field


class RAGEvaluationCase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    case_id: str = Field(
        min_length=1,
        max_length=100,
    )

    knowledge_base: str = Field(
        min_length=1,
        max_length=100,
    )

    query: str = Field(
        min_length=1,
    )

    reference_answer: str = Field(
        min_length=1,
    )

    expected_citations: list[str] = Field(
        default_factory=list,
    )


class RAGEvaluationResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    case_id: str

    answer_relevance: float = Field(
        ge=0.0,
        le=1.0,
    )

    citation_precision: float = Field(
        ge=0.0,
        le=1.0,
    )

    citation_recall: float = Field(
        ge=0.0,
        le=1.0,
    )

    grounding: float = Field(
        ge=0.0,
        le=1.0,
    )


class RAGEvaluationMetrics(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    answer_relevance: float = Field(
        ge=0.0,
        le=1.0,
    )

    citation_precision: float = Field(
        ge=0.0,
        le=1.0,
    )

    citation_recall: float = Field(
        ge=0.0,
        le=1.0,
    )

    grounding: float = Field(
        ge=0.0,
        le=1.0,
    )

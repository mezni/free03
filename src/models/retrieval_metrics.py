from pydantic import BaseModel, ConfigDict, Field


class RetrievalMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    recall_at_k: float = Field(ge=0.0, le=1.0)
    precision_at_k: float = Field(ge=0.0, le=1.0)
    mrr: float = Field(ge=0.0, le=1.0)
    ndcg_at_k: float = Field(ge=0.0, le=1.0)

    # Measured over the final context the LLM received, not the
    # ranked list. Optional because they require knowing what the
    # context-selection stage produced.
    context_recall: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    context_precision: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
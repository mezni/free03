from pydantic import BaseModel, ConfigDict, Field

from src.models.retrieval import RetrievalFilter


class QueryAnalysis(BaseModel):
    """Structured output of query analysis.

    Transformation produces an object rather than a bare string, so
    intent, entities, document_type, or date_range can be added later
    without changing the retrieval contract.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    original_query: str = Field(min_length=1)

    rewritten_query: str = Field(min_length=1)

    filters: RetrievalFilter | None = None
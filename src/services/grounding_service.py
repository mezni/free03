from pydantic import BaseModel, ConfigDict


class GroundingResult(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    grounded: bool
    citation_count: int


class GroundingService:
    """Check whether an answer is backed by at least one citation."""

    def validate(
        self,
        answer: str,
        citation_count: int,
    ) -> GroundingResult:
        if not answer.strip():
            return GroundingResult(
                grounded=False,
                citation_count=0,
            )

        return GroundingResult(
            grounded=citation_count > 0,
            citation_count=citation_count,
        )

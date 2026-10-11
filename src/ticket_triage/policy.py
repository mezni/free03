from ticket_triage.domain import Priority, Recommendation


class RecommendationValidationError(ValueError):
    """Raised when a recommendation violates application policy."""


class RecommendationPolicy:
    def __init__(
        self,
        *,
        allowed_categories: set[str],
        allowed_destinations: set[str],
    ) -> None:
        self.allowed_categories = allowed_categories
        self.allowed_destinations = allowed_destinations

    def validate(self, recommendation: Recommendation) -> None:
        if not recommendation.category.strip():
            raise RecommendationValidationError("Category cannot be empty.")
        if recommendation.category not in self.allowed_categories:
            raise RecommendationValidationError(
                f"Unsupported category: {recommendation.category}"
            )
        if recommendation.destination not in self.allowed_destinations:
            raise RecommendationValidationError(
                f"Unsupported destination: {recommendation.destination}"
            )
        if not isinstance(recommendation.priority, Priority):
            raise RecommendationValidationError(
                f"Unsupported priority: {recommendation.priority}"
            )

import pytest

from ticket_triage.domain import Priority, Recommendation
from ticket_triage.policy import (
    RecommendationPolicy,
    RecommendationValidationError,
)


@pytest.fixture
def policy():
    return RecommendationPolicy(
        allowed_categories={"billing", "account", "general"},
        allowed_destinations={
            "billing-team",
            "account-support",
            "general-support",
        },
    )


def test_accepts_valid_recommendation(policy):
    recommendation = Recommendation(
        category="billing",
        priority=Priority.HIGH,
        destination="billing-team",
        rationale="The ticket concerns a payment.",
    )
    policy.validate(recommendation)

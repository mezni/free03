from typing import Protocol

from ticket_triage.domain import Priority, Recommendation, Ticket


class ClassificationError(RuntimeError):
    """Raised when classification cannot produce a usable result."""


class Classifier(Protocol):
    def classify(self, ticket: Ticket) -> Recommendation:
        """Return a recommendation for the supplied ticket."""
        ...


class FakeClassifier:
    """Deterministic classifier for development and testing."""

    def classify(self, ticket: Ticket) -> Recommendation:
        text = f"{ticket.subject} {ticket.description}".lower()

        if any(word in text for word in ("refund", "charged", "payment")):
            return Recommendation(
                category="billing",
                priority=Priority.HIGH,
                destination="billing-team",
                rationale="The ticket mentions a billing issue.",
            )

        if any(word in text for word in ("login", "password", "account")):
            return Recommendation(
                category="account",
                priority=Priority.MEDIUM,
                destination="account-support",
                rationale="The ticket mentions account access.",
            )

        return Recommendation(
            category="general",
            priority=Priority.LOW,
            destination="general-support",
            rationale="The ticket does not match a specific category.",
        )

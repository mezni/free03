from time import sleep

from ticket_triage.classification import Classifier
from ticket_triage.domain import Recommendation, Ticket
from ticket_triage.errors import TransientProviderError


class RetryingClassifier:
    """Retry only explicitly identified transient provider failures."""

    def __init__(
        self,
        classifier: Classifier,
        *,
        max_attempts: int = 2,
        retry_delay_seconds: float = 0.2,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        if retry_delay_seconds < 0:
            raise ValueError("retry delay cannot be negative.")
        self.classifier = classifier
        self.max_attempts = max_attempts
        self.retry_delay_seconds = retry_delay_seconds

    def classify(self, ticket: Ticket) -> Recommendation:
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self.classifier.classify(ticket)
            except TransientProviderError:
                if attempt == self.max_attempts:
                    raise
                sleep(self.retry_delay_seconds)
import logging
from dataclasses import dataclass
from time import perf_counter

from ticket_triage.classification import Classifier
from ticket_triage.domain import Recommendation, Ticket

logger = logging.getLogger(__name__)


@dataclass
class ClassificationMetrics:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_latency_ms: float = 0.0

    @property
    def average_latency_ms(self) -> float:
        if self.total_calls == 0:
            return 0.0
        return self.total_latency_ms / self.total_calls


class InstrumentedClassifier:
    """Decorator that records metrics around an existing classifier."""

    def __init__(self, classifier: Classifier) -> None:
        self.classifier = classifier
        self.metrics = ClassificationMetrics()

    def classify(
        self,
        ticket: Ticket,
        *,
        timeout_seconds: float | None = None,
    ) -> Recommendation:
        started = perf_counter()
        try:
            result = self.classifier.classify(ticket, timeout_seconds=timeout_seconds)
        except Exception as exc:
            elapsed_ms = (perf_counter() - started) * 1000.0
            self.metrics.total_calls += 1
            self.metrics.failed_calls += 1
            self.metrics.total_latency_ms += elapsed_ms
            logger.warning(
                "classification failed",
                extra={
                    "event": "classification_failure",
                    "duration_ms": round(elapsed_ms, 3),
                    "error_type": type(exc).__name__,
                },
            )
            raise
        else:
            elapsed_ms = (perf_counter() - started) * 1000.0
            self.metrics.total_calls += 1
            self.metrics.successful_calls += 1
            self.metrics.total_latency_ms += elapsed_ms
            logger.info(
                "classification succeeded",
                extra={
                    "event": "classification_success",
                    "duration_ms": round(elapsed_ms, 3),
                    "category": result.category,
                    "priority": result.priority.value,
                    "destination": result.destination,
                },
            )
            return result

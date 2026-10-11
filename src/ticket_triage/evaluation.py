from dataclasses import dataclass

from ticket_triage.classification import Classifier
from ticket_triage.domain import Recommendation, Ticket


@dataclass(frozen=True)
class EvaluationExample:
    ticket: Ticket
    expected: Recommendation


@dataclass
class EvaluationReport:
    total: int = 0
    failed: int = 0
    category_correct: int = 0
    priority_correct: int = 0
    destination_correct: int = 0

    @property
    def category_accuracy(self) -> float:
        return self.category_correct / self.total if self.total else 0.0

    @property
    def priority_accuracy(self) -> float:
        return self.priority_correct / self.total if self.total else 0.0

    @property
    def destination_accuracy(self) -> float:
        return self.destination_correct / self.total if self.total else 0.0

    @property
    def failure_rate(self) -> float:
        return self.failed / self.total if self.total else 0.0


def evaluate_classifier(
    classifier: Classifier,
    examples: list[EvaluationExample],
) -> EvaluationReport:
    report = EvaluationReport()
    for example in examples:
        report.total += 1
        try:
            predicted = classifier.classify(example.ticket)
        except Exception:
            report.failed += 1
            continue
        if predicted.category == example.expected.category:
            report.category_correct += 1
        if predicted.priority == example.expected.priority:
            report.priority_correct += 1
        if predicted.destination == example.expected.destination:
            report.destination_correct += 1
    return report
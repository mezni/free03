import pytest

from tests.fakes import FakeLLMClient
from ticket_triage.classification import ClassificationError
from ticket_triage.domain import Priority, Ticket
from ticket_triage.llm_classifier import LLMClassifier


@pytest.fixture
def ticket():
    return Ticket(
        ticket_id="T-200",
        subject="Charged twice",
        description="I was charged twice for one order.",
    )


VALID_RESPONSE = (
    '{"category":"billing",'
    '"priority":"high",'
    '"destination":"billing-team",'
    '"rationale":"The customer reports duplicate charges."}'
)


def test_parses_valid_response(ticket):
    client = FakeLLMClient(VALID_RESPONSE)
    result = LLMClassifier(client).classify(ticket)
    assert result.category == "billing"
    assert result.priority == Priority.HIGH
    assert result.destination == "billing-team"
    assert result.rationale == "The customer reports duplicate charges."
    assert ticket.ticket_id in client.last_prompt


def test_parses_markdown_fenced_response(ticket):
    client = FakeLLMClient(f"```json\n{VALID_RESPONSE}\n```")
    result = LLMClassifier(client).classify(ticket)
    assert result.category == "billing"
    assert result.priority == Priority.HIGH


def test_rejects_invalid_json(ticket):
    client = FakeLLMClient("not json")
    with pytest.raises(ClassificationError):
        LLMClassifier(client).classify(ticket)


@pytest.mark.parametrize(
    "response",
    [
        pytest.param(
            '{"priority":"high","destination":"billing-team",'
            '"rationale":"The customer reports duplicate charges."}',
            id="missing-field",
        ),
        pytest.param(
            '{"category":"billing","priority":"high",'
            '"destination":"billing-team","rationale":"x","extra":"extra"}',
            id="unexpected-field",
        ),
        pytest.param(
            '{"category":["billing"],"priority":"high",'
            '"destination":"billing-team","rationale":"x"}',
            id="incorrect-type",
        ),
        pytest.param(
            '{"category":"","priority":"high",'
            '"destination":"billing-team","rationale":"x"}',
            id="empty-field",
        ),
    ],
)
def test_rejects_schema_violations(ticket, response):
    with pytest.raises(ClassificationError):
        LLMClassifier(FakeLLMClient(response)).classify(ticket)


def test_rejects_unsupported_priority(ticket):
    response = (
        '{"category":"billing","priority":"critical",'
        '"destination":"billing-team","rationale":"x"}'
    )
    with pytest.raises(ClassificationError):
        LLMClassifier(FakeLLMClient(response)).classify(ticket)


def test_wraps_client_failure(ticket):
    class BrokenClient:
        def generate(self, prompt: str) -> str:
            raise RuntimeError("network down")

    with pytest.raises(ClassificationError):
        LLMClassifier(BrokenClient()).classify(ticket)

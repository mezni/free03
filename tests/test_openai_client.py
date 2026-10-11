from types import SimpleNamespace

import pytest

from ticket_triage.errors import (
    InvalidModelOutputError,
    TransientProviderError,
)
from ticket_triage.openai_client import OpenAILLMClient


class FakeResponses:
    def __init__(self):
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            output_text=(
                '{"category":"billing",'
                '"priority":"high",'
                '"destination":"billing-team",'
                '"rationale":"The ticket reports duplicate charges."}'
            )
        )


class FakeOpenAI:
    def __init__(self):
        self.responses = FakeResponses()


def test_openai_adapter_requests_structured_output():
    fake_sdk = FakeOpenAI()
    adapter = OpenAILLMClient(
        model="test-model",
        client=fake_sdk,
    )

    result = adapter.generate("Classify this synthetic ticket.")

    assert result == (
        '{"category":"billing",'
        '"priority":"high",'
        '"destination":"billing-team",'
        '"rationale":"The ticket reports duplicate charges."}'
    )

    request = fake_sdk.responses.kwargs
    assert request["model"] == "test-model"
    assert request["input"] == "Classify this synthetic ticket."
    text_format = request["text"]["format"]
    assert text_format["type"] == "json_schema"
    assert text_format["strict"] is True
    assert text_format["schema"]["required"] == [
        "category",
        "priority",
        "destination",
        "rationale",
    ]


def test_openai_adapter_maps_transient_errors():
    from openai import APITimeoutError

    class TimeoutResponses:
        def create(self, **kwargs):
            raise APITimeoutError("timed out")

    class TimeoutOpenAI:
        def __init__(self):
            self.responses = TimeoutResponses()

    adapter = OpenAILLMClient(
        model="test-model",
        client=TimeoutOpenAI(),
    )

    with pytest.raises(TransientProviderError):
        adapter.generate("Classify this synthetic ticket.")


def test_openai_adapter_rejects_empty_output():
    class EmptyResponses:
        def create(self, **kwargs):
            return SimpleNamespace(output_text="")

    class EmptyOpenAI:
        def __init__(self):
            self.responses = EmptyResponses()

    adapter = OpenAILLMClient(
        model="test-model",
        client=EmptyOpenAI(),
    )

    with pytest.raises(InvalidModelOutputError):
        adapter.generate("Classify this synthetic ticket.")

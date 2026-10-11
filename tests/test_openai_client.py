from types import SimpleNamespace

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
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.models.generation import GenerationRequest
from src.providers.llm.openrouter import OpenRouterProvider


def make_provider(**overrides) -> OpenRouterProvider:
    kwargs = {
        "api_key": "test-key",
        "model_name": "openai/gpt-oss-20b:free",
        "temperature": 0.0,
        "max_tokens": 1000,
        "timeout_seconds": 60,
    }
    kwargs.update(overrides)

    return OpenRouterProvider(**kwargs)


def make_request(
    query: str = "What is the billing policy?",
    context: str = "Billing disputes must be filed within 30 days.",
) -> GenerationRequest:
    return GenerationRequest(query=query, context=context)


def api_payload(
    answer: str = "Disputes must be filed within 30 days.",
    model: str = "openai/gpt-oss-20b:free",
    usage: dict | None = None,
) -> dict:
    payload = {
        "choices": [
            {"message": {"content": answer}},
        ],
        "model": model,
    }

    if usage is not None:
        payload["usage"] = usage

    return payload


def post_args(mock_client_cls):
    client = (
        mock_client_cls.return_value.__enter__.return_value
    )

    return client.post.call_args


def test_provider_exposes_model_name():
    provider = make_provider()

    assert provider.model_name == "openai/gpt-oss-20b:free"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_extracts_answer(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    result = provider.generate(make_request())

    assert (
        result.answer
        == "Disputes must be filed within 30 days."
    )


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_extracts_usage(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload(
        usage={
            "prompt_tokens": 120,
            "completion_tokens": 30,
            "total_tokens": 150,
        }
    )

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    result = provider.generate(make_request())

    assert result.prompt_tokens == 120
    assert result.completion_tokens == 30
    assert result.total_tokens == 150


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_tolerates_missing_usage(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    result = provider.generate(make_request())

    assert result.prompt_tokens is None
    assert result.completion_tokens is None
    assert result.total_tokens is None


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_prefers_model_from_response(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload(
        model="provider-reported-model"
    )

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    result = provider.generate(make_request())

    assert result.model_name == "provider-reported-model"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_falls_back_to_configured_model(mock_client_cls):
    payload = api_payload()
    payload.pop("model")

    response = MagicMock()
    response.json.return_value = payload

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    result = provider.generate(make_request())

    assert result.model_name == "openai/gpt-oss-20b:free"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_passes_model_and_generation_settings(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider(
        temperature=0.7,
        max_tokens=512,
    )

    provider.generate(make_request())

    payload = post_args(mock_client_cls).kwargs["json"]

    assert payload["model"] == "openai/gpt-oss-20b:free"
    assert payload["temperature"] == 0.7
    assert payload["max_tokens"] == 512


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_passes_api_key_and_endpoint(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    provider.generate(make_request())

    args, kwargs = post_args(mock_client_cls)

    assert args[0] == OpenRouterProvider.BASE_URL
    assert kwargs["headers"]["Authorization"] == "Bearer test-key"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_sends_query_and_context_in_messages(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    provider.generate(make_request())

    messages = post_args(mock_client_cls).kwargs["json"]["messages"]

    assert messages[0]["role"] == "system"

    assert messages[1]["role"] == "user"
    assert "30 days" in messages[1]["content"]
    assert "What is the billing policy?" in messages[1]["content"]


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_applies_configured_timeout(mock_client_cls):
    response = MagicMock()
    response.json.return_value = api_payload()

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider(timeout_seconds=17)

    provider.generate(make_request())

    assert mock_client_cls.call_args.kwargs["timeout"] == 17


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_propagates_http_errors(mock_client_cls):
    response = MagicMock()
    response.raise_for_status.side_effect = (
        httpx.HTTPStatusError(
            "rate limited",
            request=MagicMock(),
            response=MagicMock(),
        )
    )

    client = mock_client_cls.return_value.__enter__.return_value
    client.post.return_value = response

    provider = make_provider()

    with pytest.raises(httpx.HTTPStatusError):
        provider.generate(make_request())


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_propagates_transport_errors(mock_client_cls):
    client = mock_client_cls.return_value.__enter__.return_value
    client.post.side_effect = httpx.ConnectError("unreachable")

    provider = make_provider()

    with pytest.raises(httpx.ConnectError):
        provider.generate(make_request())
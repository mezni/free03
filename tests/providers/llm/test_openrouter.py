from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.core.exceptions import (
    ProviderResponseError,
    ProviderTimeoutError,
    TransientProviderError,
)
from src.models.generation import GenerationRequest
from src.providers.llm.openrouter import OpenRouterProvider
from src.providers.retry import RetryPolicy


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
) -> GenerationRequest:
    return GenerationRequest(
        query=query,
        system_prompt="system instructions",
        user_prompt="user instructions",
    )


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


def make_response(
    payload: dict | None = None,
    status_code: int = 200,
    json_error: Exception | None = None,
    body: str = "",
) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.text = body

    if json_error is not None:
        response.json.side_effect = json_error
    else:
        response.json.return_value = (
            api_payload() if payload is None else payload
        )

    return response


def wire(
    mock_client_cls,
    response,
    side_effect: Exception | None = None,
):
    client = mock_client_cls.return_value.__enter__.return_value

    if side_effect is not None:
        client.post.side_effect = side_effect
    else:
        client.post.return_value = response

    return client


def post_args(mock_client_cls):
    client = (
        mock_client_cls.return_value.__enter__.return_value
    )

    return client.post.call_args


def no_retries() -> RetryPolicy:
    return RetryPolicy(max_retries=0, delay_seconds=0.0)


def test_provider_exposes_model_name():
    provider = make_provider()

    assert provider.model_name == "openai/gpt-oss-20b:free"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_extracts_answer(mock_client_cls):
    wire(mock_client_cls, make_response())

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert (
        result.answer
        == "Disputes must be filed within 30 days."
    )


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_extracts_usage(mock_client_cls):
    wire(
        mock_client_cls,
        make_response(
            payload=api_payload(
                usage={
                    "prompt_tokens": 120,
                    "completion_tokens": 30,
                    "total_tokens": 150,
                }
            )
        ),
    )

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.prompt_tokens == 120
    assert result.completion_tokens == 30
    assert result.total_tokens == 150


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_tolerates_missing_usage(mock_client_cls):
    wire(mock_client_cls, make_response())

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.prompt_tokens is None
    assert result.completion_tokens is None
    assert result.total_tokens is None


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_tolerates_null_usage(mock_client_cls):
    payload = api_payload()
    payload["usage"] = None

    wire(mock_client_cls, make_response(payload=payload))

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.total_tokens is None


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_prefers_model_from_response(mock_client_cls):
    wire(
        mock_client_cls,
        make_response(
            payload=api_payload(
                model="provider-reported-model"
            )
        ),
    )

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.model_name == "provider-reported-model"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_falls_back_to_configured_model(mock_client_cls):
    payload = api_payload()
    payload.pop("model")

    wire(mock_client_cls, make_response(payload=payload))

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.model_name == "openai/gpt-oss-20b:free"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_ignores_non_string_model(mock_client_cls):
    payload = api_payload()
    payload["model"] = {"unexpected": "object"}

    wire(mock_client_cls, make_response(payload=payload))

    result = make_provider(retry_policy=no_retries()).generate(
        make_request()
    )

    assert result.model_name == "openai/gpt-oss-20b:free"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_passes_model_and_generation_settings(mock_client_cls):
    wire(mock_client_cls, make_response())

    make_provider(
        temperature=0.7,
        max_tokens=512,
        retry_policy=no_retries(),
    ).generate(make_request())

    payload = post_args(mock_client_cls).kwargs["json"]

    assert payload["model"] == "openai/gpt-oss-20b:free"
    assert payload["temperature"] == 0.7
    assert payload["max_tokens"] == 512


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_passes_api_key_and_endpoint(mock_client_cls):
    wire(mock_client_cls, make_response())

    make_provider(retry_policy=no_retries()).generate(make_request())

    args, kwargs = post_args(mock_client_cls)

    assert args[0] == OpenRouterProvider.BASE_URL
    assert kwargs["headers"]["Authorization"] == "Bearer test-key"


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_sends_prebuilt_prompts_in_messages(mock_client_cls):
    wire(mock_client_cls, make_response())

    make_provider(retry_policy=no_retries()).generate(make_request())

    messages = post_args(mock_client_cls).kwargs["json"]["messages"]

    assert messages == [
        {
            "role": "system",
            "content": "system instructions",
        },
        {
            "role": "user",
            "content": "user instructions",
        },
    ]


@patch("src.providers.llm.openrouter.httpx.Client")
def test_generate_applies_configured_timeout(mock_client_cls):
    wire(mock_client_cls, make_response())

    make_provider(
        timeout_seconds=17,
        retry_policy=no_retries(),
    ).generate(make_request())

    assert mock_client_cls.call_args.kwargs["timeout"] == 17


class TestFailureClassification:
    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_timeout_becomes_provider_timeout(
        self,
        mock_client_cls,
    ) -> None:
        wire(
            mock_client_cls,
            None,
            side_effect=httpx.ReadTimeout("slow"),
        )

        with pytest.raises(ProviderTimeoutError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_connect_error_becomes_transient(
        self,
        mock_client_cls,
    ) -> None:
        wire(
            mock_client_cls,
            None,
            side_effect=httpx.ConnectError("unreachable"),
        )

        with pytest.raises(TransientProviderError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_server_error_becomes_transient(
        self,
        mock_client_cls,
    ) -> None:
        wire(mock_client_cls, make_response(status_code=503))

        with pytest.raises(TransientProviderError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_client_error_is_not_transient(
        self,
        mock_client_cls,
    ) -> None:
        wire(mock_client_cls, make_response(status_code=401))

        with pytest.raises(ProviderResponseError) as info:
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

        assert not isinstance(
            info.value, TransientProviderError
        )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_error_body_is_never_exposed(
        self,
        mock_client_cls,
    ) -> None:
        response = make_response(
            status_code=401,
            body='{"error":"invalid key sk-or-v1-SECRET"}',
        )
        wire(mock_client_cls, response)

        with pytest.raises(ProviderResponseError) as info:
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

        assert "SECRET" not in str(info.value)
        assert "sk-or-v1" not in str(info.value)

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_no_httpx_errors_escape(self, mock_client_cls) -> None:
        wire(
            mock_client_cls,
            None,
            side_effect=httpx.ReadTimeout("slow"),
        )

        with pytest.raises(Exception) as info:
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

        assert not isinstance(info.value, httpx.HTTPError)


class TestResponseValidation:
    @pytest.mark.parametrize(
        "payload",
        [
            pytest.param({}, id="empty"),
            pytest.param({"choices": []}, id="no-choices"),
            pytest.param({"choices": "nope"}, id="choices-not-list"),
            pytest.param(
                {"choices": [{"nope": 1}]},
                id="no-message",
            ),
            pytest.param(
                {"choices": [{"message": "text"}]},
                id="message-not-dict",
            ),
            pytest.param(
                {"choices": [{"message": {"content": None}}]},
                id="content-null",
            ),
            pytest.param(
                {"choices": [{"message": {"content": 42}}]},
                id="content-not-string",
            ),
            pytest.param(
                {"choices": {"a": 1}},
                id="choices-not-list-2",
            ),
        ],
    )
    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_malformed_payload_raises(
        self,
        mock_client_cls,
        payload: dict,
    ) -> None:
        wire(mock_client_cls, make_response(payload=payload))

        with pytest.raises(ProviderResponseError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_invalid_json_raises(self, mock_client_cls) -> None:
        wire(
            mock_client_cls,
            make_response(json_error=ValueError("not json")),
        )

        with pytest.raises(ProviderResponseError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_non_dict_json_raises(self, mock_client_cls) -> None:
        wire(
            mock_client_cls,
            make_response(payload=["a", "list"]),
        )

        with pytest.raises(ProviderResponseError):
            make_provider(retry_policy=no_retries()).generate(
                make_request()
            )

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_empty_content_is_accepted(
        self,
        mock_client_cls,
    ) -> None:
        wire(
            mock_client_cls,
            make_response(
                payload=api_payload(answer="")
            ),
        )

        result = make_provider(retry_policy=no_retries()).generate(
            make_request()
        )

        assert result.answer == ""


class TestRetryIntegration:
    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_retries_server_error_then_succeeds(
        self,
        mock_client_cls,
    ) -> None:
        client = wire(
            mock_client_cls,
            make_response(status_code=503),
        )
        client.post.side_effect = [
            make_response(status_code=503),
            make_response(),
        ]

        provider = make_provider(
            retry_policy=RetryPolicy(
                max_retries=2,
                delay_seconds=0.0,
            )
        )

        result = provider.generate(make_request())

        assert result.answer == (
            "Disputes must be filed within 30 days."
        )
        assert client.post.call_count == 2

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_does_not_retry_client_error(
        self,
        mock_client_cls,
    ) -> None:
        client = wire(
            mock_client_cls,
            make_response(status_code=400),
        )

        provider = make_provider(
            retry_policy=RetryPolicy(
                max_retries=3,
                delay_seconds=0.0,
            )
        )

        with pytest.raises(ProviderResponseError):
            provider.generate(make_request())

        assert client.post.call_count == 1

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_does_not_retry_malformed_payload(
        self,
        mock_client_cls,
    ) -> None:
        client = wire(
            mock_client_cls,
            make_response(payload={"choices": []}),
        )

        provider = make_provider(
            retry_policy=RetryPolicy(
                max_retries=3,
                delay_seconds=0.0,
            )
        )

        with pytest.raises(ProviderResponseError):
            provider.generate(make_request())

        assert client.post.call_count == 1

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_exhausted_retries_raise_transient(
        self,
        mock_client_cls,
    ) -> None:
        client = wire(
            mock_client_cls,
            make_response(status_code=500),
        )

        provider = make_provider(
            retry_policy=RetryPolicy(
                max_retries=2,
                delay_seconds=0.0,
            )
        )

        with pytest.raises(TransientProviderError):
            provider.generate(make_request())

        assert client.post.call_count == 3

    @patch("src.providers.llm.openrouter.httpx.Client")
    def test_default_policy_does_not_retry(
        self,
        mock_client_cls,
    ) -> None:
        client = wire(
            mock_client_cls,
            make_response(status_code=500),
        )

        with pytest.raises(TransientProviderError):
            make_provider().generate(make_request())

        assert client.post.call_count == 1
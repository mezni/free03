import httpx

from src.core.exceptions import (
    ProviderResponseError,
    ProviderTimeoutError,
    TransientProviderError,
)
from src.models.generation import (
    GenerationRequest,
    GenerationResponse,
)
from src.providers.circuit_breaker import CircuitBreaker, CircuitState
from src.providers.llm.base import LLMProvider
from src.providers.retry import RetryPolicy
from src.providers.retryable import is_retryable_status


class OpenRouterProvider(LLMProvider):
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        timeout_seconds: int,
        retry_policy: RetryPolicy | None = None,
        circuit_breaker: CircuitBreaker | None = None,
    ) -> None:
        self._api_key = api_key
        self._model_name = model_name
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout_seconds = timeout_seconds
        self._retry_policy = retry_policy or RetryPolicy(
            max_retries=0,
            delay_seconds=0.0,
        )
        self._circuit_breaker = circuit_breaker

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def circuit_state(self) -> CircuitState:
        if self._circuit_breaker is None:
            return CircuitState.CLOSED

        return self._circuit_breaker.state

    def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:
        payload = {
            "model": self._model_name,
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
            "messages": [
                {
                    "role": "system",
                    "content": request.system_prompt,
                },
                {
                    "role": "user",
                    "content": request.user_prompt,
                },
            ],
        }

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        if self._circuit_breaker is not None:
            # Rejected before the request is built, so an open circuit
            # costs no network call and no provider load.
            self._circuit_breaker.before_call()

        try:
            response = self._retry_policy.execute(
                lambda: self._complete(payload, headers)
            )
        except (ProviderTimeoutError, TransientProviderError):
            if self._circuit_breaker is not None:
                self._circuit_breaker.record_failure()

            raise

        if self._circuit_breaker is not None:
            self._circuit_breaker.record_success()

        return response

    def _complete(
        self,
        payload: dict,
        headers: dict[str, str],
    ) -> GenerationResponse:
        response = self._post(payload, headers)

        return self._parse(response)

    def _post(
        self,
        payload: dict,
        headers: dict[str, str],
    ) -> httpx.Response:
        try:
            with httpx.Client(
                timeout=self._timeout_seconds,
            ) as client:
                response = client.post(
                    self.BASE_URL,
                    json=payload,
                    headers=headers,
                )
        except httpx.TimeoutException as exc:
            raise ProviderTimeoutError("LLM provider request timed out.") from exc
        except httpx.HTTPError as exc:
            raise TransientProviderError("LLM provider request failed.") from exc

        if response.status_code >= 400:
            # Status only. The response body can echo the request,
            # model name, or credential fragments, so it is never
            # surfaced.
            #
            # Transient statuses become retryable errors; everything
            # else stays a deterministic `ProviderResponseError`, which
            # the retry policy will not retry.
            if is_retryable_status(response.status_code):
                raise TransientProviderError(
                    "LLM provider returned a retryable status."
                )

            raise ProviderResponseError("LLM provider rejected the request.")

        return response

    def _parse(
        self,
        response: httpx.Response,
    ) -> GenerationResponse:
        try:
            data = response.json()
        except ValueError as exc:
            raise ProviderResponseError("LLM provider returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise ProviderResponseError("LLM provider returned an invalid payload.")

        choices = data.get("choices")

        if not isinstance(choices, list) or not choices:
            raise ProviderResponseError("LLM provider returned no choices.")

        first = choices[0]

        if not isinstance(first, dict):
            raise ProviderResponseError("LLM provider returned an invalid choice.")

        message = first.get("message")

        if not isinstance(message, dict):
            raise ProviderResponseError("LLM provider returned an invalid message.")

        content = message.get("content")

        if not isinstance(content, str):
            raise ProviderResponseError("LLM provider returned invalid content.")

        raw_usage = data.get("usage")
        usage = raw_usage if isinstance(raw_usage, dict) else {}

        model = data.get("model")

        return GenerationResponse(
            answer=content,
            model_name=(model if isinstance(model, str) and model else self._model_name),
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
        )

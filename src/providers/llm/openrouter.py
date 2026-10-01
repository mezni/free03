import httpx

from src.models.generation import (
    GenerationRequest,
    GenerationResponse,
)
from src.providers.llm.base import LLMProvider


class OpenRouterProvider(LLMProvider):
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        timeout_seconds: int,
    ) -> None:
        self._api_key = api_key
        self._model_name = model_name
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout_seconds = timeout_seconds

    @property
    def model_name(self) -> str:
        return self._model_name

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

        with httpx.Client(
            timeout=self._timeout_seconds,
        ) as client:
            response = client.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
            )

        response.raise_for_status()

        data = response.json()

        usage = data.get("usage") or {}

        return GenerationResponse(
            answer=data["choices"][0]["message"]["content"],
            model_name=data.get(
                "model",
                self._model_name,
            ),
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get(
                "completion_tokens"
            ),
            total_tokens=usage.get("total_tokens"),
        )
from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError

from ticket_triage.config import get_settings
from ticket_triage.errors import InvalidModelOutputError, TransientProviderError

_RECOMMENDATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "category": {"type": "string"},
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "urgent"],
        },
        "destination": {"type": "string"},
        "rationale": {"type": "string"},
    },
    "required": ["category", "priority", "destination", "rationale"],
}


class OpenAILLMClient:
    """OpenAI implementation of the application's LLMClient protocol."""

    def __init__(
        self,
        *,
        model: str | None = None,
        client: OpenAI | None = None,
    ) -> None:
        settings = get_settings()
        self.model = model or settings.openai_model
        if client is not None:
            # Dependency injection keeps unit tests independent of the API.
            self.client = client
        else:
            if not settings.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required to use the real "
                    "OpenAI client."
                )
            self.client = OpenAI(
                api_key=settings.openai_api_key,
                timeout=20.0,
                max_retries=1,
            )

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "ticket_recommendation",
                        "strict": True,
                        "schema": _RECOMMENDATION_SCHEMA,
                    }
                },
            )
        except (APITimeoutError, APIConnectionError, RateLimitError) as exc:
            raise TransientProviderError(
                "Temporary OpenAI provider failure."
            ) from exc
        if not response.output_text:
            raise InvalidModelOutputError(
                "The OpenAI response contained no output text."
            )
        return response.output_text
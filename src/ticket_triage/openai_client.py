import os

from openai import APIConnectionError, APITimeoutError, OpenAI, RateLimitError

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
        self.model = model or os.getenv(
            "OPENAI_MODEL", "gpt-4o-mini"
        )
        # Injection allows tests to provide a fake client.
        self.client = client or OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
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
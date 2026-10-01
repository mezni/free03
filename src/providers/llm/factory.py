from src.config.settings import LLMConfig
from src.providers.llm.base import LLMProvider
from src.providers.llm.openrouter import OpenRouterProvider


class LLMProviderFactory:
    """Create LLM providers from configuration."""

    def create(
        self,
        config: LLMConfig,
        api_key: str | None,
    ) -> LLMProvider:
        provider_name = config.provider.strip().lower()

        if provider_name == "openrouter":
            if not api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY is required "
                    "for the OpenRouter provider."
                )

            return OpenRouterProvider(
                api_key=api_key,
                model_name=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout_seconds=config.timeout_seconds,
            )

        raise ValueError(
            f"Unsupported LLM provider: {config.provider}"
        )

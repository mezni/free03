from src.config.settings import LLMConfig, ReliabilityConfig
from src.providers.llm.base import LLMProvider
from src.providers.llm.openrouter import OpenRouterProvider
from src.providers.retry import RetryPolicy


class LLMProviderFactory:
    """Create LLM providers from configuration."""

    def create(
        self,
        config: LLMConfig,
        api_key: str | None,
        reliability: ReliabilityConfig | None = None,
    ) -> LLMProvider:
        provider_name = config.provider.strip().lower()

        if provider_name == "openrouter":
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is required for the OpenRouter provider.")

            llm_reliability = (
                reliability.llm if reliability is not None else LLMReliabilityDefaults()
            )

            return OpenRouterProvider(
                api_key=api_key,
                model_name=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout_seconds=llm_reliability.timeout_seconds,
                retry_policy=RetryPolicy(
                    max_retries=llm_reliability.max_retries,
                    delay_seconds=(llm_reliability.retry_delay_seconds),
                ),
            )

        raise ValueError(f"Unsupported LLM provider: {config.provider}")


class LLMReliabilityDefaults:
    """Fallback used when no reliability config is supplied.

    Matches `config/reliability.yaml` so a caller that omits
    configuration behaves like a correctly configured application.
    """

    timeout_seconds = 60
    max_retries = 0
    retry_delay_seconds = 0.0

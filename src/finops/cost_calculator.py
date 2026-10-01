from src.config.settings import FinOpsConfig

TOKENS_PER_PRICING_UNIT = 1_000_000


class CostCalculator:
    """Estimate spend from configured token prices.

    Deliberately independent of any LLM provider: rates come from
    configuration, because provider pricing changes without a code change.
    """

    def __init__(self, config: FinOpsConfig) -> None:
        self._config = config

    def calculate(
        self,
        provider: str,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        provider_pricing = self._config.pricing.get(provider)

        if provider_pricing is None:
            raise ValueError(f"No pricing configured for provider: {provider}")

        pricing = provider_pricing.get(model_name)

        if pricing is None:
            raise ValueError(f"No pricing configured for model: {model_name}")

        input_cost = (prompt_tokens / TOKENS_PER_PRICING_UNIT) * pricing.input_per_1m_tokens

        output_cost = (completion_tokens / TOKENS_PER_PRICING_UNIT) * pricing.output_per_1m_tokens

        return input_cost + output_cost

import logging

from src.db.repositories.llm_usage import LLMUsageRepository
from src.finops.cost_calculator import CostCalculator
from src.models.generation import GenerationResponse
from src.models.llm_usage import LLMUsageRecord

logger = logging.getLogger("rag-system.finops")


class UsageTracker:
    """Turn a provider response into a persisted usage record.

    Only real provider calls are recorded. A response served from a cache
    never reaches this tracker, because no provider request happened and
    therefore no provider tokens were consumed.

    Like the other services in this project, this owns the transaction and
    commits; the repository only flushes. Usage history is telemetry, so a
    write failure is logged rather than propagated into the answer path.
    """

    def __init__(
        self,
        repository: LLMUsageRepository,
        cost_calculator: CostCalculator,
        provider_name: str,
        currency: str,
    ) -> None:
        self._repository = repository
        self._cost_calculator = cost_calculator
        self._provider_name = provider_name
        self._currency = currency

    def record(
        self,
        response: GenerationResponse,
        request_id: str | None = None,
    ) -> LLMUsageRecord:
        prompt_tokens = response.prompt_tokens or 0
        completion_tokens = response.completion_tokens or 0
        total_tokens = (
            response.total_tokens
            if response.total_tokens is not None
            else prompt_tokens + completion_tokens
        )

        cost = self._estimate_cost(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model_name=response.model_name,
        )

        usage = LLMUsageRecord(
            request_id=request_id,
            provider=self._provider_name,
            model_name=response.model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost=cost,
            currency=self._currency,
        )

        try:
            stored = self._repository.create(usage)
            self._commit()
        except Exception:
            logger.exception(
                "Failed to persist LLM usage",
                extra={
                    "event": "finops.usage_persist_failed",
                    "model": response.model_name,
                },
            )

            return usage

        return stored

    def _estimate_cost(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model_name: str,
    ) -> float:
        try:
            return self._cost_calculator.calculate(
                provider=self._provider_name,
                model_name=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except ValueError:
            # Unpriced models still consumed tokens. Losing the token
            # record would be worse than recording an unknown cost as
            # zero, so the gap is logged instead.
            logger.warning(
                "No pricing configured for model",
                extra={
                    "event": "finops.pricing_missing",
                    "provider": self._provider_name,
                    "model": model_name,
                },
            )

            return 0.0

    def _commit(self) -> None:
        self._repository.session.commit()

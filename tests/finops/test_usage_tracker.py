from uuid import uuid4

from src.config.settings import FinOpsConfig, ModelPricing
from src.finops.cost_calculator import CostCalculator
from src.finops.usage_tracker import UsageTracker
from src.models.generation import GenerationResponse
from src.models.llm_usage import LLMUsageRecord


class FakeSession:
    def __init__(self) -> None:
        self.commits = 0

    def commit(self) -> None:
        self.commits += 1


class FakeUsageRepository:
    def __init__(self) -> None:
        self.session = FakeSession()
        self.created: list[LLMUsageRecord] = []

    def create(
        self,
        usage: LLMUsageRecord,
    ) -> LLMUsageRecord:
        self.created.append(usage)

        return usage.model_copy(
            update={"id": uuid4()}
        )


def make_tracker(
    repository: FakeUsageRepository,
    model_name: str = "test-model",
    currency: str = "USD",
) -> UsageTracker:
    return UsageTracker(
        repository=repository,  # type: ignore[arg-type]
        cost_calculator=CostCalculator(
            FinOpsConfig(
                currency=currency,
                pricing={
                    "openrouter": {
                        model_name: ModelPricing(
                            input_per_1m_tokens=1.0,
                            output_per_1m_tokens=2.0,
                        )
                    }
                },
            )
        ),
        provider_name="openrouter",
        currency=currency,
    )


def test_record_persists_tokens_and_cost() -> None:
    repository = FakeUsageRepository()

    tracker = make_tracker(repository)

    usage = tracker.record(
        GenerationResponse(
            answer="Billing disputes are filed within 30 days.",
            model_name="test-model",
            prompt_tokens=1_000_000,
            completion_tokens=500_000,
            total_tokens=1_500_000,
        ),
        request_id="req-1",
    )

    assert usage.provider == "openrouter"
    assert usage.model_name == "test-model"
    assert usage.request_id == "req-1"
    assert usage.prompt_tokens == 1_000_000
    assert usage.completion_tokens == 500_000
    assert usage.total_tokens == 1_500_000
    assert usage.estimated_cost == 2.0
    assert usage.currency == "USD"
    assert usage.id is not None
    assert len(repository.created) == 1


def test_record_derives_total_tokens_when_absent() -> None:
    repository = FakeUsageRepository()

    usage = make_tracker(repository).record(
        GenerationResponse(
            answer="answer",
            model_name="test-model",
            prompt_tokens=100,
            completion_tokens=40,
        )
    )

    assert usage.total_tokens == 140


def test_record_treats_missing_token_counts_as_zero() -> None:
    repository = FakeUsageRepository()

    usage = make_tracker(repository).record(
        GenerationResponse(
            answer="answer",
            model_name="test-model",
        )
    )

    assert usage.prompt_tokens == 0
    assert usage.completion_tokens == 0
    assert usage.total_tokens == 0
    assert usage.estimated_cost == 0.0


def test_record_commits() -> None:
    repository = FakeUsageRepository()

    make_tracker(repository).record(
        GenerationResponse(
            answer="answer",
            model_name="test-model",
            prompt_tokens=10,
            completion_tokens=10,
        )
    )

    assert repository.session.commits == 1


def test_unpriced_model_still_records_tokens() -> None:
    repository = FakeUsageRepository()

    usage = make_tracker(repository).record(
        GenerationResponse(
            answer="answer",
            model_name="unpriced-model",
            prompt_tokens=1_000,
            completion_tokens=500,
        )
    )

    assert usage.model_name == "unpriced-model"
    assert usage.prompt_tokens == 1_000
    assert usage.completion_tokens == 500
    assert usage.total_tokens == 1_500
    assert usage.estimated_cost == 0.0
    assert len(repository.created) == 1


def test_record_uses_configured_currency() -> None:
    repository = FakeUsageRepository()

    usage = make_tracker(
        repository, currency="EUR"
    ).record(
        GenerationResponse(
            answer="answer",
            model_name="test-model",
            prompt_tokens=1_000,
            completion_tokens=1_000,
        )
    )

    assert usage.currency == "EUR"
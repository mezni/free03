import pytest

from src.config.settings import FinOpsConfig, ModelPricing
from src.finops.cost_calculator import CostCalculator


def make_config(
    input_price: float = 1.0,
    output_price: float = 2.0,
) -> FinOpsConfig:
    return FinOpsConfig(
        currency="USD",
        pricing={
            "openrouter": {
                "test-model": ModelPricing(
                    input_per_1m_tokens=input_price,
                    output_per_1m_tokens=output_price,
                )
            }
        },
    )


def test_cost_calculation() -> None:
    calculator = CostCalculator(make_config())

    cost = calculator.calculate(
        provider="openrouter",
        model_name="test-model",
        prompt_tokens=1_000_000,
        completion_tokens=500_000,
    )

    assert cost == 2.0


def test_free_model_costs_nothing() -> None:
    calculator = CostCalculator(
        make_config(
            input_price=0.0,
            output_price=0.0,
        )
    )

    cost = calculator.calculate(
        provider="openrouter",
        model_name="test-model",
        prompt_tokens=1_000_000,
        completion_tokens=1_000_000,
    )

    assert cost == 0.0


def test_cost_scales_with_fractional_tokens() -> None:
    calculator = CostCalculator(
        make_config(
            input_price=3.0,
            output_price=6.0,
        )
    )

    cost = calculator.calculate(
        provider="openrouter",
        model_name="test-model",
        prompt_tokens=500_000,
        completion_tokens=250_000,
    )

    assert cost == pytest.approx(3.0)


def test_zero_tokens_cost_nothing() -> None:
    calculator = CostCalculator(make_config())

    cost = calculator.calculate(
        provider="openrouter",
        model_name="test-model",
        prompt_tokens=0,
        completion_tokens=0,
    )

    assert cost == 0.0


def test_unknown_provider_is_rejected() -> None:
    calculator = CostCalculator(make_config())

    with pytest.raises(
        ValueError,
        match="No pricing configured for provider: other",
    ):
        calculator.calculate(
            provider="other",
            model_name="test-model",
            prompt_tokens=1_000,
            completion_tokens=1_000,
        )


def test_unknown_model_is_rejected() -> None:
    calculator = CostCalculator(make_config())

    with pytest.raises(
        ValueError,
        match="No pricing configured for model: other-model",
    ):
        calculator.calculate(
            provider="openrouter",
            model_name="other-model",
            prompt_tokens=1_000,
            completion_tokens=1_000,
        )


def test_pricing_comes_from_configuration() -> None:
    cheap = CostCalculator(
        make_config(input_price=1.0, output_price=2.0)
    )
    expensive = CostCalculator(
        make_config(input_price=10.0, output_price=20.0)
    )

    tokens = {
        "provider": "openrouter",
        "model_name": "test-model",
        "prompt_tokens": 1_000_000,
        "completion_tokens": 1_000_000,
    }

    assert cheap.calculate(**tokens) == 3.0
    assert expensive.calculate(**tokens) == 30.0
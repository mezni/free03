from dataclasses import dataclass


@dataclass(frozen=True)
class SLOResult:
    name: str
    target: float
    observed: float
    sample_size: int

    @property
    def met(self) -> bool:
        return self.observed >= self.target

    @property
    def error_budget_remaining(self) -> float:
        if self.target >= 1.0:
            return 0.0

        allowed_failure_rate = 1.0 - self.target
        observed_failure_rate = 1.0 - self.observed

        if allowed_failure_rate <= 0:
            return 0.0

        remaining = (
            allowed_failure_rate - observed_failure_rate
        ) / allowed_failure_rate

        return max(0.0, min(1.0, remaining))


def evaluate_request_slo(
    *,
    name: str,
    successes: int,
    total: int,
    target: float,
) -> SLOResult:
    if total <= 0:
        raise ValueError("total must be > 0")
    if not 0 <= successes <= total:
        raise ValueError("successes must be between 0 and total")
    if not 0 < target <= 1:
        raise ValueError("target must be in (0, 1]")

    observed = successes / total

    return SLOResult(
        name=name,
        target=target,
        observed=observed,
        sample_size=total,
    )
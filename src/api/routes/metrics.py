from fastapi import APIRouter, Depends

from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics

router = APIRouter(
    prefix="/metrics",
    tags=["observability"],
)


def get_metrics_collector() -> MetricsCollector:
    return get_metrics()


@router.get("")
def metrics(
    collector: MetricsCollector = Depends(get_metrics_collector),
) -> dict[str, int]:
    return collector.snapshot()
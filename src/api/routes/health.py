import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.api.dependencies import get_db_session

logger = logging.getLogger("rag-system.health")


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@router.get("/ready")
def readiness(
    session: Session = Depends(get_db_session),
) -> dict[str, str]:
    try:
        session.execute(text("SELECT 1"))
    except Exception as exc:
        logger.warning(
            "Readiness check failed",
            extra={
                "event": "readiness.failed",
                "error_type": type(exc).__name__,
            },
        )

        raise HTTPException(
            status_code=503,
            detail="Database is unavailable.",
        ) from exc

    return {
        "status": "ready",
    }
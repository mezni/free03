from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    return datetime.now(UTC)


def iso_now() -> str:
    return utcnow().isoformat()

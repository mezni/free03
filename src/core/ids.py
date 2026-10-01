from __future__ import annotations

import uuid


def new_id() -> str:
    return uuid.uuid4().hex


def short_id(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]

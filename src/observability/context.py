from contextvars import ContextVar
from uuid import uuid4

_request_id: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def create_request_id() -> str:
    request_id = str(uuid4())

    _request_id.set(request_id)

    return request_id


def get_request_id() -> str | None:
    return _request_id.get()


def set_request_id(request_id: str) -> None:
    _request_id.set(request_id)
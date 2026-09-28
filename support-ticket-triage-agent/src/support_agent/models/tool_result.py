from typing import Any, Literal

from pydantic import BaseModel


class ToolExecutionResult(BaseModel):
    success: bool
    data: Any | None = None
    error: str | None = None
    error_type: str | None = None
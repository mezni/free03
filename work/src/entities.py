import uuid
from typing import TypeVar
from pydantic import BaseModel


UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class Task(BaseModel):

    task_code: UUIDType
    task_name: str
    task_description: str



import uuid
from typing import TypeVar
from pydantic import BaseModel


UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class Task(BaseModel):

    task_code: UUIDType
    task_name: str
    task_description: str


class Job(BaseModel):

    job_code: UUIDType
    job_name: str
    job_description: str
    job_start: str
    job_end: str
    job_status: str

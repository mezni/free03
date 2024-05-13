import uuid
from typing import TypeVar
from pydantic import BaseModel
from datetime import datetime

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class User(BaseModel):
    user_code: UUIDType
    user_name: str
    user_email: str
    user_passzord: str
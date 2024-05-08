import uuid
from typing import TypeVar

# from datetime import datetime
from pydantic import BaseModel

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class Organisation(BaseModel):

    org_code: UUIDType
    org_name: str


class Account(BaseModel):

    account_code: UUIDType
    account_name: str
    org_code: UUIDType

import uuid
from typing import TypeVar, Type
from pydantic import BaseModel
from src.infra.base import Base

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


T = TypeVar("T", bound=BaseModel)


def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)

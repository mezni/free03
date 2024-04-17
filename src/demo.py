###########
# -- Entity
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    age: int


###########
# -- Model
from sqlalchemy import Column, String, Integer

# from src.infra.db_base import Base

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


###########
# -- Repo interface
from abc import ABCMeta, abstractmethod


class AbstractUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, data: dict) -> User:
        raise NotImplementedError


###########
# -- Repo
class MemRepo(AbstractUserRepository):
    def __init__(self):
        self.users = []

    def add(self, data: dict) -> User:
        user = User(**data)
        self.users.append(user)
        return user

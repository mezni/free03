from abc import ABCMeta, abstractmethod
from src.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def store(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        raise NotImplementedError

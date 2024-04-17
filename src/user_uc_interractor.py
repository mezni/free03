from src.user import User
from src.user_repository import IUserRepository


class UserInteractor(IUserRepository):
    def __init__(self):
        pass

    def store(self, user: User):
        pass

    def find_by_id(self, user_id: int) -> User:
        pass

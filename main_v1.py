from abc import ABC, abstractmethod
from typing import List
import sqlite3


# Entities
class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email


# Repositories
class UserRepository(ABC):
    @abstractmethod
    def create_user(self, username: str, email: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_user(self, username: str, email: str) -> User:
        self.cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)", (username, email)
        )
        self.conn.commit()
        user_id = self.cursor.lastrowid
        return User(user_id, username, email)

    def get_user_by_id(self, user_id: int) -> User:
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2])

    def get_all_users(self) -> List[User]:
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        return [User(row[0], row[1], row[2]) for row in rows]


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create_user(self, username: str, email: str) -> User:
        user = User(self.next_id, username, email)
        self.users[self.next_id] = user
        self.next_id += 1
        return user

    def get_user_by_id(self, user_id: int) -> User:
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self.users.values())


# Use Cases
class UserInteractor:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, username: str, email: str) -> User:
        return self.user_repository.create_user(username, email)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all_users()


# Database initialization
def initialize_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            email TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Example usage
if __name__ == "__main__":
    initialize_database()
    #    user_repository = SQLiteUserRepository('users.db')
    user_repository = InMemoryUserRepository()
    user_interactor = UserInteractor(user_repository)

    # Create a user
    user = user_interactor.create_user("john_doe", "john@example.com")
    print("User created:", user.username, user.email)

    # Get user by ID
    user = user_interactor.get_user_by_id(user.user_id)
    print("User retrieved by ID:", user.username, user.email)

    # Get all users
    all_users = user_interactor.get_all_users()
    print("All Users:")
    for user in all_users:
        print(user.user_id, user.username, user.email)

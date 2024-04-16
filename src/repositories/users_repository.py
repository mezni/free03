from src.infra.db_config import DBConnectionHandler
from src.entities.users import Users


class UsersRepository:
    @classmethod
    def insert_user(cls, first_name: str, last_name: str, age: int) -> None:
        with DBConnectionHandler() as database:
            try:
                new_registry = Users(
                    first_name=first_name, last_name=last_name, age=age
                )
                database.session.add(new_registry)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

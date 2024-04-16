from sqlalchemy import text
from src.repositories.users_repository import UsersRepository
from src.infra.db_config import DBConnectionHandler
from src.infra.db_base import Base

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


def test_db_init():
    with DBConnectionHandler() as db_conn:
        engine = db_conn.get_engine()
        Base.metadata.create_all(engine)


def test_users_insert():
    mocked_first_name = "first"
    mocked_last_name = "last"
    mocked_age = 51

    users_repository = UsersRepository()
    users_repository.insert_user(mocked_first_name, mocked_last_name, mocked_age)

    sql = """
        SELECT * FROM users
        WHERE first_name = '{}'
        AND last_name = '{}'
        AND age = {}
    """.format(
        mocked_first_name, mocked_last_name, mocked_age
    )
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.first_name == mocked_first_name
    assert registry.last_name == mocked_last_name
    assert registry.age == mocked_age

    connection.execute(
        text(
            f"""
        DELETE FROM users WHERE id = {registry.id}
    """
        )
    )
    connection.commit()

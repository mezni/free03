from src.infra.db_config import DBConnectionHandler
from src.infra.db_base import Base
from src.entities.users import Users


def test_db_init():
    with DBConnectionHandler() as db_conn:
        engine = db_conn.get_engine()
        Base.metadata.create_all(engine)
        new_user = Users(first_name="Mohamed Ali", last_name="MEZNI", age=50)
        db_conn.session.add(new_user)
        db_conn.session.commit()


def test_db_user_create():
    with DBConnectionHandler() as db_conn:
        engine = db_conn.get_engine()
        new_user = Users(first_name="Mohamed Ali", last_name="MEZNI", age=50)
        db_conn.session.add(new_user)
        db_conn.session.commit()

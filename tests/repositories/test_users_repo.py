from src.repositories.users_repository import UsersRepository
from src.infra.db_config import DBConnectionHandler

users_repo = UsersRepository()
db_conn = DBConnectionHandler()

def test_repo():
    first_name="Mohamed Ali"
    last_name="MEZNI"
    age=50
    users_repo.insert_user(first_name=first_name,last_name=last_name,age=age)

    with db_conn.get_engine().begin() as conn:
        response = conn.exec_driver_sql("SELECT * FROM users WHERE id=1").all()
    assert response[0].id  == 1
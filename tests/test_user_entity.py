from src.user import User


def test_user_entity():
    user = User(user_id=1, name="dali", email="dali@example.com")
    assert user.user_id == 1
    assert user.name == "dali"
    assert user.email == "dali@example.com"

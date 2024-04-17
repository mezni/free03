import uuid
from src.demo import User
from src.demo import MemRepo


def test_user_entity():
    user_id = uuid.uuid4()
    user = User(user_id=user_id, first_name="Mohamed Ali", last_name="MEZNI", age=51)
    assert user.user_id == user_id
    assert user.first_name == "Mohamed Ali"
    assert user.last_name == "MEZNI"
    assert user.age == 51


def test_mem_repo():
    repo = MemRepo()
    repo.add(
        {
            "user_id": uuid.uuid4(),
            "first_name": "Mohamed Ali",
            "last_name": "MEZNI",
            "age": 51,
        }
    )

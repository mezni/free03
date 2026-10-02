import pytest

from support_agent.database import initialize_database


@pytest.fixture
def evaluation_database(
    monkeypatch,
    tmp_path,
):
    database_path = (
        tmp_path / "evaluation.db"
    )

    monkeypatch.setattr(
        "support_agent.database.DATABASE_PATH",
        database_path,
    )

    initialize_database()

    return database_path
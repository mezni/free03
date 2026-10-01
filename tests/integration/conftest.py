import pytest

from src.core.enums import IndexVersionStatus
from src.db.repositories.index_versions import IndexVersionRepository


@pytest.fixture(autouse=True)
def active_index_version(database_session) -> None:
    """Ensure an active index version exists for integration tests."""

    repository = IndexVersionRepository(database_session)

    if repository.get_active() is None:
        repository.create(
            version_number=1,
            status=IndexVersionStatus.ACTIVE.value,
            embedding_model="local-deterministic",
            embedding_dimensions=8,
        )

        database_session.commit()

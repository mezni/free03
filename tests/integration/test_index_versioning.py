from src.core.enums import IndexVersionStatus
from src.db.repositories.index_versions import IndexVersionRepository


def test_get_active_index_version(database_session):
    repository = IndexVersionRepository(database_session)

    version = repository.get_active()

    assert version is not None
    assert version.version_number == 1
    assert version.status == IndexVersionStatus.ACTIVE.value
    assert version.embedding_dimensions == 8

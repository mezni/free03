from src.core.enums import IndexVersionStatus
from src.services.versioning_service import VersioningService


def test_create_index_version(database_session):
    service = VersioningService(database_session)

    version = service.create_version(
        embedding_model="local-dev-v2",
        embedding_dimensions=8,
    )

    assert version.version_number >= 2
    assert version.status == IndexVersionStatus.BUILDING


def test_activate_index_version(database_session):
    service = VersioningService(database_session)

    version = service.create_version(
        embedding_model="local-dev-v2",
        embedding_dimensions=8,
    )

    service.activate_version(version)
    database_session.commit()

    active = service.get_active_version()

    assert active is not None
    assert active.id == version.id
    assert active.status == IndexVersionStatus.ACTIVE

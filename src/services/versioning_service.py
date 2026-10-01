from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import IndexVersionStatus
from src.db.models.index_version import IndexVersionDB
from src.db.repositories.index_versions import IndexVersionRepository
from src.models.indexing import IndexVersion


class VersioningService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = IndexVersionRepository(session)

    def create_version(
        self,
        embedding_model: str,
        embedding_dimensions: int,
    ) -> IndexVersionDB:
        return self.repository.create_building(
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
        )

    def activate_version(
        self,
        version: IndexVersionDB,
    ) -> IndexVersionDB:
        return self.repository.activate(version)

    def fail_version(
        self,
        version: IndexVersionDB,
    ) -> IndexVersionDB:
        return self.repository.mark_failed(version)

    def get_active_version(self) -> IndexVersionDB | None:
        return self.repository.get_active()

    def get_version(
        self,
        version_id: UUID,
    ) -> IndexVersion | None:
        version = self.repository.get_by_id(version_id)

        if version is None:
            return None

        return self.to_domain(version)

    @staticmethod
    def to_domain(version: IndexVersionDB) -> IndexVersion:
        return IndexVersion(
            id=version.id,
            version_number=version.version_number,
            status=IndexVersionStatus(version.status),
            embedding_model=version.embedding_model,
            embedding_dimensions=version.embedding_dimensions,
            created_at=version.created_at,
            activated_at=version.activated_at,
        )

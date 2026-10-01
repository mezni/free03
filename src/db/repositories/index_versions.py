from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.enums import IndexVersionStatus
from src.db.models.index_version import IndexVersionDB


class IndexVersionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        version_number: int,
        status: str,
        embedding_model: str,
        embedding_dimensions: int,
    ) -> IndexVersionDB:
        version = IndexVersionDB(
            version_number=version_number,
            status=status,
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
        )

        self.session.add(version)
        self.session.flush()

        return version

    def get_active(self) -> IndexVersionDB | None:
        statement = (
            select(IndexVersionDB)
            .where(IndexVersionDB.status == IndexVersionStatus.ACTIVE.value)
            .order_by(IndexVersionDB.version_number.desc())
            .limit(1)
        )

        return self.session.execute(statement).scalar_one_or_none()

    def get_by_version_number(
        self,
        version_number: int,
    ) -> IndexVersionDB | None:
        statement = select(IndexVersionDB).where(IndexVersionDB.version_number == version_number)

        return self.session.execute(statement).scalar_one_or_none()

    def get_by_id(
        self,
        version_id: UUID,
    ) -> IndexVersionDB | None:
        statement = select(IndexVersionDB).where(IndexVersionDB.id == version_id)

        return self.session.execute(statement).scalar_one_or_none()

    def get_next_version_number(self) -> int:
        statement = (
            select(IndexVersionDB.version_number)
            .order_by(IndexVersionDB.version_number.desc())
            .limit(1)
        )

        latest = self.session.execute(statement).scalar_one_or_none()

        if latest is None:
            return 1

        return latest + 1

    def create_building(
        self,
        embedding_model: str,
        embedding_dimensions: int,
    ) -> IndexVersionDB:
        version_number = self.get_next_version_number()

        version = IndexVersionDB(
            version_number=version_number,
            status=IndexVersionStatus.BUILDING.value,
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
        )

        self.session.add(version)
        self.session.flush()

        return version

    def activate(self, version: IndexVersionDB) -> IndexVersionDB:
        active_versions = (
            self.session.execute(
                select(IndexVersionDB).where(
                    IndexVersionDB.status == IndexVersionStatus.ACTIVE.value,
                    IndexVersionDB.id != version.id,
                )
            )
            .scalars()
            .all()
        )

        for active_version in active_versions:
            active_version.status = IndexVersionStatus.RETIRED.value

        version.status = IndexVersionStatus.ACTIVE.value
        version.activated_at = datetime.now(UTC)

        self.session.flush()

        return version

    def mark_failed(self, version: IndexVersionDB) -> IndexVersionDB:
        version.status = IndexVersionStatus.FAILED.value
        self.session.flush()

        return version

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.enums import IngestionRunStatus
from src.db.models.run import IngestionRunDB


class IngestionRunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        run_type: str,
    ) -> IngestionRunDB:
        run = IngestionRunDB(
            run_type=run_type,
            status=IngestionRunStatus.RUNNING.value,
        )

        self.session.add(run)
        self.session.flush()

        return run

    def get_by_id(
        self,
        run_id: UUID,
    ) -> IngestionRunDB | None:
        statement = select(IngestionRunDB).where(IngestionRunDB.id == run_id)

        return self.session.execute(statement).scalar_one_or_none()

    def mark_completed(
        self,
        run: IngestionRunDB,
    ) -> IngestionRunDB:
        run.status = IngestionRunStatus.COMPLETED.value
        run.completed_at = datetime.now(UTC)

        self.session.flush()

        return run

    def mark_failed(
        self,
        run: IngestionRunDB,
        error_message: str,
    ) -> IngestionRunDB:
        run.status = IngestionRunStatus.FAILED.value
        run.completed_at = datetime.now(UTC)
        run.error_message = error_message

        self.session.flush()

        return run

    def update_counts(
        self,
        run: IngestionRunDB,
        *,
        discovered_count: int | None = None,
        processed_count: int | None = None,
        skipped_count: int | None = None,
        failed_count: int | None = None,
    ) -> IngestionRunDB:
        if discovered_count is not None:
            run.discovered_count = discovered_count

        if processed_count is not None:
            run.processed_count = processed_count

        if skipped_count is not None:
            run.skipped_count = skipped_count

        if failed_count is not None:
            run.failed_count = failed_count

        self.session.flush()

        return run

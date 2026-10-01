from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select

from src.db.repositories.base import Repository
from src.db.models.ingestion_job import IngestionJobDB
from src.core.enums import IngestionJobStatus


class IngestionJobRepository(Repository):
    """Persistence operations for ingestion jobs."""

    def create(
        self,
        source: str,
        input_path: str,
    ) -> IngestionJobDB:
        """Create a new ingestion job."""
        job = IngestionJobDB(
            status=IngestionJobStatus.PENDING,
            source=source,
            input_path=input_path,
            created_at=self._get_current_time(),
        )
        self.session.add(job)
        self.session.flush()
        return job

    def get_by_id(self, job_id: UUID) -> IngestionJobDB | None:
        """Get a job by ID."""
        statement = select(IngestionJobDB).where(IngestionJobDB.id == job_id)
        return self.session.execute(statement).scalar_one_or_none()

    def get_pending(self) -> list[IngestionJobDB]:
        """Get all pending jobs."""
        statement = select(IngestionJobDB).where(
            IngestionJobDB.status == IngestionJobStatus.PENDING
        )
        return list(self.session.execute(statement).scalars().all())

    def get_running(self) -> list[IngestionJobDB]:
        """Get all running jobs."""
        statement = select(IngestionJobDB).where(
            IngestionJobDB.status == IngestionJobStatus.RUNNING
        )
        return list(self.session.execute(statement).scalars().all())

    def mark_running(self, job: IngestionJobDB) -> IngestionJobDB:
        """Mark a job as running."""
        job.status = IngestionJobStatus.RUNNING
        job.started_at = self._get_current_time()
        self.session.flush()
        return job

    def mark_completed(
        self, job: IngestionJobDB, run_id: UUID, error_message: str | None = None
    ) -> IngestionJobDB:
        """Mark a job as completed."""
        job.status = IngestionJobStatus.COMPLETED
        job.run_id = run_id
        job.completed_at = self._get_current_time()
        if error_message:
            job.error_message = error_message
        self.session.flush()
        return job

    def mark_failed(self, job: IngestionJobDB, error_message: str) -> IngestionJobDB:
        """Mark a job as failed."""
        job.status = IngestionJobStatus.FAILED
        job.error_message = error_message
        job.completed_at = self._get_current_time()
        self.session.flush()
        return job

    def mark_cancelled(self, job: IngestionJobDB) -> IngestionJobDB:
        """Mark a job as cancelled."""
        job.status = IngestionJobStatus.CANCELLED
        job.completed_at = self._get_current_time()
        self.session.flush()
        return job

def _get_current_time(self) -> datetime:
        """Get current UTC time."""
        return datetime.now(tz=timezone.utc)
from uuid import UUID

from src.db.models.ingestion_job import IngestionJobDB
from src.db.repositories.ingestion_jobs import IngestionJobRepository
from src.models.ingestion_job import IngestionJob, IngestionJobStatus


class IngestionJobService:
    """Service for managing ingestion job lifecycle."""

    def __init__(self, repository: IngestionJobRepository) -> None:
        self._repository = repository

    def create_job(
        self,
        source: str,
        input_path: str,
    ) -> IngestionJob:
        """Create a new ingestion job in PENDING state."""
        db_job = self._repository.create(source=source, input_path=input_path)
        return self._to_domain(db_job)

    def get_job(self, job_id: UUID) -> IngestionJob | None:
        """Get a job by ID."""
        db_job = self._repository.get_by_id(job_id)
        if db_job is None:
            return None
        return self._to_domain(db_job)

    def start_job(self, job: IngestionJob) -> IngestionJob:
        """Transition job from PENDING to RUNNING."""
        if job.status != IngestionJobStatus.PENDING:
            raise ValueError(
                f"Cannot start job in status {job.status}. "
                "Only PENDING jobs can be started."
            )
        db_job = self._repository.get_by_id(job.id)
        if db_job is None:
            db_job = self._repository.create(source=job.source, input_path=job.input_path)
        db_job = self._repository.mark_running(db_job)
        return self._to_domain(db_job)

    def complete_job(
        self, job: IngestionJob, run_id: UUID
    ) -> IngestionJob:
        """Transition job from RUNNING to COMPLETED."""
        if job.status != IngestionJobStatus.RUNNING:
            raise ValueError(
                f"Cannot complete job in status {job.status}. "
                "Only RUNNING jobs can be completed."
            )
        db_job = self._repository.get_by_id(job.id)
        if db_job is None:
            db_job = self._repository.create(source=job.source, input_path=job.input_path)
        db_job = self._repository.mark_completed(db_job, run_id=run_id)
        return self._to_domain(db_job)

    def fail_job(self, job: IngestionJob, error_message: str) -> IngestionJob:
        """Transition job from RUNNING to FAILED."""
        if job.status != IngestionJobStatus.RUNNING:
            raise ValueError(
                f"Cannot fail job in status {job.status}. "
                "Only RUNNING jobs can be failed."
            )
        db_job = self._repository.get_by_id(job.id)
        if db_job is None:
            db_job = self._repository.create(source=job.source, input_path=job.input_path)
        db_job = self._repository.mark_failed(db_job, error_message=error_message)
        return self._to_domain(db_job)

    def cancel_job(self, job: IngestionJob) -> IngestionJob:
        """Transition job from PENDING/RUNNING to CANCELLED."""
        if job.status not in (
            IngestionJobStatus.PENDING,
            IngestionJobStatus.RUNNING,
        ):
            raise ValueError(
                f"Cannot cancel job in status {job.status}. "
                "Only PENDING or RUNNING jobs can be cancelled."
            )
        db_job = self._repository.get_by_id(job.id)
        if db_job is None:
            db_job = self._repository.create(source=job.source, input_path=job.input_path)
        db_job = self._repository.mark_cancelled(db_job)
        return self._to_domain(db_job)

    def _to_domain(self, db_job: IngestionJobDB) -> IngestionJob:
        """Convert database model to domain model."""
        return IngestionJob(
            id=db_job.id,
            status=IngestionJobStatus(db_job.status),
            run_id=db_job.run_id,
            source=db_job.source,
            input_path=db_job.input_path,
            created_at=db_job.created_at,
            started_at=db_job.started_at,
            completed_at=db_job.completed_at,
            error_message=db_job.error_message,
        )
from src.services.ingestion_service import IngestionService
from src.services.ingestion_job_service import IngestionJobService
from src.db.repositories.ingestion_jobs import IngestionJobRepository


class IngestionWorker:
    """Worker that processes ingestion jobs from the queue."""

    def __init__(
        self,
        job_repository: IngestionJobRepository,
        job_service: IngestionJobService,
        ingestion_service: IngestionService,
    ) -> None:
        self._job_repository = job_repository
        self._job_service = job_service
        self._ingestion_service = ingestion_service

    def process_next(self) -> bool:
        """Process the next pending ingestion job.

        Returns True if a job was processed, False if no pending jobs.
        """
        job = self._job_repository.get_pending()

        if job is None:
            return False

        # Transition from PENDING to RUNNING
        job = self._job_service.start_job(job)

        try:
            # Run the ingestion pipeline
            result = self._ingestion_service.ingest(path=job.input_path)

            # Transition from RUNNING to COMPLETED
            job = self._job_service.complete_job(job, run_id=result.run_id)

        except Exception as e:
            # Transition from RUNNING to FAILED
            job = self._job_service.fail_job(
                job, error_message=str(e)
            )

        return True

    def run_loop(self, sleep_seconds: float = 1.0) -> None:
        """Run the worker loop.

        Continuously process pending jobs with a sleep interval between checks.
        """
        import time

        while True:
            processed = self.process_next()

            if not processed:
                time.sleep(sleep_seconds)
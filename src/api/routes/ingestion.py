from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_ingestion_job_service, get_document_service
from src.models.ingestion_job import IngestionJob
from src.models.ingestion_api import (
    CreateIngestionJobRequest,
    CreateIngestionJobResponse,
    IngestionJobResponse,
)
from src.services.ingestion_job_service import IngestionJobService

router = APIRouter(
    prefix="/ingestion/jobs",
    tags=["ingestion-jobs"],
    dependencies=[Depends(get_document_service)],  # Auth guarded by API key
)


@router.post(
    "",
    response_model=CreateIngestionJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Create an ingestion job",
)
def create_ingestion_job(
    request: CreateIngestionJobRequest,
    service: IngestionJobService = Depends(get_ingestion_job_service),
):
    """Create a new ingestion job.

    Accepts a path and returns immediately with job ID and status.
    The actual ingestion is performed asynchronously by a worker.
    """
    job = service.create_job(
        source=request.source,
        input_path=request.input_path,
    )

    return CreateIngestionJobResponse(
        job_id=job.id,
        status=job.status,
    )


@router.get(
    "/{job_id}",
    response_model=IngestionJobResponse,
    summary="Get ingestion job status",
)
def get_ingestion_job(
    job_id: UUID,
    service: IngestionJobService = Depends(get_ingestion_job_service),
):
    """Get the status of an ingestion job."""
    job = service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingestion job not found.",
        )

    return IngestionJobResponse(
        job_id=job.id,
        status=job.status,
        run_id=job.run_id,
        source=job.source,
        input_path=job.input_path,
        created_at=str(job.created_at) if job.created_at else None,
        started_at=str(job.started_at) if job.started_at else None,
        completed_at=str(job.completed_at) if job.completed_at else None,
        error_message=job.error_message,
    )
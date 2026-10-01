from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_document_service, get_ingestion_service
from src.api.security import verify_api_key
from src.models.document_api import (
    DocumentDetailResponse,
    DocumentIngestRequest,
    DocumentIngestResponse,
    DocumentListResponse,
    DocumentSummary,
)
from src.services.document_service import DocumentService
from src.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(verify_api_key)],
)


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List documents with optional filtering and pagination",
)
def list_documents(
    service: DocumentService = Depends(get_document_service),
    source: str | None = Query(default=None, min_length=1, max_length=100),
    status: str | None = Query(default=None, min_length=1, max_length=50),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """List documents with optional filtering and pagination."""
    items, total = service.list_documents(
        source=source,
        status=status,
        limit=limit,
        offset=offset,
    )

    domain_items = [
        DocumentSummary(
            id=doc.id,  # type: ignore[arg-type]
            source=doc.source,
            source_uri=doc.source_uri,
            title=doc.title,
            document_type=doc.document_type,
            status=doc.status.value,
            created_at=str(doc.created_at) if doc.created_at else None,
            updated_at=str(doc.updated_at) if doc.updated_at else None,
        )
        for doc in items
    ]

    return DocumentListResponse(
        items=domain_items,
        total=total,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentDetailResponse,
    summary="Retrieve a document by ID",
)
def get_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """Retrieve a document by ID."""
    document = service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="The requested document was not found.",
        )

    return document


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document and its associated data",
)
def delete_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
) -> None:
    """Delete a document by ID."""
    service.delete_document(document_id)


@router.post(
    "/ingest",
    response_model=DocumentIngestResponse,
    summary="Trigger document ingestion from a path",
)
def ingest_documents(
    request: DocumentIngestRequest,
    service: IngestionService = Depends(get_ingestion_service),
):
    """Trigger document ingestion from a filesystem path."""
    result = service.ingest()

    return DocumentIngestResponse(
        run_id=str(result.run_id),
        discovered_count=result.discovered_count,
        processed_count=result.processed_count,
        skipped_count=result.skipped_count,
        failed_count=result.failed_count,
        document_ids=[str(did) for did in result.document_ids],
    )
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import (
    DocumentChangeType,
    DocumentProcessingOperation,
    DocumentProcessingStatus,
)
from src.db.repositories.documents import DocumentRepository
from src.ingestion.change_detection import ChangeDetector
from src.ingestion.chunking import DocumentChunker
from src.ingestion.cleaning import DocumentCleaner
from src.ingestion.context import DocumentInput, IngestionResult
from src.ingestion.loaders.base import DocumentLoader
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.sources.base import DocumentSource
from src.ingestion.stages.chunk import ChunkStage
from src.ingestion.stages.clean import CleanStage
from src.ingestion.stages.discover import DiscoveryStage
from src.ingestion.stages.embed import EmbedStage
from src.ingestion.stages.enrich import EnrichStage
from src.ingestion.stages.finalizer import FileFinalizer
from src.ingestion.stages.load import LoadStage
from src.ingestion.stages.parse import ParseStage
from src.models.ingestion import DocumentProcessingResult
from src.providers.embeddings.base import EmbeddingProvider
from src.services.document_processing_service import (
    DocumentProcessingService,
)
from src.services.indexing_service import IndexingService
from src.services.ingestion_run_service import IngestionRunService


class IngestionPipeline:
    """Execute the complete document ingestion pipeline."""

    _OPERATION_BY_CHANGE_TYPE: dict[
        DocumentChangeType,
        DocumentProcessingOperation,
    ] = {
        DocumentChangeType.NEW: DocumentProcessingOperation.ADD,
        DocumentChangeType.MODIFIED: DocumentProcessingOperation.UPDATE,
        DocumentChangeType.UNCHANGED: DocumentProcessingOperation.SKIP,
    }

    def __init__(
        self,
        source: DocumentSource,
        loader: DocumentLoader,
        parser: ParserRegistry,
        cleaner: DocumentCleaner,
        metadata_extractor: MetadataExtractor,
        chunker: DocumentChunker,
        embedding_provider: EmbeddingProvider,
        finalizer: FileFinalizer,
        session: Session,
    ) -> None:
        self.discovery_stage = DiscoveryStage(source)
        self.loader_stage = LoadStage(loader)
        self.parse_stage = ParseStage(parser)
        self.clean_stage = CleanStage(cleaner)
        self.enrich_stage = EnrichStage(metadata_extractor)
        self.chunk_stage = ChunkStage(chunker)
        self.embed_stage = EmbedStage(embedding_provider)
        self.finalizer = finalizer

        self.indexing_service = IndexingService(session)
        self.documents = DocumentRepository(session)
        self.run_service = IngestionRunService(session)
        self.processing_service = DocumentProcessingService(session)

        self.change_detector = ChangeDetector()

    def run(self) -> IngestionResult:
        """Run ingestion for all discovered documents."""

        discovered_documents = self.discovery_stage.execute()

        run = self.run_service.start("ingestion")

        document_ids: list[UUID] = []

        processed_count = 0
        skipped_count = 0
        failed_count = 0

        for document_input in discovered_documents:
            result = self._process_document(
                run_id=run.id,
                document_input=document_input,
            )

            if result.status == DocumentProcessingStatus.SUCCESS:
                processed_count += 1

                if result.document_id is not None:
                    document_ids.append(result.document_id)

                self.finalizer.finalize(document_input.path)

            elif result.status == DocumentProcessingStatus.SKIPPED:
                skipped_count += 1

            elif result.status == DocumentProcessingStatus.FAILED:
                failed_count += 1

        try:
            self.run_service.update_counts(
                run.id,
                discovered_count=len(discovered_documents),
                processed_count=processed_count,
                skipped_count=skipped_count,
                failed_count=failed_count,
            )

            self.run_service.complete(run.id)

        except Exception as exc:
            self.run_service.fail(
                run.id,
                str(exc),
            )
            raise

        return IngestionResult(
            run_id=run.id,
            discovered_count=len(discovered_documents),
            processed_count=processed_count,
            skipped_count=skipped_count,
            failed_count=failed_count,
            document_ids=document_ids,
        )

    def _process_document(
        self,
        run_id: UUID,
        document_input: DocumentInput,
    ) -> DocumentProcessingResult:
        """Process exactly one source document and record its outcome."""

        existing_document = self.documents.get_by_source_uri(
            document_input.source_uri
        )

        previous_content_hash = (
            existing_document.content_hash
            if existing_document is not None
            else None
        )

        change = self.change_detector.detect(
            document=document_input,
            previous_content_hash=previous_content_hash,
        )

        operation = self._operation_for(change.change_type)

        if change.change_type == DocumentChangeType.UNCHANGED:
            record = self.processing_service.record_skipped(
                run_id=run_id,
                source_uri=document_input.source_uri,
                document_id=(
                    existing_document.id
                    if existing_document is not None
                    else None
                ),
            )

            return self._to_result(record)

        try:
            raw_document = self.loader_stage.execute(change)
            parsed_document = self.parse_stage.execute(raw_document)
            cleaned_document = self.clean_stage.execute(parsed_document)
            enriched_document = self.enrich_stage.execute(cleaned_document)
            chunked_document = self.chunk_stage.execute(enriched_document)
            embedded_document = self.embed_stage.execute(chunked_document)

            if operation == DocumentProcessingOperation.UPDATE:
                if existing_document is None:
                    raise ValueError(
                        f"Cannot update missing document: "
                        f"{document_input.source_uri}"
                    )

                document_id = self.indexing_service.update(
                    embedded_document
                )

            else:
                document_id = self.indexing_service.add(
                    embedded_document
                )

            record = self.processing_service.record_success(
                run_id=run_id,
                document_id=document_id,
                source_uri=document_input.source_uri,
                operation=operation,
            )

            return self._to_result(record)

        except Exception as exc:
            record = self.processing_service.record_failure(
                run_id=run_id,
                document_id=(
                    existing_document.id
                    if existing_document is not None
                    else None
                ),
                source_uri=document_input.source_uri,
                operation=operation,
                error_message=str(exc),
            )

            return self._to_result(record)

    @classmethod
    def _operation_for(
        cls,
        change_type: DocumentChangeType,
    ) -> DocumentProcessingOperation:
        return cls._OPERATION_BY_CHANGE_TYPE[change_type]

    @staticmethod
    def _to_result(record) -> DocumentProcessingResult:
        return DocumentProcessingResult(
            id=record.id,
            run_id=record.run_id,
            document_id=record.document_id,
            source_uri=record.source_uri,
            operation=record.operation,
            status=record.status,
            error_message=record.error_message,
        )
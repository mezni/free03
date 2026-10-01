from pathlib import Path
from types import SimpleNamespace
from uuid import UUID, uuid4

from src.core.enums import (
    DocumentProcessingOperation,
    DocumentProcessingStatus,
)
from src.core.hashing import calculate_file_hash
from src.ingestion.chunkers.text import CharacterTextChunker
from src.ingestion.cleaners.text import TextDocumentCleaner
from src.ingestion.context import DocumentInput
from src.ingestion.loaders.filesystem import FilesystemLoader
from src.ingestion.metadata_extractor import FilesystemMetadataExtractor
from src.ingestion.parsers.markdown import MarkdownParser
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.parsers.text import TextParser
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.sources.filesystem import FilesystemSource
from src.ingestion.stages.finalizer import FileFinalizer
from src.providers.embeddings.local import LocalEmbeddingProvider


class _FakeSession:
    """In-memory session stub for pipelines that do not hit the database."""

    def __init__(self) -> None:
        self.added: list[object] = []

    def add(self, record: object) -> None:
        self.added.append(record)

    def flush(self) -> None:
        pass

    def commit(self) -> None:
        pass


class _FakeDocumentRepository:
    def __init__(self, existing) -> None:
        self._existing = existing

    def get_by_source_uri(self, source_uri: str):
        return self._existing


class _FakeIndexingService:
    def __init__(self, document_id: UUID) -> None:
        self.document_id = document_id
        self.added: list[object] = []
        self.updated: list[object] = []
        self.fail_add = False

    def add(self, data: object) -> UUID:
        self.added.append(data)

        if self.fail_add:
            raise ValueError("indexing failure")

        return self.document_id

    def update(self, data: object) -> UUID:
        self.updated.append(data)

        return self.document_id


def _write_document(tmp_path: Path, content: str) -> DocumentInput:
    document_path = tmp_path / "policy.md"
    document_path.write_text(content, encoding="utf-8")

    return DocumentInput(
        source="filesystem",
        source_uri=str(document_path),
        path=document_path,
    )


def _build_pipeline(tmp_path: Path, existing) -> IngestionPipeline:
    pipeline = IngestionPipeline(
        source=FilesystemSource(input_dir=tmp_path),
        loader=FilesystemLoader(),
        parser=ParserRegistry(
            parsers=[
                MarkdownParser(),
                TextParser(),
            ]
        ),
        cleaner=TextDocumentCleaner(),
        metadata_extractor=FilesystemMetadataExtractor(),
        chunker=CharacterTextChunker(
            chunk_size=500,
            chunk_overlap=50,
        ),
        embedding_provider=LocalEmbeddingProvider(dimensions=8),
        finalizer=FileFinalizer(
            processed_dir=tmp_path / "processed",
            archive_flag=True,
        ),
        session=_FakeSession(),
    )

    pipeline.documents = _FakeDocumentRepository(existing)
    pipeline.indexing_service = _FakeIndexingService(document_id=uuid4())

    return pipeline


def test_new_document_is_added(
    tmp_path: Path,
) -> None:
    document_input = _write_document(
        tmp_path,
        "# Billing Policy\n\nNew billing policy content.\n",
    )

    pipeline = _build_pipeline(tmp_path, existing=None)

    result = pipeline._process_document(
        run_id=uuid4(),
        document_input=document_input,
    )

    assert result.operation == DocumentProcessingOperation.ADD
    assert result.status == DocumentProcessingStatus.SUCCESS
    assert result.document_id == pipeline.indexing_service.document_id
    assert len(pipeline.indexing_service.added) == 1


def test_modified_document_is_updated(
    tmp_path: Path,
) -> None:
    document_input = _write_document(
        tmp_path,
        "# Billing Policy\n\nUpdated billing policy content.\n",
    )

    existing = SimpleNamespace(
        id=uuid4(),
        content_hash="0" * 64,
    )

    pipeline = _build_pipeline(tmp_path, existing=existing)

    result = pipeline._process_document(
        run_id=uuid4(),
        document_input=document_input,
    )

    assert result.operation == DocumentProcessingOperation.UPDATE
    assert result.status == DocumentProcessingStatus.SUCCESS
    assert result.document_id == pipeline.indexing_service.document_id
    assert len(pipeline.indexing_service.updated) == 1


def test_unchanged_document_is_skipped(
    tmp_path: Path,
) -> None:
    document_input = _write_document(
        tmp_path,
        "# Billing Policy\n\nUnchanged billing policy content.\n",
    )

    existing = SimpleNamespace(
        id=uuid4(),
        content_hash=calculate_file_hash(document_input.path),
    )

    pipeline = _build_pipeline(tmp_path, existing=existing)

    result = pipeline._process_document(
        run_id=uuid4(),
        document_input=document_input,
    )

    assert result.operation == DocumentProcessingOperation.SKIP
    assert result.status == DocumentProcessingStatus.SKIPPED
    assert result.document_id == existing.id
    assert pipeline.indexing_service.added == []
    assert pipeline.indexing_service.updated == []


def test_processing_exception_records_failure(
    tmp_path: Path,
) -> None:
    document_input = _write_document(
        tmp_path,
        "# Billing Policy\n\nBilling policy that triggers a failure.\n",
    )

    pipeline = _build_pipeline(tmp_path, existing=None)
    pipeline.indexing_service.fail_add = True

    result = pipeline._process_document(
        run_id=uuid4(),
        document_input=document_input,
    )

    assert result.operation == DocumentProcessingOperation.ADD
    assert result.status == DocumentProcessingStatus.FAILED
    assert result.error_message is not None
    assert "indexing failure" in result.error_message

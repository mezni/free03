from pathlib import Path

import pytest

from src.core.enums import IndexVersionStatus
from src.db.models.chunk import ChunkDB
from src.db.models.index_version import IndexVersionDB
from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.embeddings import EmbeddingRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.ingestion.chunkers.text import CharacterTextChunker
from src.ingestion.cleaners.text import TextDocumentCleaner
from src.ingestion.loaders.filesystem import FilesystemLoader
from src.ingestion.metadata_extractor import FilesystemMetadataExtractor
from src.ingestion.parsers.markdown import MarkdownParser
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.parsers.text import TextParser
from src.ingestion.sources.filesystem import FilesystemSource
from src.providers.embeddings.base import EmbeddingProvider
from src.providers.embeddings.local import LocalEmbeddingProvider
from src.services.index_validation_service import IndexValidationService
from src.services.indexing_service import IndexingService
from src.services.reindex_service import ReindexService
from src.services.versioning_service import VersioningService


class _FlakyEmbeddingProvider(EmbeddingProvider):
    """Embedding provider that fails on a specific call."""

    def __init__(
        self,
        provider: EmbeddingProvider,
        fail_on_call: int,
    ) -> None:
        self.provider = provider
        self.fail_on_call = fail_on_call
        self.calls = 0

    @property
    def model_name(self) -> str:
        return self.provider.model_name

    @property
    def dimensions(self) -> int:
        return self.provider.dimensions

    def embed_query(self, query: str) -> list[float]:
        return self.provider.embed_query(query)

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls += 1

        if self.calls == self.fail_on_call:
            raise RuntimeError("simulated embedding failure")

        return self.provider.embed(texts)


def _write_markdown(
    raw: Path,
    name: str,
    content: str,
) -> None:
    raw.mkdir(parents=True, exist_ok=True)
    (raw / name).write_text(content, encoding="utf-8")


def _build_reindex_service(
    database_session,
    raw: Path,
    embedding_provider: EmbeddingProvider | None = None,
) -> ReindexService:
    return ReindexService(
        versioning_service=VersioningService(database_session),
        indexing_service=IndexingService(database_session),
        validation_service=IndexValidationService(
            index_version_repository=IndexVersionRepository(database_session),
            chunk_repository=ChunkRepository(database_session),
            embedding_repository=EmbeddingRepository(database_session),
        ),
        document_source=FilesystemSource(
            input_dir=raw,
            patterns=("*.md", "*.txt"),
        ),
        document_loader=FilesystemLoader(),
        parser_registry=ParserRegistry(
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
        embedding_provider=(
            embedding_provider
            if embedding_provider is not None
            else LocalEmbeddingProvider(dimensions=8)
        ),
    )


def test_reindex_builds_activates_and_retires_previous(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"

    _write_markdown(
        raw,
        "policy.md",
        "# Security Policy\n\nAccess is granted by role.\n",
    )

    _write_markdown(
        raw,
        "billing.md",
        "# Billing\n\nCustomers are billed by service plan.\n",
    )

    versioning = VersioningService(database_session)

    old_version = versioning.create_version("local-deterministic", 8)
    versioning.activate_version(old_version)
    database_session.commit()

    service = _build_reindex_service(
        database_session,
        raw,
    )

    new_version = service.reindex(
        embedding_model="local-deterministic",
        embedding_dimensions=8,
    )

    assert new_version.status == IndexVersionStatus.ACTIVE

    retired = versioning.get_version(old_version.id)

    assert retired is not None
    assert retired.status == IndexVersionStatus.RETIRED

    chunks = (
        database_session.query(ChunkDB).filter(ChunkDB.index_version_id == new_version.id).all()
    )

    assert len(chunks) > 0
    assert all(chunk.index_version_id == new_version.id for chunk in chunks)


def test_reindex_failure_marks_version_failed_and_keeps_previous_active(
    database_session,
    tmp_path: Path,
) -> None:
    raw = tmp_path / "raw"

    _write_markdown(raw, "a.md", "# A\n\nAlpha content.\n")
    _write_markdown(raw, "b.md", "# B\n\nBeta content.\n")
    _write_markdown(raw, "c.md", "# C\n\nGamma content.\n")

    versioning = VersioningService(database_session)

    old_version = versioning.create_version("local-deterministic", 8)
    versioning.activate_version(old_version)
    database_session.commit()

    flaky = _FlakyEmbeddingProvider(
        LocalEmbeddingProvider(dimensions=8),
        fail_on_call=3,
    )

    service = _build_reindex_service(
        database_session,
        raw,
        embedding_provider=flaky,
    )

    with pytest.raises(RuntimeError, match="simulated embedding failure"):
        service.reindex(
            embedding_model="local-deterministic",
            embedding_dimensions=8,
        )

    active = versioning.get_version(old_version.id)

    assert active is not None
    assert active.status == IndexVersionStatus.ACTIVE

    versions = (
        database_session.query(IndexVersionDB).order_by(IndexVersionDB.version_number.asc()).all()
    )

    failed_versions = [
        version for version in versions if version.status == IndexVersionStatus.FAILED.value
    ]

    assert len(failed_versions) == 1

    assert (
        database_session.query(ChunkDB)
        .filter(ChunkDB.index_version_id == failed_versions[0].id)
        .count()
        == 0
    )

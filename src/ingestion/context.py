from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.core.enums import DocumentChangeType


class DocumentInput(BaseModel):
    """A document discovered by an ingestion source."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    source: str
    source_uri: str
    path: Path


class DocumentChange(BaseModel):
    """Result of comparing a document with its persisted state."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    document: DocumentInput
    change_type: DocumentChangeType
    content_hash: str
    previous_content_hash: str | None = None


class RawDocument(BaseModel):
    """Raw content loaded from a document source."""

    model_config = ConfigDict(
        extra="forbid",
    )

    document: DocumentInput
    content: str
    content_hash: str


class ParsedDocument(BaseModel):
    """Structured textual representation of a document."""

    model_config = ConfigDict(
        extra="forbid",
    )

    document: DocumentInput
    content: str
    content_hash: str
    format: str


class CleanedDocument(BaseModel):
    """Cleaned textual representation of a document."""

    model_config = ConfigDict(
        extra="forbid",
    )

    document: DocumentInput
    content: str
    content_hash: str
    format: str


class DocumentMetadata(BaseModel):
    """Metadata extracted from a document."""

    model_config = ConfigDict(extra="forbid")

    source: str
    source_uri: str
    file_name: str
    extension: str
    document_type: str
    title: str | None = None
    file_size_bytes: int
    modified_at: datetime


class EnrichedDocument(BaseModel):
    """Cleaned document with extracted metadata."""

    model_config = ConfigDict(extra="forbid")

    document: DocumentInput
    content: str
    content_hash: str
    format: str
    metadata: DocumentMetadata


class DocumentChunk(BaseModel):
    """A chunk of an enriched document."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document: DocumentInput
    content: str
    content_hash: str
    chunk_index: int
    start_char: int
    end_char: int
    metadata: DocumentMetadata


class ChunkedDocument(BaseModel):
    """An enriched document split into chunks."""

    model_config = ConfigDict(extra="forbid")

    document: DocumentInput
    content_hash: str
    metadata: DocumentMetadata
    chunks: list[DocumentChunk]


class ChunkEmbedding(BaseModel):
    """Embedding generated for a document chunk."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    vector: list[float]
    model_name: str
    dimensions: int


class EmbeddedDocument(BaseModel):
    """Document chunks with their embeddings."""

    model_config = ConfigDict(extra="forbid")

    document: DocumentInput
    content_hash: str
    metadata: DocumentMetadata
    chunks: list[DocumentChunk]
    embeddings: list[ChunkEmbedding]


class IngestionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: UUID

    discovered_count: int = Field(default=0, ge=0)
    processed_count: int = Field(default=0, ge=0)
    skipped_count: int = Field(default=0, ge=0)
    failed_count: int = Field(default=0, ge=0)

    document_ids: list[UUID] = Field(default_factory=list)

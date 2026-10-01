from pathlib import Path

import pytest

from src.ingestion.chunkers.text import CharacterTextChunker
from src.ingestion.context import (
    DocumentInput,
    DocumentMetadata,
    EnrichedDocument,
)


def create_document(tmp_path: Path) -> EnrichedDocument:
    path = tmp_path / "policy.md"

    content = "A" * 1000

    path.write_text(content, encoding="utf-8")

    document_input = DocumentInput(
        source="filesystem",
        source_uri=str(path),
        path=path,
    )

    metadata = DocumentMetadata(
        source="filesystem",
        source_uri=str(path),
        file_name="policy.md",
        extension=".md",
        document_type="markdown",
        title="Policy",
        file_size_bytes=1000,
        modified_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    )

    return EnrichedDocument(
        document=document_input,
        content=content,
        content_hash="a" * 64,
        format="markdown",
        metadata=metadata,
    )


def test_chunk_document(tmp_path: Path) -> None:
    document = create_document(tmp_path)

    chunker = CharacterTextChunker(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 3

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[2].chunk_index == 2

    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 500

    assert chunks[1].start_char == 450
    assert chunks[1].end_char == 950

    assert chunks[2].start_char == 900
    assert chunks[2].end_char == 1000


def test_chunker_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError):
        CharacterTextChunker(chunk_size=100, chunk_overlap=100)

    with pytest.raises(ValueError):
        CharacterTextChunker(chunk_size=100, chunk_overlap=101)

    with pytest.raises(ValueError):
        CharacterTextChunker(chunk_size=0)


def test_empty_document_returns_no_chunks(tmp_path: Path) -> None:
    document = create_document(tmp_path).model_copy(update={"content": ""})

    chunker = CharacterTextChunker()

    chunks = chunker.chunk(document)

    assert chunks == []

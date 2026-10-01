from pathlib import Path

from src.ingestion.context import (
    ChunkedDocument,
    DocumentChunk,
    DocumentInput,
    DocumentMetadata,
)
from src.ingestion.stages.embed import EmbedStage
from src.providers.embeddings.local import LocalEmbeddingProvider


def test_embed_stage(tmp_path: Path) -> None:
    path = tmp_path / "policy.md"

    path.write_text("Billing policy", encoding="utf-8")

    document = DocumentInput(
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
        title="Billing Policy",
        file_size_bytes=14,
        modified_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc),
    )

    chunk = DocumentChunk(
        chunk_id="chunk-1",
        document=document,
        content="Billing policy",
        content_hash="a" * 64,
        chunk_index=0,
        start_char=0,
        end_char=14,
        metadata=metadata,
    )

    input_document = ChunkedDocument(
        document=document,
        content_hash="a" * 64,
        metadata=metadata,
        chunks=[chunk],
    )

    stage = EmbedStage(LocalEmbeddingProvider(dimensions=8))

    result = stage.execute(input_document)

    assert len(result.embeddings) == 1
    assert result.embeddings[0].chunk_id == "chunk-1"
    assert result.embeddings[0].model_name == "local-dev"
    assert result.embeddings[0].dimensions == 8
    assert len(result.embeddings[0].vector) == 8

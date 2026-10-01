import hashlib
import os
from datetime import UTC, datetime
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from src.db.models.document import DocumentDB
from src.db.models.index_version import IndexVersionDB
from src.db.models.llm_usage import LLMUsageDB
from src.db.models.run import IngestionRunDB
from src.ingestion.context import (
    ChunkEmbedding,
    DocumentChunk,
    DocumentInput,
    DocumentMetadata,
    EmbeddedDocument,
)

load_dotenv()


@pytest.fixture
def embedded_document_factory():
    def factory(
        source_uri: str,
        content: str,
        *,
        source: str = "filesystem",
        dimensions: int = 8,
    ) -> EmbeddedDocument:
        metadata = DocumentMetadata(
            source=source,
            source_uri=source_uri,
            file_name="policy.md",
            extension=".md",
            document_type="markdown",
            title="Policy",
            file_size_bytes=100,
            modified_at=datetime.now(UTC),
        )

        document_input = DocumentInput(
            source=source,
            source_uri=source_uri,
            path=Path(source_uri),
        )

        return EmbeddedDocument(
            document=document_input,
            content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            metadata=metadata,
            chunks=[
                DocumentChunk(
                    chunk_id=f"{source_uri}#0",
                    document=document_input,
                    content=content,
                    content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
                    chunk_index=0,
                    start_char=0,
                    end_char=len(content),
                    metadata=metadata,
                )
            ],
            embeddings=[
                ChunkEmbedding(
                    chunk_id=f"{source_uri}#0",
                    vector=[0.1] * dimensions,
                    model_name="local-deterministic",
                    dimensions=dimensions,
                )
            ],
        )

    return factory


@pytest.fixture
def database_engine():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        pytest.fail("DATABASE_URL is not configured")

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    return engine


@pytest.fixture
def database_session(database_engine):
    with Session(database_engine) as session:
        yield session

        session.execute(delete(DocumentDB))
        session.execute(delete(IndexVersionDB))
        session.execute(delete(IngestionRunDB))
        session.execute(delete(LLMUsageDB))
        session.commit()

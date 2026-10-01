from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.embeddings import EmbeddingRepository


def test_chunk_and_embedding_persistence(database_session) -> None:
    chunk_repository = ChunkRepository(database_session)

    # This test will be expanded once the complete ingestion
    # persistence flow is connected.
    assert chunk_repository is not None
    assert EmbeddingRepository(database_session) is not None

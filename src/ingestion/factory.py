from pathlib import Path

from sqlalchemy.orm import Session

from src.ingestion.chunkers.text import CharacterTextChunker
from src.ingestion.cleaners.text import TextDocumentCleaner
from src.ingestion.loaders.filesystem import FilesystemLoader
from src.ingestion.metadata_extractor import FilesystemMetadataExtractor
from src.ingestion.parsers.markdown import MarkdownParser
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.parsers.text import TextParser
from src.ingestion.pipeline import IngestionPipeline
from src.ingestion.sources.filesystem import FilesystemSource
from src.ingestion.stages.finalizer import FileFinalizer
from src.providers.embeddings.local import LocalEmbeddingProvider


def create_filesystem_ingestion_pipeline(
    session: Session,
    input_dir: str | Path,
    processed_dir: str | Path = "data/processed",
    archive_flag: bool = True,
) -> IngestionPipeline:
    source = FilesystemSource(
        input_dir=input_dir,
        patterns=("*.md", "*.txt"),
    )

    loader = FilesystemLoader()

    parser = ParserRegistry(
        parsers=[
            MarkdownParser(),
            TextParser(),
        ]
    )

    cleaner = TextDocumentCleaner()

    metadata_extractor = FilesystemMetadataExtractor()

    chunker = CharacterTextChunker(
        chunk_size=500,
        chunk_overlap=50,
    )

    embedding_provider = LocalEmbeddingProvider(
        dimensions=8,
    )

    finalizer = FileFinalizer(
        processed_dir=Path(processed_dir),
        archive_flag=archive_flag,
    )

    return IngestionPipeline(
        source=source,
        loader=loader,
        parser=parser,
        cleaner=cleaner,
        metadata_extractor=metadata_extractor,
        chunker=chunker,
        embedding_provider=embedding_provider,
        finalizer=finalizer,
        session=session,
    )
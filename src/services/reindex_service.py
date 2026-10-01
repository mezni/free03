from uuid import UUID

from sqlalchemy.orm import Session

from src.core.enums import DocumentChangeType
from src.core.hashing import calculate_file_hash
from src.db.models.index_version import IndexVersionDB
from src.ingestion.chunking import DocumentChunker
from src.ingestion.cleaning import DocumentCleaner
from src.ingestion.context import DocumentChange
from src.ingestion.loaders.base import DocumentLoader
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.parsers.registry import ParserRegistry
from src.ingestion.sources.base import DocumentSource
from src.ingestion.stages.chunk import ChunkStage
from src.ingestion.stages.clean import CleanStage
from src.ingestion.stages.embed import EmbedStage
from src.ingestion.stages.enrich import EnrichStage
from src.ingestion.stages.load import LoadStage
from src.ingestion.stages.parse import ParseStage
from src.models.indexing import IndexVersion
from src.providers.embeddings.base import EmbeddingProvider
from src.services.index_validation_service import IndexValidationService
from src.services.indexing_service import IndexingService
from src.services.versioning_service import VersioningService


class ReindexService:
    """Coordinate source-to-index reindexing against a new index version.

    Builds a BUILDING version, ingests every discovered document into it,
    validates the version, then activates it (retiring the previous ACTIVE
    version). On failure the new version is marked FAILED and the previously
    active version is left untouched.
    """

    def __init__(
        self,
        versioning_service: VersioningService,
        indexing_service: IndexingService,
        validation_service: IndexValidationService,
        document_source: DocumentSource,
        document_loader: DocumentLoader,
        parser_registry: ParserRegistry,
        cleaner: DocumentCleaner,
        metadata_extractor: MetadataExtractor,
        chunker: DocumentChunker,
        embedding_provider: EmbeddingProvider,
    ) -> None:
        self.versioning_service = versioning_service
        self.indexing_service = indexing_service
        self.validation_service = validation_service
        self.document_source = document_source
        self.document_loader = document_loader
        self.parser_registry = parser_registry
        self.cleaner = cleaner
        self.metadata_extractor = metadata_extractor
        self.chunker = chunker
        self.embedding_provider = embedding_provider

        self._load_stage = LoadStage(self.document_loader)
        self._parse_stage = ParseStage(self.parser_registry)
        self._clean_stage = CleanStage(self.cleaner)
        self._enrich_stage = EnrichStage(self.metadata_extractor)
        self._chunk_stage = ChunkStage(self.chunker)
        self._embed_stage = EmbedStage(self.embedding_provider)

        self.session: Session = indexing_service.session

    def reindex(
        self,
        embedding_model: str,
        embedding_dimensions: int,
    ) -> IndexVersion:
        version = self.versioning_service.create_version(
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
        )

        try:
            self._build_version(version.id)

            validation = self.validation_service.validate(
                version.id
            )

            if not validation.valid:
                raise ValueError(
                    "Index validation failed: "
                    + "; ".join(validation.errors)
                )

            self.versioning_service.activate_version(version)

            self.session.commit()

            activated_version = self.versioning_service.get_version(
                version.id
            )

            if activated_version is None:
                raise ValueError(
                    f"Index version not found: {version.id}"
                )

            return activated_version

        except Exception:
            self.session.rollback()
            self._mark_failed(version)
            raise

    def _build_version(self, version_id: UUID) -> None:
        documents = self.document_source.discover()

        for document_input in documents:
            change = DocumentChange(
                document=document_input,
                change_type=DocumentChangeType.NEW,
                content_hash=calculate_file_hash(document_input.path),
            )

            raw_document = self._load_stage.execute(change)
            parsed_document = self._parse_stage.execute(raw_document)
            cleaned_document = self._clean_stage.execute(parsed_document)
            enriched_document = self._enrich_stage.execute(cleaned_document)
            chunked_document = self._chunk_stage.execute(enriched_document)
            embedded_document = self._embed_stage.execute(chunked_document)

            self.indexing_service.add_to_version(
                data=embedded_document,
                index_version_id=version_id,
            )

    def _mark_failed(self, version: IndexVersionDB) -> None:
        if version not in self.session:
            self.session.add(version)

        self.versioning_service.fail_version(version)
        self.session.commit()
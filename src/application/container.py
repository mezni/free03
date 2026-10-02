from sqlalchemy.orm import Session

from src.config.settings import Settings
from src.db.repositories.chunks import ChunkRepository
from src.db.repositories.documents import DocumentRepository
from src.db.repositories.embeddings import EmbeddingRepository
from src.db.repositories.index_versions import IndexVersionRepository
from src.db.repositories.ingestion_jobs import IngestionJobRepository
from src.db.repositories.keyword_search import KeywordSearchRepository
from src.db.repositories.knowledge_bases import KnowledgeBaseRepository
from src.db.repositories.llm_usage import LLMUsageRepository
from src.db.repositories.vector_search import VectorSearchRepository
from src.evaluation.answer.semantic import SimpleAnswerEvaluator
from src.evaluation.citation.evaluator import CitationEvaluator
from src.evaluation.grounding.evaluator import GroundingEvaluator
from src.evaluation.quality_gate import QualityGate
from src.finops.cost_calculator import CostCalculator
from src.finops.usage_tracker import UsageTracker
from src.generation.citations import CitationExtractor
from src.generation.context_builder import ContextBuilder
from src.generation.prompt_builder import PromptBuilder
from src.observability.metrics import MetricsCollector
from src.observability.registry import get_metrics
from src.providers.embeddings.base import EmbeddingProvider
from src.providers.embeddings.factory import EmbeddingProviderFactory
from src.providers.llm.base import LLMProvider
from src.providers.llm.factory import LLMProviderFactory
from src.retrieval.context.base import ContextSelector
from src.retrieval.context.simple import SimpleContextSelector
from src.retrieval.context.window import ContextWindowService
from src.retrieval.pipeline import RetrievalPipeline
from src.retrieval.query.base import QueryAnalyzer
from src.retrieval.query.expander import QueryExpander
from src.retrieval.query.simple import SimpleQueryAnalyzer
from src.retrieval.rerank.simple import SimpleReranker
from src.retrieval.search.hybrid import HybridSearchStrategy
from src.retrieval.search.keyword import KeywordSearchStrategy
from src.retrieval.search.vector import VectorSearchStrategy
from src.services.document_service import DocumentService
from src.services.evaluation_resolver import EvaluationResolver
from src.services.generation_service import GenerationService
from src.services.grounding_service import GroundingService
from src.services.rag_evaluation_service import RAGEvaluationService
from src.services.rag_service import RAGService
from src.services.retrieval_evaluation_runner import RetrievalEvaluationRunner
from src.services.retrieval_metrics_service import RetrievalMetricsService
from src.services.retrieval_service import RetrievalService


class ApplicationContainer:
    """Composition root for the RAG application."""

    def __init__(
        self,
        session: Session,
        settings: Settings,
    ) -> None:
        self._session = session
        self._settings = settings
        self._embedding_factory = EmbeddingProviderFactory()
        self._metrics = get_metrics()

    @property
    def metrics(self) -> MetricsCollector:
        """Process-wide collector, shared across containers.

        A collector built here would reset on every request, because the
        API constructs a new container per request.
        """
        return self._metrics

    def document_service(self) -> DocumentService:
        return DocumentService(session=self._session)

    def document_repository(self) -> DocumentRepository:
        return DocumentRepository(self._session)

    def chunk_repository(self) -> ChunkRepository:
        return ChunkRepository(self._session)

    def embedding_repository(self) -> EmbeddingRepository:
        return EmbeddingRepository(self._session)

    def index_version_repository(self) -> IndexVersionRepository:
        return IndexVersionRepository(self._session)

    def vector_search_repository(self) -> VectorSearchRepository:
        return VectorSearchRepository(self._session)

    def keyword_search_repository(self) -> KeywordSearchRepository:
        return KeywordSearchRepository(self._session)

    def llm_usage_repository(self) -> LLMUsageRepository:
        return LLMUsageRepository(self._session)

    def ingestion_job_repository(self) -> IngestionJobRepository:
        return IngestionJobRepository(self._session)

    def cost_calculator(self) -> CostCalculator:
        return CostCalculator(self._settings.finops)

    def embedding_provider(self) -> EmbeddingProvider:
        return self._embedding_factory.create(
            self._settings.embedding,
        )

    def retrieval_service(self) -> RetrievalService:
        embedding_provider = self.embedding_provider()
        vector_search_repository = self.vector_search_repository()
        keyword_search_repository = self.keyword_search_repository()

        vector_strategy = VectorSearchStrategy(
            embedding_provider=embedding_provider,
            repository=vector_search_repository,
        )

        keyword_strategy = KeywordSearchStrategy(
            repository=keyword_search_repository,
        )

        hybrid_strategy = HybridSearchStrategy(
            vector_strategy=vector_strategy,
            keyword_strategy=keyword_strategy,
        )

        return RetrievalService(
            search_strategy=hybrid_strategy,
            index_version_repository=self.index_version_repository(),
            embedding_provider=embedding_provider,
        )

    def query_analyzer(self) -> QueryAnalyzer:
        return SimpleQueryAnalyzer()

    def query_expander(self) -> QueryExpander:
        return QueryExpander()

    def context_window_service(self) -> ContextWindowService:
        return ContextWindowService(
            chunk_repository=self.chunk_repository(),
        )

    def context_selector(self) -> ContextSelector:
        return SimpleContextSelector()

    def retrieval_pipeline(self) -> RetrievalPipeline:
        advanced = self._settings.advanced_retrieval

        return RetrievalPipeline(
            retrieval_service=self.retrieval_service(),
            query_analyzer=self.query_analyzer(),
            reranker=(SimpleReranker() if advanced.reranking.enabled else None),
            context_window_service=(
                self.context_window_service() if advanced.context.window_enabled else None
            ),
            context_selector=self.context_selector(),
            rerank_candidate_k=advanced.reranking.candidate_k,
            window_size=advanced.context.window_size,
            max_chunks=advanced.context.max_chunks,
            metrics=self._metrics,
        )

    def evaluation_resolver(self) -> EvaluationResolver:
        return EvaluationResolver(
            document_repository=self.document_repository(),
            chunk_repository=self.chunk_repository(),
            index_version_repository=self.index_version_repository(),
        )

    def llm_provider(self) -> LLMProvider:
        factory = LLMProviderFactory()

        return factory.create(
            config=self._settings.llm,
            api_key=(self._settings.environment.openrouter_api_key),
            reliability=self._settings.reliability,
        )

    def usage_tracker(self) -> UsageTracker:
        return UsageTracker(
            repository=self.llm_usage_repository(),
            cost_calculator=self.cost_calculator(),
            provider_name=self._settings.llm.provider,
            currency=self._settings.finops.currency,
        )

    def generation_service(self) -> GenerationService:
        return GenerationService(
            llm_provider=self.llm_provider(),
            context_builder=ContextBuilder(),
            prompt_builder=PromptBuilder(),
            citation_extractor=CitationExtractor(),
            grounding_service=GroundingService(),
            usage_tracker=self.usage_tracker(),
            metrics=self._metrics,
        )

    def quality_gate(self) -> QualityGate:
        return QualityGate(self._settings.evaluation.quality_gate)

    def rag_service(self) -> RAGService:
        return RAGService(
            retrieval_pipeline=self.retrieval_pipeline(),
            generation_service=self.generation_service(),
            metrics=self._metrics,
        )

    def knowledge_base_service(self) -> KnowledgeBaseService:
        return KnowledgeBaseService(
            repository=KnowledgeBaseRepository(session=self._session),
        )

    def ingestion_service(self) -> IngestionService:
        from src.ingestion.chunkers.text import CharacterTextChunker
        from src.ingestion.cleaners.text import TextDocumentCleaner
        from src.ingestion.loaders.filesystem import FilesystemLoader
        from src.ingestion.metadata import MetadataExtractor
        from src.ingestion.parsers.registry import ParserRegistry
        from src.ingestion.pipeline import IngestionPipeline
        from src.ingestion.sources.filesystem import FilesystemSource
        from src.ingestion.stages.finalizer import FileFinalizer

        source = FilesystemSource(base_path=self._settings.ingestion.root_path)
        loader = FilesystemLoader()
        parser = ParserRegistry()
        cleaner = TextDocumentCleaner()
        metadata_extractor = MetadataExtractor()
        chunker = CharacterTextChunker()
        embedding_provider = self.embedding_provider()
        finalizer = FileFinalizer()

        pipeline = IngestionPipeline(
            source=source,
            loader=loader,
            parser=parser,
            cleaner=cleaner,
            metadata_extractor=metadata_extractor,
            chunker=chunker,
            embedding_provider=embedding_provider,
            finalizer=finalizer,
            session=self._session,
        )

        return IngestionService(pipeline=pipeline)

    def rag_evaluation_service(
        self,
    ) -> RAGEvaluationService:
        return RAGEvaluationService(
            rag_service=self.rag_service(),
            answer_evaluator=SimpleAnswerEvaluator(),
            citation_evaluator=CitationEvaluator(),
            grounding_evaluator=GroundingEvaluator(),
        )

    def retrieval_evaluation_runner(self) -> RetrievalEvaluationRunner:
        return RetrievalEvaluationRunner(
            retrieval_pipeline=self.retrieval_pipeline(),
            metrics_service=RetrievalMetricsService(),
            evaluation_resolver=self.evaluation_resolver(),
        )

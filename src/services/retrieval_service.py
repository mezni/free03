from src.db.repositories.index_versions import IndexVersionRepository
from src.models.retrieval import RetrievalQuery, RetrievalResult


class RetrievalService:
    """Search the active index version for the chunks closest to a query."""

    def __init__(
        self,
        index_version_repository: IndexVersionRepository,
        search_strategy,
        embedding_provider,
    ) -> None:
        self.index_version_repository = index_version_repository
        self.search_strategy = search_strategy
        # Held directly rather than reached through the strategy.
        # The dimension guard is a property of the active index
        # version, not of any one search strategy, and composite
        # strategies like HybridSearchStrategy do not expose an
        # embedding provider of their own.
        self.embedding_provider = embedding_provider

    def search(
        self,
        request: RetrievalQuery,
    ) -> list[RetrievalResult]:
        active_version = self.index_version_repository.get_active()

        if active_version is None:
            raise ValueError("No active index version exists")

        query_vector = self.embedding_provider.embed_query(request.query)

        if len(query_vector) != active_version.embedding_dimensions:
            raise ValueError("Query embedding dimensions do not match the active index version")

        return self.search_strategy.search(
            request,
            active_version.id,
        )

from src.config.settings import EmbeddingConfig
from src.providers.embeddings.base import EmbeddingProvider
from src.providers.embeddings.local import LocalEmbeddingProvider


class EmbeddingProviderFactory:
    """Create embedding providers from configuration."""

    def create(
        self,
        config: EmbeddingConfig,
    ) -> EmbeddingProvider:
        provider_name = config.provider.strip().lower()

        if provider_name == "local":
            return LocalEmbeddingProvider(
                dimensions=config.dimensions,
                model_name=config.model,
            )

        raise ValueError(
            f"Unsupported embedding provider: {config.provider}"
        )

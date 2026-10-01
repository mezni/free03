from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.loader import load_yaml_config
from src.evaluation.quality_gate import QualityGateConfig

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"

load_dotenv(BASE_DIR / ".env")


class ApplicationConfig(BaseModel):
    name: str = "rag-system"
    environment: str = "dev"


class LoggingConfig(BaseModel):
    level: str = "INFO"


class EmbeddingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=200)
    dimensions: int = Field(gt=0)


class LLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=200)
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(gt=0, le=100_000)


class LLMReliabilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout_seconds: int = Field(gt=0, le=300)
    max_retries: int = Field(ge=0, le=5)
    retry_delay_seconds: float = Field(ge=0.0, le=30.0)


class RetrievalReliabilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout_seconds: int = Field(gt=0, le=120)


class APIReliabilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_query_length: int = Field(gt=0, le=100_000)
    max_top_k: int = Field(gt=0, le=100)


class ReliabilityConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    llm: LLMReliabilityConfig
    retrieval: RetrievalReliabilityConfig
    api: APIReliabilityConfig


class ModelPricing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_per_1m_tokens: float = Field(ge=0)
    output_per_1m_tokens: float = Field(ge=0)


class ProviderPricing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    models: dict[str, ModelPricing]


class FinOpsConfig(BaseModel):
    """Currency and per-provider token pricing.

    Pricing lives in configuration rather than in provider code because
    provider rates change independently of application releases.
    """

    model_config = ConfigDict(extra="forbid")

    currency: str = Field(min_length=3, max_length=3)

    pricing: dict[str, dict[str, ModelPricing]]

    @property
    def providers(self) -> dict[str, ProviderPricing]:
        return {
            name: ProviderPricing(models=models)
            for name, models in self.pricing.items()
        }


class EvaluationConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quality_gate: QualityGateConfig


class QueryConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expansion_enabled: bool = False

    max_queries: int = Field(gt=0, le=10)


class ContextConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    window_enabled: bool = True

    window_size: int = Field(ge=0, le=5)

    max_chunks: int = Field(gt=0, le=50)


class RerankingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = True

    candidate_k: int = Field(gt=0, le=100)


class AdvancedRetrievalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: QueryConfig
    context: ContextConfig
    reranking: RerankingConfig


class EnvironmentSettings(BaseSettings):
    """Environment-specific settings loaded from .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="dev")
    database_url: str
    openrouter_api_key: str | None = None


class Settings(BaseModel):
    """Complete application configuration."""

    environment: EnvironmentSettings
    application: ApplicationConfig
    logging: LoggingConfig
    embedding: EmbeddingConfig
    llm: LLMConfig
    reliability: ReliabilityConfig
    finops: FinOpsConfig
    evaluation: EvaluationConfig
    advanced_retrieval: AdvancedRetrievalConfig

    @property
    def application_name(self) -> str:
        return self.application.name

    @property
    def environment_name(self) -> str:
        return self.application.environment

    @property
    def database_url(self) -> str:
        return self.environment.database_url

    @property
    def openrouter_api_key(self) -> str | None:
        return self.environment.openrouter_api_key


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    environment = EnvironmentSettings(_env_file=None)  # type: ignore[call-arg]

    settings_data = load_yaml_config(CONFIG_DIR / "settings.yaml")
    embedding_data = load_yaml_config(
        CONFIG_DIR / "embedding.yaml"
    )
    llm_data = load_yaml_config(CONFIG_DIR / "llm.yaml")
    reliability_data = load_yaml_config(
        CONFIG_DIR / "reliability.yaml"
    )
    finops_data = load_yaml_config(CONFIG_DIR / "finops.yaml")
    evaluation_data = load_yaml_config(
        CONFIG_DIR / "evaluation.yaml"
    )
    advanced_retrieval_data = load_yaml_config(
        CONFIG_DIR / "advanced_retrieval.yaml"
    )

    return Settings(
        environment=environment,
        application=ApplicationConfig.model_validate(
            settings_data["application"]
        ),
        logging=LoggingConfig.model_validate(
            settings_data["logging"]
        ),
        embedding=EmbeddingConfig.model_validate(
            embedding_data["embedding"]
        ),
        llm=LLMConfig.model_validate(llm_data["llm"]),
        reliability=ReliabilityConfig.model_validate(
            reliability_data["reliability"]
        ),
        finops=FinOpsConfig.model_validate(
            finops_data["finops"]
        ),
        evaluation=EvaluationConfig.model_validate(
            evaluation_data
        ),
        advanced_retrieval=AdvancedRetrievalConfig.model_validate(
            advanced_retrieval_data["advanced_retrieval"]
        ),
    )
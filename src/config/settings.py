from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.loader import load_yaml_config

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
    environment = EnvironmentSettings()

    settings_data = load_yaml_config(CONFIG_DIR / "settings.yaml")
    embedding_data = load_yaml_config(
        CONFIG_DIR / "embedding.yaml"
    )
    llm_data = load_yaml_config(CONFIG_DIR / "llm.yaml")
    reliability_data = load_yaml_config(
        CONFIG_DIR / "reliability.yaml"
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
    )
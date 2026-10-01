from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field
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
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    dimensions: int = Field(gt=0)


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
    )
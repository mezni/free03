from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "triage-ai"
    environment: str = "development"
    debug: bool = True
    openrouter_api_key: str
    openrouter_model: str = "openrouter/free"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
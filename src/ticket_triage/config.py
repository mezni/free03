"""Centralized application configuration."""

import json
from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["development", "test", "production"] = Field(
        default="development",
        validation_alias="APP_ENV",
    )
    database_path: str = Field(
        default="ticket_triage.db",
        min_length=1,
        validation_alias="TRIAGE_DATABASE_PATH",
    )
    openai_api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )
    openai_model: str = Field(
        default="gpt-4o-mini",
        min_length=1,
        validation_alias="OPENAI_MODEL",
    )
    api_tokens_json: str = Field(
        default="{}",
        validation_alias="TRIAGE_API_TOKENS",
    )

    @field_validator("api_tokens_json")
    @classmethod
    def _validate_token_registry(cls, value: str) -> str:
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            raise ValueError(
                "TRIAGE_API_TOKENS must be a valid JSON object."
            )
        if not isinstance(parsed, dict):
            raise ValueError(
                "TRIAGE_API_TOKENS must be a valid JSON object."
            )
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
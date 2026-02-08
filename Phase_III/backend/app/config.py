"""Configuration settings for the Task CRUD API application."""

import logging
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(..., validation_alias="DATABASE_URL")

    # Authentication
    better_auth_secret: str = Field(..., validation_alias="BETTER_AUTH_SECRET")
    gemini_api_key: str = Field(..., validation_alias="GEMINI_API_KEY")
    claude_api_key: Optional[str] = Field(None, validation_alias="CLAUDE_API_KEY")

    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True
    log_level: str = "INFO"

    # Application
    app_name: str = "Task CRUD API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def LOG_LEVEL(self) -> int:
        """Convert log level string to logging constant."""
        return getattr(logging, self.log_level.upper(), logging.INFO)


# Instantiate settings (loaded from environment variables or .env file)
settings = Settings()

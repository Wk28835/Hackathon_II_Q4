"""Configuration settings for the Task CRUD API application."""

import logging
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://neondb_owner:npg_tJ8NEvh9dHGV@ep-still-fog-a4ctbf4n-pooler.us-east-1.aws.neon.tech/hackthonQ4_db?sslmode=require&channel_binding=require"

    # Authentication
    better_auth_secret: str = "PrkNWTriWNtT6lO+L/R2WufIiY9cshUs6HjiiGSW1xU="
    claude_api_key: str = "dummy-key-for-dev"
    gemini_api_key: Optional[str] = None

    # API
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True
    log_level: str = "INFO"

    # Application
    app_name: str = "Task CRUD API"
    app_version: str = "1.0.0"

    class Config:
        """Pydantic config for loading from .env file."""

        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    @property
    def LOG_LEVEL(self) -> int:
        """Convert log level string to logging constant."""
        return getattr(logging, self.log_level.upper(), logging.INFO)


# Instantiate settings (loaded from environment variables or .env file)
settings = Settings()

"""Configuration settings for the Task CRUD API application."""

import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database (Neon URL from .env)
    # Hint: Ensure your .env has DATABASE_URL
    database_url: str 

    # Authentication (BetterAuth Secret from .env)
    better_auth_secret: str

    # API Configuration
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    debug: bool = True
    log_level: str = "INFO"

    # Application Metadata
    app_name: str = "Task CRUD API"
    app_version: str = "1.0.0"

    # Pydantic v2 Settings Configuration
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=False, 
        extra="ignore"
    )

    @property
    def LOG_LEVEL(self) -> int:
        """Convert log level string to logging constant."""
        return getattr(logging, self.log_level.upper(), logging.INFO)

    @property
    def sqlalchemy_database_url(self) -> str:
        """
        Fixes the database URL for SQLAlchemy compatibility.
        Neon/Postgres URLs often need 'postgresql+asyncpg://' for FastAPI.
        """
        if self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql+asyncpg://", 1)
        return self.database_url


# Instantiate settings
settings = Settings()
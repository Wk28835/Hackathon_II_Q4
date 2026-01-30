"""Database connection and session management for Task CRUD API."""

import logging
import ssl
from typing import AsyncGenerator
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

logger = logging.getLogger(__name__)


def _make_async_database_url(url: str) -> tuple[str, dict]:
    """Ensure the SQLAlchemy URL uses an async driver and handle SSL for asyncpg.

    Returns:
        Tuple of (processed_url, connect_args dict for SSL)
    """
    connect_args = {}

    # Parse URL to handle query parameters
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    # Check for sslmode and convert to asyncpg-compatible SSL
    if "sslmode" in query_params:
        sslmode = query_params.pop("sslmode")[0]
        if sslmode in ("require", "verify-ca", "verify-full"):
            # Create SSL context for asyncpg
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connect_args["ssl"] = ssl_context

    # Remove channel_binding as asyncpg doesn't support it
    query_params.pop("channel_binding", None)

    # Rebuild query string without unsupported params
    new_query = urlencode({k: v[0] for k, v in query_params.items()})

    # Rebuild URL
    new_parsed = parsed._replace(query=new_query)
    url = urlunparse(new_parsed)

    # Convert to async driver
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("sqlite://"):
        url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)

    return url, connect_args


# Process database URL and get connect args
_async_url, _connect_args = _make_async_database_url(settings.database_url)

# Create async engine for PostgreSQL
engine = create_async_engine(
    _async_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
    connect_args=_connect_args,
)


# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def create_db_and_tables() -> None:
    """Create database tables on application startup."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

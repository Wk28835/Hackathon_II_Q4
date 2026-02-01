"""FastAPI application entry point for Task CRUD API."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes, chat
from app.config import settings
from app.database import create_db_and_tables
from app.middleware.error_handler import register_error_handlers
from app.middleware.metrics import MetricsLoggingMiddleware


# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events."""
    # Startup
    logger.info("Starting Task CRUD API...")
    await create_db_and_tables()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down Task CRUD API...")


# Create FastAPI application
app = FastAPI(
    title="Task CRUD API",
    description="Authenticated, user-scoped Task CRUD API with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Docusaurus dev
        "https://hackathoniiq4phaseiifrontend-sigma.vercel.app",
        "hackathoniiq4phaseiifrontend-m44ci5b8z.vercel.app",  # (add later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics middleware (request/response latency + status)
app.add_middleware(MetricsLoggingMiddleware)

# Register error handlers
register_error_handlers(app)


app.include_router(routes.health_router)
app.include_router(routes.router)
app.include_router(chat.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
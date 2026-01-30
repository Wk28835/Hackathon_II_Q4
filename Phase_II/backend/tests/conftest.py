"""Pytest fixtures for Task CRUD API tests."""

import asyncio
from typing import AsyncGenerator

import pytest
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from app.config import settings
from app.models.task import Task


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db():
    """Create a test database and tables.

    Returns a sessionmaker factory so tests can do:
        async with test_db() as session:
            ...

    Note: We use StaticPool so the in-memory sqlite DB persists across
    multiple connections.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    yield async_session_factory

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def client(test_db):
    """FastAPI TestClient wired to the async sqlite test DB.

    We patch the app's database engine/session so startup does not try to
    connect to the real DATABASE_URL.

    Note: `test_db` already created tables using an in-memory DB that persists
    across connections (StaticPool).
    """
    from fastapi.testclient import TestClient

    from app.database import get_session
    from app.main import app

    # Patch app.database globals used during lifespan startup.
    import app.database as app_database

    async_session_factory = test_db

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            yield session

    # Save originals so we can restore them after the test.
    original_engine = app_database.engine
    original_async_session = app_database.async_session

    app_database.engine = async_session_factory.kw["bind"]  # type: ignore[attr-defined]
    app_database.async_session = async_session_factory

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app, raise_server_exceptions=True) as c:
        yield c

    app.dependency_overrides.clear()

    app_database.engine = original_engine
    app_database.async_session = original_async_session
    return



@pytest.fixture
def auth_headers(test_jwt_token):
    """Authorization header for the default test user."""
    return {"Authorization": f"Bearer {test_jwt_token}"}


@pytest.fixture
def other_auth_headers(other_user_jwt_token):
    """Authorization header for the other test user."""
    return {"Authorization": f"Bearer {other_user_jwt_token}"}


@pytest.fixture
def invalid_auth_headers(invalid_jwt_token):
    """Authorization header with invalid token."""
    return {"Authorization": f"Bearer {invalid_jwt_token}"}


@pytest.fixture
async def sample_task_id(client, auth_headers):
    """Create a task via API and return its ID."""
    resp = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Sample task", "description": "This is a sample task"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture
async def sample_complete_task_id(client, auth_headers):
    """Create a completed task via API and return its ID."""
    resp = client.post(
        "/api/tasks",
        headers=auth_headers,
        json={"title": "Completed task", "description": "This is a completed task"},
    )
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    resp2 = client.patch(
        f"/api/tasks/{task_id}/status",
        headers=auth_headers,
        json={"status": "Complete"},
    )
    assert resp2.status_code == 200
    return task_id


@pytest.fixture
async def other_user_task_id(client, other_auth_headers):
    """Create a task owned by another user and return its ID."""
    resp = client.post(
        "/api/tasks",
        headers=other_auth_headers,
        json={"title": "Other user's task", "description": "This task belongs to another user"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


@pytest.fixture
def test_user_id():
    """Test user ID (string to match Better Auth format)."""
    return "test_user_42"


@pytest.fixture
def test_jwt_token(test_user_id):
    """Generate a valid JWT token for testing."""
    payload = {
        "sub": str(test_user_id),
        "exp": 9999999999,  # Far in the future
    }
    token = jwt.encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256",
    )
    return token


@pytest.fixture
def invalid_jwt_token():
    """Generate an invalid JWT token for testing."""
    return "invalid.token.here"


@pytest.fixture
def other_user_jwt_token():
    """Generate a JWT token for a different user."""
    other_user_id = "other_user_99"
    payload = {
        "sub": other_user_id,
        "exp": 9999999999,
    }
    token = jwt.encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256",
    )
    return token


@pytest.fixture
async def sample_task(test_db, test_user_id):
    """Create a sample task in the test database."""
    async with test_db() as session:
        task = Task(
            user_id=test_user_id,
            title="Sample task",
            description="This is a sample task",
            status="Incomplete",
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


@pytest.fixture
async def sample_complete_task(test_db, test_user_id):
    """Create a sample completed task in the test database."""
    async with test_db() as session:
        task = Task(
            user_id=test_user_id,
            title="Completed task",
            description="This is a completed task",
            status="Complete",
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


@pytest.fixture
async def other_user_task(test_db):
    """Create a task owned by another user."""
    other_user_id = 99
    async with test_db() as session:
        task = Task(
            user_id=other_user_id,
            title="Other user's task",
            description="This task belongs to another user",
            status="Incomplete",
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

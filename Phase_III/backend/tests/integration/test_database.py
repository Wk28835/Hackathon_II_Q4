"""Database integration tests.

This file exists to match the tasks.md artifact list:
- T042: Create database integration tests in backend/tests/integration/test_database.py

These tests focus on basic transaction behavior and concurrent DB usage. They do not
require a live PostgreSQL instance; they use the async SQLite test DB fixture.
"""

import asyncio

import pytest

from app.crud.task import create_task, update_task


class TestDatabaseIntegration:
    """Database-focused integration tests."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_updates_do_not_crash(self, test_db, test_user_id):
        """Test: concurrent updates complete without raising exceptions.

        Each concurrent update uses its own DB session.
        """
        async with test_db() as session:
            task = await create_task(
                session=session,
                user_id=test_user_id,
                title="Initial",
                description="",
            )
            task_id = task.id

        async def do_update(i: int):
            async with test_db() as session:
                return await update_task(
                    session=session,
                    task_id=task_id,
                    user_id=test_user_id,
                    title=f"Title {i}",
                    description=f"Desc {i}",
                )

        results = await asyncio.gather(
            *(do_update(i) for i in range(20)), return_exceptions=True
        )
        assert all(r is not None and not isinstance(r, Exception) for r in results)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_create_many_tasks_persists(self, test_db, test_user_id):
        """Test: creating multiple tasks persists and returns IDs."""
        async with test_db() as session:
            tasks = []
            for i in range(25):
                tasks.append(
                    await create_task(
                        session=session,
                        user_id=test_user_id,
                        title=f"Task {i}",
                        description="",
                    )
                )
            assert len({t.id for t in tasks}) == 25

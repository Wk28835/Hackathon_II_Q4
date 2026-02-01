"""Concurrency and concurrent request tests."""

import asyncio

import pytest

from app.crud.task import create_task, list_tasks
from app.models.task import Task


class TestConcurrentCreation:
    """Test concurrent task creation."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_task_creation(self, test_db, test_user_id):
        """Test: 100 concurrent task creations complete successfully.

        Each concurrent task uses its own DB session.
        """

        async def do_create(i: int) -> Task:
            async with test_db() as session:
                return await create_task(
                    session=session,
                    user_id=test_user_id,
                    title=f"Task {i}",
                    description=f"Description for task {i}",
                )

        results = await asyncio.gather(
            *(do_create(i) for i in range(100)), return_exceptions=True
        )

        assert len(results) == 100
        assert all(isinstance(r, Task) for r in results)

        task_ids = [r.id for r in results]
        assert len(set(task_ids)) == 100

        # Verify tasks can be listed after concurrent creation
        async with test_db() as session:
            listed = await list_tasks(session=session, user_id=test_user_id)
            assert len(listed) >= 100


class TestConcurrentRetrieval:
    """Test concurrent task retrieval."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_task_listing(self, test_db, test_user_id, sample_task):
        """Test: 50 concurrent list requests complete successfully.

        Each concurrent list uses its own DB session.
        """

        async def do_list() -> list[Task]:
            async with test_db() as session:
                return await list_tasks(session=session, user_id=test_user_id)

        results = await asyncio.gather(
            *(do_list() for _ in range(50)), return_exceptions=True
        )

        assert len(results) == 50
        assert all(isinstance(r, list) for r in results)
        assert all(len(r) >= 1 for r in results)

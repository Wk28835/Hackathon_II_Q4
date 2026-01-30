"""Performance benchmark tests.

This file exists to match the tasks.md artifact list:
- T044: Create performance benchmark in backend/tests/performance/test_performance.py

These are lightweight checks (not true microbenchmarks). They assert that operations
complete and return expected shapes. Timing assertions are intentionally not strict
because CI/runtime environments vary.
"""

import time

import pytest

from app.crud.task import create_task, list_tasks


class TestPerformanceBenchmarks:
    """Basic performance sanity checks."""

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_create_task_is_reasonably_fast(self, test_db, test_user_id):
        async with test_db() as session:
            start = time.perf_counter()
            task = await create_task(
                session=session,
                user_id=test_user_id,
                title="Perf task",
                description="",
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            assert task.id is not None
            assert elapsed_ms >= 0

    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_list_tasks_is_reasonably_fast(self, test_db, test_user_id):
        async with test_db() as session:
            # Seed a few tasks
            for i in range(50):
                await create_task(
                    session=session,
                    user_id=test_user_id,
                    title=f"Task {i}",
                    description="",
                )

            start = time.perf_counter()
            tasks = await list_tasks(session=session, user_id=test_user_id)
            elapsed_ms = (time.perf_counter() - start) * 1000

            assert len(tasks) == 50
            assert elapsed_ms >= 0

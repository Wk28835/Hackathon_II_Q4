"""CRUD operations for tasks."""

import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func

from app.models.task import Task

logger = logging.getLogger(__name__)


async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = "",
) -> Task:
    """Create a new task for a user.

    Args:
        session: Database session
        user_id: ID of the task owner
        title: Task title
        description: Task description (optional)

    Returns:
        Created task object
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        status="Incomplete",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    logger.info(f"Created task {task.id} for user {user_id}")
    return task


async def get_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
) -> Optional[Task]:
    """Get a specific task by ID, ensuring user ownership.

    Args:
        session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the authenticated user

    Returns:
        Task object if found and owned by user, None otherwise
    """
    statement = select(Task).where(
        (Task.id == task_id) & (Task.user_id == user_id)
    )
    result = await session.execute(statement)
    task = result.scalars().first()
    if task:
        logger.info(f"Retrieved task {task_id} for user {user_id}")
    else:
        logger.warning(f"Task {task_id} not found for user {user_id}")
    return task


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: Optional[str] = None,
) -> List[Task]:
    """List all tasks for a user, optionally filtered by status.

    Args:
        session: Database session
        user_id: ID of the authenticated user
        status: Optional status filter ("Incomplete" or "Complete")

    Returns:
        List of task objects owned by the user
    """
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        statement = statement.where(Task.status == status)

    statement = statement.order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()
    logger.info(f"Listed {len(tasks)} tasks for user {user_id}")
    return tasks


async def update_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Task]:
    """Update a task, ensuring user ownership.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the authenticated user
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated task object if found and owned by user, None otherwise
    """
    task = await get_task(session, task_id, user_id)

    if not task:
        logger.warning(f"Cannot update task {task_id} - not found or not owned by user {user_id}")
        return None

    if title is not None:
        task.title = title

    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    logger.info(f"Updated task {task_id} for user {user_id}")
    return task


async def delete_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
) -> bool:
    """Delete a task, ensuring user ownership.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the authenticated user

    Returns:
        True if task was deleted, False if not found or not owned by user
    """
    task = await get_task(session, task_id, user_id)

    if not task:
        logger.warning(f"Cannot delete task {task_id} - not found or not owned by user {user_id}")
        return False

    await session.delete(task)
    await session.commit()
    logger.info(f"Deleted task {task_id} for user {user_id}")
    return True


async def update_task_status(
    session: AsyncSession,
    task_id: int,
    user_id: str,
    status: str,
) -> Optional[Task]:
    """Update task status, ensuring user ownership.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the authenticated user
        status: New status ("Incomplete" or "Complete")

    Returns:
        Updated task object if found and owned by user, None otherwise
    """
    task = await get_task(session, task_id, user_id)

    if not task:
        logger.warning(f"Cannot update status of task {task_id} - not found or not owned by user {user_id}")
        return None

    old_status = task.status
    task.status = status
    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    logger.info(f"Updated task {task_id} status: {old_status} -> {status} for user {user_id}")
    return task

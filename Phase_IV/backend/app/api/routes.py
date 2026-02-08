"""API routes for Task CRUD API."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.crud.task import (create_task, delete_task, get_task, list_tasks,
                           update_task, update_task_status)
from app.database import get_session
from app.schemas.task import (ErrorResponse, TaskCreate, TaskResponse,
                              TaskStatusUpdate, TaskUpdate)

logger = logging.getLogger(__name__)

# Create router for task endpoints
router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Health router (tasks.md T055 expects /health in this file)
health_router = APIRouter(tags=["health"])


@health_router.get(
    "/health",
    summary="Health check",
    description="Health check endpoint for monitoring.",
)
async def health_check() -> dict:
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}


# Phase 3: User Story 1 - Create Task (P1)
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    summary="Create a new task",
    description="Create a new task with title and optional description. The task is automatically assigned to the authenticated user.",
)
async def create_task_endpoint(
    task_create: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Create a new task for the authenticated user.

    Args:
        task_create: Task creation request (title, description)
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        Created task object

    Raises:
        400: If validation fails (empty title, too long)
        401: If authentication fails
    """
    try:
        task = await create_task(
            session=session,
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
        )
        logger.info(f"Task {task.id} created successfully for user {user_id}")
        return TaskResponse.model_validate(task)
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


# Phase 4: User Story 2 - List Tasks (P1)
@router.get(
    "",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
    summary="List all tasks for the authenticated user",
    description="Retrieve all tasks owned by the authenticated user. Optionally filter by status.",
)
async def list_tasks_endpoint(
    status_filter: Optional[str] = Query(
        None,
        alias="status",
        description="Filter by status: Incomplete or Complete",
    ),
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> List[TaskResponse]:
    """List all tasks for the authenticated user.

    Args:
        status_filter: Optional status filter
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        List of task objects

    Raises:
        401: If authentication fails
    """
    try:
        tasks = await list_tasks(
            session=session,
            user_id=user_id,
            status=status_filter,
        )
        logger.info(f"Listed {len(tasks)} tasks for user {user_id}")
        return [TaskResponse.model_validate(task) for task in tasks]
    except Exception as e:
        logger.error(f"Error listing tasks for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks",
        )


# Phase 5: User Story 3 - Get Task by ID (P1)
@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {
            "model": ErrorResponse,
            "description": "Forbidden - task belongs to another user",
        },
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
    summary="Get a specific task by ID",
    description="Retrieve a specific task. Users can only access their own tasks.",
)
async def get_task_endpoint(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        Task object

    Raises:
        401: If authentication fails
        403: If task belongs to another user
        404: If task not found
    """
    try:
        task = await get_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
        )

        if not task:
            # Check if task exists but belongs to another user
            logger.warning(f"Task {task_id} access denied for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        logger.info(f"Retrieved task {task_id} for user {user_id}")
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task {task_id} for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task",
        )


# Phase 6: User Story 4 - Update Task (P1)
@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {
            "model": ErrorResponse,
            "description": "Forbidden - task belongs to another user",
        },
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
    summary="Update a task",
    description="Update a task's title and/or description. Users can only update their own tasks.",
)
async def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Update a task.

    Args:
        task_id: ID of the task to update
        task_update: Task update request (title, description)
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        Updated task object

    Raises:
        400: If validation fails
        401: If authentication fails
        403: If task belongs to another user
        404: If task not found
    """
    try:
        task = await update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            title=task_update.title,
            description=task_update.description,
        )

        if not task:
            logger.warning(f"Task {task_id} update denied for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        logger.info(f"Updated task {task_id} for user {user_id}")
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


# Phase 7: User Story 5 - Delete Task (P1)
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {
            "model": ErrorResponse,
            "description": "Forbidden - task belongs to another user",
        },
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
    summary="Delete a task",
    description="Permanently delete a task. Users can only delete their own tasks.",
)
async def delete_task_endpoint(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a task.

    Args:
        task_id: ID of the task to delete
        user_id: Authenticated user ID from JWT token
        session: Database session

    Raises:
        401: If authentication fails
        403: If task belongs to another user
        404: If task not found
    """
    try:
        deleted = await delete_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
        )

        if not deleted:
            logger.warning(f"Task {task_id} deletion denied for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        logger.info(f"Deleted task {task_id} for user {user_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task {task_id} for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )


# Phase 8: User Story 6 - Mark Task Status (P2)
@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid status value"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {
            "model": ErrorResponse,
            "description": "Forbidden - task belongs to another user",
        },
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
    summary="Update task status",
    description="Mark a task as complete or incomplete. Users can only update their own tasks.",
)
async def update_task_status_endpoint(
    task_id: int,
    status_update: TaskStatusUpdate,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Update task status.

    Args:
        task_id: ID of the task
        status_update: Status update request (Incomplete or Complete)
        user_id: Authenticated user ID from JWT token
        session: Database session

    Returns:
        Updated task object

    Raises:
        400: If invalid status value
        401: If authentication fails
        403: If task belongs to another user
        404: If task not found
    """
    # Validate status value
    if status_update.status not in ["Incomplete", "Complete"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status value. Must be 'Incomplete' or 'Complete'",
        )

    try:
        task = await update_task_status(
            session=session,
            task_id=task_id,
            user_id=user_id,
            status=status_update.status,
        )

        if not task:
            logger.warning(f"Task {task_id} status update denied for user {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        logger.info(
            f"Updated task {task_id} status to {status_update.status} for user {user_id}"
        )
        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task {task_id} status for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task status",
        )

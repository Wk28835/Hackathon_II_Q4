"""Update handler module for updating tasks."""

from typing import List
from uuid import UUID

try:
    from .task import Task
except ImportError:
    from task import Task


def is_valid_uuid(val: str) -> bool:
    """
    Check if a string is a valid UUID.

    Args:
        val: String to check

    Returns:
        True if valid UUID, False otherwise
    """
    try:
        UUID(val)
        return True
    except ValueError:
        return False


def find_task_by_id(tasks: List[Task], task_id: str) -> Task | None:
    """
    Find a task by its ID.

    Args:
        tasks: List of tasks to search
        task_id: UUID string of the task to find

    Returns:
        Task if found, None otherwise
    """
    for task in tasks:
        if task.id == task_id:
            return task
    return None


def update_task(task: Task, new_title: str | None, new_description: str | None) -> None:
    """
    Update a task's title and/or description.

    Args:
        task: Task to update
        new_title: New title (None means don't change)
        new_description: New description (None means don't change)
    """
    if new_title is not None:
        task.title = new_title
    if new_description is not None:
        task.description = new_description


def format_update_success(task: Task) -> str:
    """
    Format a success message for task update.

    Args:
        task: Updated task

    Returns:
        Formatted success message
    """
    return f"Task updated successfully.\nID: {task.id}\nTitle: {task.title}\nDescription: {task.description}"

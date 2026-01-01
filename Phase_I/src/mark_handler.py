"""Mark handler module for marking task status."""

from typing import List

try:
    from .task import Task
    from .update_handler import is_valid_uuid, find_task_by_id
except ImportError:
    from task import Task
    from update_handler import is_valid_uuid, find_task_by_id


def mark_task(task: Task, new_status: str) -> None:
    """
    Update a task's status.

    Args:
        task: Task to update
        new_status: New status ("Complete" or "Incomplete")
    """
    task.status = new_status


def format_mark_success(task: Task, old_status: str) -> str:
    """
    Format a success message for task status update.

    Args:
        task: Updated task
        old_status: Previous status of the task

    Returns:
        Formatted success message
    """
    return f"Task status updated successfully.\nID: {task.id}\nTitle: {task.title}\nStatus: {old_status} -> {task.status}"

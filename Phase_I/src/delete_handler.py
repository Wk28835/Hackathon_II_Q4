"""Delete handler module for deleting tasks."""

from typing import List

try:
    from .task import Task
    from .update_handler import is_valid_uuid, find_task_by_id
except ImportError:
    from task import Task
    from update_handler import is_valid_uuid, find_task_by_id


def delete_task(tasks: List[Task], task: Task) -> None:
    """
    Delete a task from the list.

    Args:
        tasks: List of tasks
        task: Task to delete
    """
    tasks.remove(task)


def format_delete_success(task: Task) -> str:
    """
    Format a success message for task deletion.

    Args:
        task: Deleted task

    Returns:
        Formatted success message
    """
    return f"Task deleted successfully.\nID: {task.id}\nTitle: {task.title}"

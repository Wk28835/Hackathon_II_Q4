"""CLI interface for the Task application."""

import argparse
from typing import NamedTuple


class AddTaskArgs(NamedTuple):
    """Arguments for the add command."""

    title: str
    description: str


class ListTaskArgs(NamedTuple):
    """Arguments for the list command."""

    status: str  # "all", "incomplete", "complete"


class UpdateTaskArgs(NamedTuple):
    """Arguments for the update command."""

    task_id: str
    title: str | None
    description: str | None


class DeleteTaskArgs(NamedTuple):
    """Arguments for the delete command."""

    task_id: str


class MarkTaskArgs(NamedTuple):
    """Arguments for the mark command."""

    task_id: str
    status: str  # "complete" or "incomplete"


def parse_add_args(args: list[str] | None = None) -> AddTaskArgs:
    """
    Parse arguments for the add command.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        AddTaskArgs with title and description
    """
    parser = argparse.ArgumentParser(description="Add a new task to the todo list")
    parser.add_argument("title", help="Title of the task")
    parser.add_argument(
        "--description", "-d", default="", help="Optional description of the task"
    )

    parsed = parser.parse_args(args)
    return AddTaskArgs(title=parsed.title, description=parsed.description)


def parse_list_args(args: list[str] | None = None) -> ListTaskArgs:
    """
    Parse arguments for the list command.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        ListTaskArgs with status filter
    """
    parser = argparse.ArgumentParser(description="List tasks")
    parser.add_argument(
        "--status",
        "-s",
        default="all",
        choices=["all", "incomplete", "complete"],
        help="Filter tasks by status (default: all)",
    )

    parsed = parser.parse_args(args)
    return ListTaskArgs(status=parsed.status)


def parse_update_args(args: list[str] | None = None) -> UpdateTaskArgs:
    """
    Parse arguments for the update command.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        UpdateTaskArgs with task_id, title, and description
    """
    parser = argparse.ArgumentParser(description="Update an existing task")
    parser.add_argument("task_id", help="ID of the task to update")
    parser.add_argument(
        "--title", help="New title for the task (leave unchanged if not specified)"
    )
    parser.add_argument(
        "--description", "-d", help="New description for the task"
    )

    parsed = parser.parse_args(args)
    return UpdateTaskArgs(
        task_id=parsed.task_id,
        title=parsed.title,
        description=parsed.description,
    )


def parse_delete_args(args: list[str] | None = None) -> DeleteTaskArgs:
    """
    Parse arguments for the delete command.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        DeleteTaskArgs with task_id
    """
    parser = argparse.ArgumentParser(description="Delete an existing task")
    parser.add_argument("task_id", help="ID of the task to delete")

    parsed = parser.parse_args(args)
    return DeleteTaskArgs(task_id=parsed.task_id)


def parse_mark_args(args: list[str] | None = None) -> MarkTaskArgs:
    """
    Parse arguments for the mark command.

    Args:
        args: Command line arguments (defaults to sys.argv)

    Returns:
        MarkTaskArgs with task_id and status
    """
    parser = argparse.ArgumentParser(description="Mark task status")
    parser.add_argument("task_id", help="ID of the task to mark")

    status_group = parser.add_mutually_exclusive_group(required=True)
    status_group.add_argument(
        "--complete", action="store_const", const="Complete", dest="status", help="Mark task as complete"
    )
    status_group.add_argument(
        "--incomplete", action="store_const", const="Incomplete", dest="status", help="Mark task as incomplete"
    )

    parsed = parser.parse_args(args)
    return MarkTaskArgs(task_id=parsed.task_id, status=parsed.status)


def create_parser() -> argparse.ArgumentParser:
    """
    Create the main argument parser.

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Task management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")
    add_parser.add_argument(
        "--description", "-d", default="", help="Optional description of the task"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status",
        "-s",
        default="all",
        choices=["all", "incomplete", "complete"],
        help="Filter tasks by status (default: all)",
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("task_id", help="ID of the task to update")
    update_parser.add_argument(
        "--title", help="New title for the task"
    )
    update_parser.add_argument(
        "--description", "-d", help="New description for the task"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an existing task")
    delete_parser.add_argument("task_id", help="ID of the task to delete")

    # Mark command
    mark_parser = subparsers.add_parser("mark", help="Mark task status")
    mark_parser.add_argument("task_id", help="ID of the task to mark")
    status_group = mark_parser.add_mutually_exclusive_group(required=True)
    status_group.add_argument(
        "--complete", action="store_const", const="Complete", dest="status", help="Mark task as complete"
    )
    status_group.add_argument(
        "--incomplete", action="store_const", const="Incomplete", dest="status", help="Mark task as incomplete"
    )

    return parser

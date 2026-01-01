#!/usr/bin/env python3
"""Main entry point for the Task CLI application."""

import sys

try:
    from .cli import create_parser
    from .storage import TaskList
    from .validation import validate_title
    from .list_handler import format_task_table
    from .update_handler import (
        is_valid_uuid,
        find_task_by_id,
        update_task,
        format_update_success,
    )
    from .delete_handler import (
        delete_task,
        format_delete_success,
    )
    from .mark_handler import (
        mark_task,
        format_mark_success,
    )
except ImportError:
    from cli import create_parser
    from storage import TaskList
    from validation import validate_title
    from list_handler import format_task_table
    from update_handler import (
        is_valid_uuid,
        find_task_by_id,
        update_task,
        format_update_success,
    )
    from delete_handler import (
        delete_task,
        format_delete_success,
    )
    from mark_handler import (
        mark_task,
        format_mark_success,
    )

def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "add":
        return handle_add(args)
    elif args.command == "list":
        return handle_list(args)
    elif args.command == "update":
        return handle_update(args)
    elif args.command == "delete":
        return handle_delete(args)
    elif args.command == "mark":
        return handle_mark(args)

    elif args.command is None:
        parser.print_help()
        return 0
    else:
        parser.print_help()
        return 0


def handle_add(args) -> int:
    """
    Handle the add command.

    Args:
        args: Parsed command arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate title
    is_valid, error_msg = validate_title(args.title)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        return 1

    # Create task
    storage = TaskList()
    task = storage.add_task(args.title, args.description)

    # Display success message
    print(f"Task '{task.title}' added successfully with ID {task.id}.")
    return 0

def handle_list(args) -> int:
    """
    Handle the list command.

    Args:
        args: Parsed command arguments with status filter

    Returns:
        Exit code (0 for success, 1 for error)
    """
    storage = TaskList()

    # Filter tasks by status
    filtered_tasks = storage.filter_by_status(args.status)

    # Display tasks or empty message
    if filtered_tasks:
        output = format_task_table(filtered_tasks)
        print(output)
    else:
        # No tasks match the filter
        if args.status.lower() == "all":
            print("No tasks found. Add a task to get started.")
        else:
            print(f"No tasks found matching filter '{args.status}'.")

    return 0


def handle_update(args) -> int:
    """
    Handle the update command.

    Args:
        args: Parsed command arguments with task_id, title, and description

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate UUID format
    if not is_valid_uuid(args.task_id):
        print("Error: Invalid task ID format. Please provide a valid UUID.", file=sys.stderr)
        return 1

    # Initialize storage and find task
    storage = TaskList()
    task = find_task_by_id(storage.tasks, args.task_id)

    if task is None:
        print("Error: Task not found.", file=sys.stderr)
        return 1

    # Validate title if provided
    if args.title is not None:
        is_valid, error_msg = validate_title(args.title)
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            return 1

    # Update the task
    update_task(task, args.title, args.description)
    storage._save()  # Persist changes

    # Display success message
    print(format_update_success(task))
    return 0


def handle_delete(args) -> int:
    """
    Handle the delete command.

    Args:
        args: Parsed command arguments with task_id

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate UUID format
    if not is_valid_uuid(args.task_id):
        print("Error: Invalid task ID format. Please provide a valid UUID.", file=sys.stderr)
        return 1

    # Initialize storage and find task
    storage = TaskList()
    task = find_task_by_id(storage.tasks, args.task_id)

    if task is None:
        print("Error: Task not found.", file=sys.stderr)
        return 1

    # Delete the task
    delete_task(storage.tasks, task)
    storage._save()  # Persist changes

    # Display success message
    print(format_delete_success(task))
    return 0


def handle_mark(args) -> int:
    """
    Handle the mark command.

    Args:
        args: Parsed command arguments with task_id and status

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate UUID format
    if not is_valid_uuid(args.task_id):
        print("Error: Invalid task ID format. Please provide a valid UUID.", file=sys.stderr)
        return 1

    # Initialize storage and find task
    storage = TaskList()
    task = find_task_by_id(storage.tasks, args.task_id)

    if task is None:
        print("Error: Task not found.", file=sys.stderr)
        return 1

    # Store old status for confirmation message
    old_status = task.status

    # Update the task status
    mark_task(task, args.status)
    storage._save()  # Persist changes

    # Display success message
    print(format_mark_success(task, old_status))
    return 0


if __name__ == "__main__":
    sys.exit(main())

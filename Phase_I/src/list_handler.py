"""List handler module for displaying tasks in tabular format."""

from typing import List

# Column widths for table display
COLUMN_WIDTHS = {
    "id": 36,
    "title": 20,
    "description": 25,
    "status": 12,
}


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to max_length with ellipsis.

    Args:
        text: The text to truncate
        max_length: Maximum length allowed

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length] + "..."


def format_task_table(tasks: List) -> str:
    """
    Format a list of tasks into a table string.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted table string
    """
    if not tasks:
        return format_empty_message()

    # Try to use tabulate if available
    try:
        from tabulate import tabulate

        headers = ["ID", "Title", "Description", "Status"]
        rows = [
            [
                t.id,
                truncate_text(t.title, COLUMN_WIDTHS["title"]),
                truncate_text(t.description, COLUMN_WIDTHS["description"]),
                t.status,
            ]
            for t in tasks
        ]
        return tabulate(rows, headers=headers, tablefmt="simple")
    except ImportError:
        # Fallback to custom formatting
        return _format_table_custom(tasks)


def _format_table_custom(tasks: List) -> str:
    """
    Custom table formatting without tabulate dependency.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted table string
    """
    # Build header
    header = f"{'ID':<{COLUMN_WIDTHS['id']}} {'Title':<{COLUMN_WIDTHS['title']}} {'Description':<{COLUMN_WIDTHS['description']}} {'Status':<{COLUMN_WIDTHS['status']}}"
    separator = "-" * COLUMN_WIDTHS["id"] + " " + "-" * COLUMN_WIDTHS["title"] + " " + "-" * COLUMN_WIDTHS["description"] + " " + "-" * COLUMN_WIDTHS["status"]

    # Build rows
    rows = []
    for t in tasks:
        row = (
            f"{t.id:<{COLUMN_WIDTHS['id']}} "
            f"{truncate_text(t.title, COLUMN_WIDTHS['title']):<{COLUMN_WIDTHS['title']}} "
            f"{truncate_text(t.description, COLUMN_WIDTHS['description']):<{COLUMN_WIDTHS['description']}} "
            f"{t.status:<{COLUMN_WIDTHS['status']}}"
        )
        rows.append(row)

    return "\n".join([header, separator] + rows)


def format_empty_message() -> str:
    """
    Return the empty state message.

    Returns:
        Empty state message string
    """
    return "No tasks found. Add a task to get started."


def format_filter_empty_message(filter_value: str) -> str:
    """
    Return the empty state message for filtered results.

    Args:
        filter_value: The filter value that returned no results

    Returns:
        Filter-specific empty state message
    """
    return f"No tasks found matching filter '{filter_value}'."

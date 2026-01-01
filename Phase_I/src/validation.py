"""Validation utilities for task input."""

from typing import Tuple


def validate_title(title: str | None) -> Tuple[bool, str | None]:
    """
    Validate that a task title is not empty or whitespace-only.

    Args:
        title: The title string to validate (can be None)

    Returns:
        Tuple of (is_valid: bool, error_message: str | None)
        - If valid: (True, None)
        - If invalid: (False, "Title must not be empty.")
    """
    if title is None or not title or not title.strip():
        return False, "Title must not be empty."
    return True, None

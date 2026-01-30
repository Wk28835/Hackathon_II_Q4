"""Task model for Task CRUD API."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a user.

    Attributes:
        id: Unique task identifier (auto-generated)
        user_id: Foreign key to user (owner of the task)
        title: Task title (required, non-empty)
        description: Task description (optional)
        status: Task status ("Incomplete" or "Complete")
        created_at: Timestamp when task was created (auto-set)
        updated_at: Timestamp when task was last modified (auto-set)
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=64)  # String to support Better Auth IDs
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    status: str = Field(default="Incomplete")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel config."""

        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 42,
                "title": "Complete project report",
                "description": "Summarize Q4 findings and submit to management",
                "status": "Incomplete",
                "created_at": "2026-01-10T14:30:00Z",
                "updated_at": "2026-01-10T14:30:00Z",
            }
        }

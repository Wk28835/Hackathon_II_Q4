"""Pydantic schemas for Task CRUD API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(
        default="",
        max_length=2000,
        description="Task description (optional)",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="New task title (optional)",
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="New task description (optional)",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "title": "Buy organic groceries",
                "description": "Organic milk, free-range eggs, whole grain bread",
            }
        }


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status."""

    status: str = Field(
        ...,
        description="New task status",
        pattern="^(Incomplete|Complete)$",
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {"example": {"status": "Complete"}}


class TaskResponse(BaseModel):
    """Schema for returning a task to the client."""

    id: int = Field(description="Unique task identifier")
    user_id: str = Field(description="User ID of the task owner")
    title: str = Field(description="Task title")
    description: str = Field(description="Task description")
    status: str = Field(description="Task status (Incomplete or Complete)")
    created_at: datetime = Field(description="When task was created")
    updated_at: datetime = Field(description="When task was last updated")

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "abc123xyz",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "status": "Incomplete",
                "created_at": "2026-01-10T14:30:00Z",
                "updated_at": "2026-01-10T14:30:00Z",
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(description="Error message")

    class Config:
        """Pydantic config."""

        json_schema_extra = {"example": {"detail": "Task not found"}}

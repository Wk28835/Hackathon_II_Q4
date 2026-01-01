"""Task entity module."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Task:
    """Represents a single todo task."""

    title: str
    description: str = ""
    status: str = "Incomplete"
    id: str = field(default_factory=lambda: str(uuid4()))

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return f"Task(id={self.id!r}, title={self.title!r}, description={self.description!r}, status={self.status!r})"

    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }

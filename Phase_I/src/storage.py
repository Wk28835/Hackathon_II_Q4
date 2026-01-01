"""In-memory task storage module with file persistence."""

import json
import os
from typing import List

try:
    from .task import Task
except ImportError:
    from task import Task

DATA_FILE = "tasks.json"


class TaskList:
    """In-memory container for storing tasks with file persistence."""

    def __init__(self, data_file: str = DATA_FILE) -> None:
        """Initialize an empty task list and load from file if exists."""
        self.data_file = data_file
        self.tasks: List[Task] = []
        self._load()

    def _load(self) -> None:
        """Load tasks from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task(**task) for task in data]
            except (json.JSONDecodeError, KeyError):
                self.tasks = []

    def _save(self) -> None:
        """Save tasks to JSON file."""
        with open(self.data_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def add_task(self, title: str, description: str = "", status: str = "Incomplete") -> Task:
        """
        Create and add a new task to the list.

        Args:
            title: The task title (required)
            description: Optional task description
            status: Task status (default: Incomplete)

        Returns:
            The newly created Task instance
        """
        task = Task(title=title, description=description, status=status)
        self.tasks.append(task)
        self._save()
        return task

    def filter_by_status(self, status: str) -> List[Task]:
        """
        Filter tasks by status.

        Args:
            status: Status to filter by ("all", "incomplete", "complete")

        Returns:
            List of tasks matching the status
        """
        if status.lower() == "all":
            return self.tasks
        return [t for t in self.tasks if t.status.lower() == status.lower()]

    def __len__(self) -> int:
        """Return the number of tasks in the list."""
        return len(self.tasks)

    def __iter__(self):
        """Iterate over tasks."""
        return iter(self.tasks)

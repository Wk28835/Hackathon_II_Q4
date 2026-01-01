# CLAUDE.md

This document provides guidance for working with this codebase.

## Project Overview

This is a CLI-based Todo List application built with Python. The project uses the `.specify` framework for feature specification, planning, and implementation workflows.

## Tech Stack

- **Language**: Python 3.12+
- **Testing**: pytest
- **Architecture**: CLI application with in-memory storage
- **Framework**: `.specify` (custom speclet framework)

## Key Commands

```bash
# Run the CLI
python src/main.py add "Task title" --description "Details"
python src/main.py list
python src/main.py list --status incomplete
python src/main.py list -s complete
python src/main.py update <task-id> --title "New title" --description "New desc"
python src/main.py delete <task-id>
python src/main.py mark <task-id> --complete
python src/main.py mark <task-id> --incomplete

# Run tests
pytest tests/ -v
```

## Project Structure

```
test/
├── src/
│   ├── __init__.py       # Package marker
│   ├── cli.py            # Argument parsing
│   ├── main.py           # Entry point
│   ├── storage.py        # TaskList storage class
│   ├── task.py           # Task dataclass
│   ├── validation.py     # Input validation
│   ├── list_handler.py   # List formatting
│   ├── update_handler.py # Update task logic
│   ├── delete_handler.py # Delete task logic
│   └── mark_handler.py   # Mark status logic
├── tests/
│   ├── __init__.py       # Test package
│   └── test_add_task.py  # Unit tests
├── specs/
│   ├── 001-add-task/         # Add Task feature specs
│   ├── 001-view-tasks/       # View Tasks feature specs
│   ├── 001-update-task/      # Update Task feature specs
│   ├── 002-delete-task/      # Delete Task feature specs
│   └── 003-mark-task-status/ # Mark Task Status feature specs
├── CLAUDE.md             # This file
└── README.md             # Project documentation
```

## Key Entities

### Task
- `id`: UUID4 string (auto-generated)
- `title`: string (required, non-empty)
- `description`: string (optional, defaults to "")
- `status`: string ("Incomplete" or "Complete")

### TaskList
- In-memory list storage with JSON persistence
- `add_task(title, description, status)` - Create and store task
- `filter_by_status(status)` - Filter tasks by status
- `_save()` - Persist tasks to tasks.json

## Implemented Features

### 1. Add Task (001-add-task)
- Add tasks with title and optional description
- Auto-generated UUID4 for each task
- Default status: "Incomplete"
- Validation: Title must not be empty

### 2. View Tasks (001-view-tasks)
- List all tasks in formatted table
- Filter by status: all, incomplete, complete
- Truncates long text for display
- Shows empty message when no tasks found

### 3. Update Task (001-update-task)
- Update task title and/or description by ID
- UUID validation
- Task existence verification
- Persists changes to storage

### 4. Delete Task (002-delete-task)
- Permanently remove tasks by ID
- UUID validation
- Task existence verification
- Confirmation message with deleted task details

### 5. Mark Task Status (003-mark-task-status)
- Mark tasks as complete or incomplete by ID
- Mutually exclusive --complete/--incomplete flags
- Shows old status -> new status transition
- UUID validation and task existence verification

## Development Workflow

This project uses the `.specify` framework:

1. **Specify**: `/speckit.specify <feature-description>` - Create feature spec
2. **Plan**: `/speckit.plan specs/<feature-dir>` - Generate implementation plan
3. **Tasks**: `/speckit.tasks specs/<feature-dir>` - Generate task breakdown
4. **Implement**: `/speckit.implement specs/<feature-dir>` - Execute implementation

## Speckit Commands

- `/speckit.specify` - Generate feature specification from description
- `/speckit.plan` - Create implementation plan from spec
- `/speckit.tasks` - Generate task breakdown from plan
- `/speckit.implement` - Execute implementation tasks
- `/speckit.checklist` - Validate specification quality

## Dependencies

- Python standard library (no external dependencies for core)
- pytest (for testing)
- tabulate (optional, for enhanced table formatting)

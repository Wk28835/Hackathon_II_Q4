# Todo CLI Application

A simple command-line todo list application built with Python.

## Features

- **Add Tasks**: Create tasks with title and optional description
- **View Tasks**: Display all tasks in a formatted table
- **Filter Tasks**: Filter by status (all, incomplete, complete)
- **Update Tasks**: Modify task title and/or description
- **Delete Tasks**: Remove tasks permanently
- **Mark Status**: Toggle tasks between complete and incomplete
- **Status Management**: Tasks default to "Incomplete"

## Quick Start

```bash
# Add a task
python src/main.py add "Buy groceries" --description "Milk, Eggs, Bread"

# Add a task with just a title
python src/main.py add "Call mom"

# List all tasks
python src/main.py list

# List only incomplete tasks
python src/main.py list --status incomplete

# List only complete tasks
python src/main.py list -s complete

# Update a task
python src/main.py update <task-id> --title "New title"
python src/main.py update <task-id> --description "New description"

# Delete a task
python src/main.py delete <task-id>

# Mark task as complete
python src/main.py mark <task-id> --complete

# Mark task as incomplete
python src/main.py mark <task-id> --incomplete
```

## Installation

```bash
# Install pytest for testing
pip install pytest

# Run tests
pytest tests/ -v
```

## Project Structure

```
test/
├── src/
│   ├── cli.py            # Command-line interface
│   ├── main.py           # Application entry point
│   ├── storage.py        # In-memory task storage
│   ├── task.py           # Task data model
│   ├── validation.py     # Input validation
│   ├── list_handler.py   # List formatting
│   ├── update_handler.py # Update task logic
│   ├── delete_handler.py # Delete task logic
│   └── mark_handler.py   # Mark status logic
├── tests/
│   └── test_add_task.py  # Unit tests
└── specs/
    ├── 001-add-task/         # Add Task feature
    ├── 001-view-tasks/       # View Tasks feature
    ├── 001-update-task/      # Update Task feature
    ├── 002-delete-task/      # Delete Task feature
    └── 003-mark-task-status/ # Mark Task Status feature
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `add "TITLE" [--description "DESC"]` | Add a new task |
| `list [--status all\|incomplete\|complete]` | List tasks with optional status filter |
| `update <ID> [--title "TITLE"] [--description "DESC"]` | Update task title and/or description |
| `delete <ID>` | Delete a task permanently |
| `mark <ID> --complete` | Mark task as complete |
| `mark <ID> --incomplete` | Mark task as incomplete |

## Examples

```bash
# Add and view tasks
$ python src/main.py add "Buy groceries" --description "Milk, Eggs, Bread"
Task 'Buy groceries' added successfully with ID 550e8400-e29b-41d4-a716-446655440000.

$ python src/main.py add "Call mom"
Task 'Call mom' added successfully with ID 6ba7b810-9dad-11d1-80b4-00c04fd430c8.

$ python src/main.py list
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread         Incomplete
6ba7b810-9dad-11d1-80b4-00c04fd430c8 Call mom                                     Incomplete

# Update a task
$ python src/main.py update 550e8400-e29b-41d4-a716-446655440000 --title "Buy organic groceries"
Task updated successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy organic groceries
Description: Milk, Eggs, Bread

# Mark task as complete
$ python src/main.py mark 550e8400-e29b-41d4-a716-446655440000 --complete
Task status updated successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy organic groceries
Status: Incomplete -> Complete

# List only complete tasks
$ python src/main.py list -s complete
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy organic grocerie... Milk, Eggs, Bread         Complete

# Delete a task
$ python src/main.py delete 6ba7b810-9dad-11d1-80b4-00c04fd430c8
Task deleted successfully.
ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
Title: Call mom
```

## Testing

Run all tests with:

```bash
pytest tests/ -v
```

## Development

This project uses the `.specify` framework for feature-driven development:

1. Create feature spec: `/speckit.specify "Feature description"`
2. Plan implementation: `/speckit.plan specs/<feature>`
3. Generate tasks: `/speckit.tasks specs/<feature>`
4. Implement: `/speckit.implement specs/<feature>`

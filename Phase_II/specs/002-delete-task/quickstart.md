# Quickstart: Delete Task Feature

## Installation

```bash
# Already have the todo app installed
cd src

# Verify installation
python main.py --help
```

## Usage

### Delete a Task

```bash
python main.py delete <task-id>
```

**Example**:
```bash
$ python main.py delete 550e8400-e29b-41d4-a716-446655440000
Task deleted successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy groceries
```

## Find Task ID

Use the list command to see task IDs:

```bash
python main.py list
```

**Output**:
```
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread         Incomplete
```

## Error Handling

### Invalid Task ID

```bash
$ python main.py delete invalid-id
Error: Invalid task ID format. Please provide a valid UUID.
```

### Task Not Found

```bash
$ python main.py delete 00000000-0000-0000-0000-000000000000
Error: Task not found.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py delete <id>` | Delete a task by ID |

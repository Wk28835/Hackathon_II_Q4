# Quickstart: Update Task Feature

## Installation

```bash
# Already have the todo app installed
cd src

# Verify installation
python main.py --help
```

## Usage

### Update Task Title Only

```bash
python main.py update <task-id> --title "New task title"
```

**Example**:
```bash
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --title "Buy organic groceries"
Task updated successfully.
```

### Update Task Description Only

```bash
python main.py update <task-id> --description "New description"
# or
python main.py update <task-id> -d "New description"
```

**Example**:
```bash
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --description "Milk, Eggs, Bread, Cheese"
Task updated successfully.
```

### Update Both Title and Description

```bash
python main.py update <task-id> --title "New title" --description "New description"
```

**Example**:
```bash
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --title "Buy groceries" --description "All dairy items"
Task updated successfully.
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
$ python main.py update invalid-id --title "New title"
Error: Invalid task ID format. Please provide a valid UUID.
```

### Task Not Found

```bash
$ python main.py update 00000000-0000-0000-0000-000000000000 --title "New title"
Error: Task not found.
```

### Empty Title

```bash
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --title ""
Error: Title must not be empty.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py update <id> --title "TITLE"` | Update task title |
| `python main.py update <id> -d "DESC"` | Update task description |
| `python main.py update <id> --title "T" --description "D"` | Update both |

## Examples

### Full Workflow

```bash
# List tasks to get ID
$ python main.py list
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk                      Incomplete

# Update title
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --title "Buy organic groceries"
Task updated successfully.

# Update description
$ python main.py update 550e8400-e29b-41d4-a716-446655440000 --description "Milk, Eggs, Bread, Cheese"
Task updated successfully.

# Verify changes
$ python main.py list
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy organic groceries Milk, Eggs, Bread, Cheese Incomplete
```

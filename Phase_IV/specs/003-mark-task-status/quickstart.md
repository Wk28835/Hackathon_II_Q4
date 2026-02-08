# Quickstart: Mark Task Status Feature

## Installation

```bash
# Already have the todo app installed
cd src

# Verify installation
python main.py --help
```

## Usage

### Mark a Task as Complete

```bash
python main.py mark <task-id> --complete
```

**Example**:
```bash
$ python main.py mark 550e8400-e29b-41d4-a716-446655440000 --complete
Task status updated successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy groceries
Status: Incomplete -> Complete
```

### Mark a Task as Incomplete

```bash
python main.py mark <task-id> --incomplete
```

**Example**:
```bash
$ python main.py mark 550e8400-e29b-41d4-a716-446655440000 --incomplete
Task status updated successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy groceries
Status: Complete -> Incomplete
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
$ python main.py mark invalid-id --complete
Error: Invalid task ID format. Please provide a valid UUID.
```

### Task Not Found

```bash
$ python main.py mark 00000000-0000-0000-0000-000000000000 --complete
Error: Task not found.
```

### Both Flags Provided

```bash
$ python main.py mark 550e8400-e29b-41d4-a716-446655440000 --complete --incomplete
Error: Cannot use both --complete and --incomplete. Please specify only one.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py mark <id> --complete` | Mark task as complete |
| `python main.py mark <id> --incomplete` | Mark task as incomplete |

## Examples

### Full Workflow

```bash
# List tasks to get ID
$ python main.py list
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk                      Incomplete

# Mark as complete
$ python main.py mark 550e8400-e29b-41d4-a716-446655440000 --complete
Task status updated successfully.
ID: 550e8400-e29b-41d4-a716-446655440000
Title: Buy groceries
Status: Incomplete -> Complete

# Verify change
$ python main.py list
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk                      Complete
```

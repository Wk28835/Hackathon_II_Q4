# Quickstart: View Tasks Feature

## Installation

```bash
# Navigate to project directory
cd src

# Ensure dependencies are installed
python main.py --help
```

## Usage

### List All Tasks

```bash
python main.py list
```

**Example Output**:
```
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread       Incomplete
6ba7b810-9dad-11d1-80b4-00c04fd430c8 Call mom                                     Complete
```

### List Incomplete Tasks Only

```bash
python main.py list --status incomplete
# or
python main.py list -s incomplete
```

**Example Output**:
```
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread       Incomplete
```

### List Complete Tasks Only

```bash
python main.py list --status complete
# or
python main.py list -s complete
```

**Example Output**:
```
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
6ba7b810-9dad-11d1-80b4-00c04fd430c8 Call mom                                     Complete
```

### Empty Task List

```bash
python main.py list
```

**Example Output**:
```
No tasks found. Add a task to get started.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py list` | List all tasks |
| `python main.py list --status all` | List all tasks (explicit) |
| `python main.py list -s incomplete` | List incomplete tasks |
| `python main.py list --status complete` | List complete tasks |

## Examples

### Adding and Viewing Tasks

```bash
# Add some tasks
$ python main.py add "Buy groceries" --description "Milk, Eggs, Bread"
Task 'Buy groceries' added successfully with ID 550e8400-e29b-41d4-a716-446655440000.

$ python main.py add "Call mom"
Task 'Call mom' added successfully with ID 6ba7b810-9dad-11d1-80b4-00c04fd430c8.

# View all tasks
$ python main.py list
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread       Incomplete
6ba7b810-9dad-11d1-80b4-00c04fd430c8 Call mom                                     Incomplete

# Mark a task as complete (if complete feature exists)
# Then filter to see only incomplete
$ python main.py list -s incomplete
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread       Incomplete
```

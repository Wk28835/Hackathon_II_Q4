# Quickstart: Add Task Feature

## Installation

```bash
# Navigate to project directory
cd src

# Verify Python installation
python --version
```

## Usage

### Add a Task with Title Only

```bash
python main.py add "Buy groceries"
```

**Expected Output**:
```
Task 'Buy groceries' added successfully with ID 550e8400-e29b-41d4-a716-446655440000.
```

### Add a Task with Title and Description

```bash
python main.py add "Buy groceries" --description "Milk, Eggs, Bread"
```

**Expected Output**:
```
Task 'Buy groceries' added successfully with ID 6ba7b810-9dad-11d1-80b4-00c04fd430c8.
```

### Add a Task with Empty Title (Error)

```bash
python main.py add ""
```

**Expected Output**:
```
Error: Title must not be empty.
```

### Add a Task with Whitespace-Only Title (Error)

```bash
python main.py add "   "
```

**Expected Output**:
```
Error: Title must not be empty.
```

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py add "title"` | Add a task with the given title |
| `python main.py add "title" --description "details"` | Add a task with title and description |

## Examples

### Create Your First Task

```bash
$ python main.py add "Learn Python"
Task 'Learn Python' added successfully with ID 12345678-1234-1234-1234-123456789abc.
```

### Create a Detailed Task

```bash
$ python main.py add "Complete project" --description "Finish all implementation tasks by Friday"
Task 'Complete project' added successfully with ID 87654321-4321-4321-4321-cba987654321.
```

### Handle Validation Error

```bash
$ python main.py add ""
Error: Title must not be empty.
```

```bash
$ python main.py add "  " --description "This won't work"
Error: Title must not be empty.
```

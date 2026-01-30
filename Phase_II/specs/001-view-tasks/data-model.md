# Data Model: View Tasks Feature

## Entity: Task (Reused from 001-add-task)

Represents a single todo task in the system.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (UUID4 format) |
| `title` | string | Task title |
| `description` | string | Task details |
| `status` | string | "Incomplete" or "Complete" |

---

## Entity: TaskList View

Display representation for listing tasks.

### View Format

| Column | Max Width | Description |
|--------|-----------|-------------|
| ID | 36 | UUID format (fixed) |
| Title | 20 | Truncated with "..." if longer |
| Description | 25 | Truncated with "..." if longer |
| Status | 12 | Full word ("Incomplete" or "Complete") |

### Example Output

```
ID                                  Title                Description              Status
------------------------------------ -------------------- ------------------------ ---------
550e8400-e29b-41d4-a716-446655440000 Buy groceries        Milk, Eggs, Bread       Incomplete
6ba7b810-9dad-11d1-80b4-00c04fd430c8 Call mom                                     Complete
```

---

## Filter Options

### Supported Values

| Filter | Description |
|--------|-------------|
| `all` | Show all tasks (default) |
| `incomplete` | Show only incomplete tasks |
| `complete` | Show only complete tasks |

### Filter Behavior

- Case-insensitive matching
- Applied before display
- Returns subset of tasks matching status

---

## Empty State

### Message

```
No tasks found. Add a task to get started.
```

### Display Conditions

- No tasks in storage
- Filter returns no matching tasks
- Displayed instead of table

# Data Model: Delete Task Feature

## Entity: DeleteRequest

Data structure representing a delete operation request.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | Yes | UUID of task to delete |

### Validation Rules

- `task_id`: Must be valid UUID format

---

## Entity: Task (Existing)

Represents a todo task.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (UUID4) |
| `title` | string | Task title |
| `description` | string | Task details |
| `status` | string | "Incomplete" or "Complete" |

---

## Delete Flow

```
[User Input] --> [Parse Args] --> [Validate UUID] --> [Find Task] --> [Delete] --> [Save]
                     |               |                  |              |              |
                     v               v                  v              v              v
               DeleteRequest    Error: Invalid     Error: Not    Task removed   Success message
                                   UUID format      found
```

---

## Error Messages

| Scenario | Message |
|----------|---------|
| Invalid UUID format | "Error: Invalid task ID format. Please provide a valid UUID." |
| Task not found | "Error: Task not found." |
| Delete success | "Task deleted successfully.\nID: {task_id}\nTitle: {task_title}" |

---

## Persistence

The delete operation modifies the in-memory task list and persists changes via `TaskList._save()` method, which writes to `tasks.json`.

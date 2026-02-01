# Data Model: Mark Task Status Feature

## Entity: MarkRequest

Data structure representing a mark operation request.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | Yes | UUID of task to mark |
| `new_status` | string | Yes | "Complete" or "Incomplete" |

### Validation Rules

- `task_id`: Must be valid UUID format
- `new_status`: Must be either "Complete" or "Incomplete"

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

## Status Flow

```
[User Input] --> [Parse Args] --> [Validate UUID] --> [Find Task] --> [Update Status] --> [Save]
                     |               |                  |              |                  |
                     v               v                  v              v                  v
               MarkRequest    Error: Invalid     Error: Not    Task.status     Success message
                                   UUID format      found          = new_status
```

---

## Error Messages

| Scenario | Message |
|----------|---------|
| Invalid UUID format | "Error: Invalid task ID format. Please provide a valid UUID." |
| Task not found | "Error: Task not found." |
| Both flags provided | "Error: Cannot use both --complete and --incomplete. Please specify only one." |
| Mark success | "Task status updated successfully.\nID: {task_id}\nTitle: {task_title}\nStatus: {old_status} -> {new_status}" |

---

## Persistence

The mark operation modifies the in-memory task list and persists changes via `TaskList._save()` method, which writes to `tasks.json`.

---

## State Transitions

| From \ To | Incomplete | Complete |
|-----------|------------|----------|
| Incomplete | No change | Valid transition |
| Complete | Valid transition | No change |

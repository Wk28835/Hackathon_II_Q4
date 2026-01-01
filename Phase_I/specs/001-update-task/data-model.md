# Data Model: Update Task Feature

## Entity: UpdateRequest

Data structure representing an update operation request.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `task_id` | string | Yes | UUID of task to update |
| `new_title` | string \| None | No | New title (None = don't update) |
| `new_description` | string \| None | No | New description (None = don't update) |

### Validation Rules

- `task_id`: Must be valid UUID format
- `new_title`: If provided, must pass validate_title() (not empty/whitespace)
- `new_description`: No validation (can be empty string)

### Example

```python
# Update title only
UpdateRequest(task_id="550e8400-e29b-41d4-a716-446655440000", new_title="New title", new_description=None)

# Update description only
UpdateRequest(task_id="550e8400-e29b-41d4-a716-446655440000", new_title=None, new_description="New desc")

# Update both
UpdateRequest(task_id="550e8400-e29b-41d4-a716-446655440000", new_title="New title", new_description="New desc")
```

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

## Update Flow

```
[User Input] --> [Parse Args] --> [Validate UUID] --> [Find Task] --> [Validate Title] --> [Update] --> [Save]
                     |               |                  |              |               |
                     v               v                  v              v               v
               UpdateRequest    Error: Invalid    Error: Not      Error: Empty    Success message
                                   UUID format     found           title
```

---

## Error Messages

| Scenario | Message |
|----------|---------|
| Invalid UUID format | "Invalid task ID format. Please provide a valid UUID." |
| Task not found | "Task not found." |
| Empty title | "Title must not be empty." |
| Update success | "Task updated successfully." |

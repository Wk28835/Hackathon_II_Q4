# Data Model: Add Task Feature

## Entity: Task

Represents a single todo item in the system.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | Auto-generated | Unique identifier (UUID4 format) |
| `title` | string | Yes | N/A | Task title (non-empty after stripping whitespace) |
| `description` | string | No | `""` | Optional task details |
| `status` | string | No | `"Incomplete"` | Current task state |

### Validation Rules

1. **Title Validation**:
   - Must not be `None`
   - Must not be empty string (`""`)
   - Must not be whitespace-only (e.g., `"   "`)
   - Maximum length: [Not specified - no limit applied]

2. **Description Validation**:
   - Can be empty string
   - Can be `None` (will default to `""`)

3. **Status Validation**:
   - Only `"Incomplete"` allowed on creation
   - Other values may be added by future features

### Example

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, Eggs, Bread",
  "status": "Incomplete"
}
```

---

## Entity: Task List

Container for all tasks in the current session.

### Structure

| Property | Type | Description |
|----------|------|-------------|
| `tasks` | List[Task] | Collection of all created tasks |

### Behavior

- New tasks are appended to the list
- Tasks persist until application restarts (in-memory)
- No duplicate IDs allowed

### Example

```python
tasks = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Buy groceries",
        "description": "Milk, Eggs, Bread",
        "status": "Incomplete"
    },
    {
        "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "title": "Call mom",
        "description": "",
        "status": "Incomplete"
    }
]
```

---

## State Transitions

### Task Creation Flow

```
[User Input] --> [Validate Title] --> [Generate ID] --> [Create Task] --> [Add to List]
                                          |                    |
                                          v                    v
                                   Return task           Success message
                                   with new ID
```

### Error Flow

```
[User Input] --> [Validate Title] --> [Show Error] --> [User retries]
                     |
                     v
              Title is empty/whitespace
              Error: "Title must not be empty"
```

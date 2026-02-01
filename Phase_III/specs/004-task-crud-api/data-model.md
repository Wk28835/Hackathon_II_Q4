# Data Model: Task CRUD API

**Feature**: Authenticated, user-scoped Task CRUD API
**Date**: 2026-01-10
**Phase**: Phase 1 - Design Artifacts

---

## Database Schema

### Task Table

**Table Name**: `task`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer/UUID | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| `user_id` | Integer/UUID | NOT NULL, FOREIGN KEY (users.id), INDEX | Owner of the task; enforces data isolation |
| `title` | VARCHAR(255) | NOT NULL, MIN_LENGTH(1) | Task title; required, non-empty |
| `description` | TEXT | DEFAULT '' | Optional task description; defaults to empty string |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'Incomplete' | Task state: "Incomplete" or "Complete" |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Auto-set on creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Auto-set on creation, updated on modify |

**Indexes**:
- PRIMARY KEY: `task(id)`
- FOREIGN KEY: `task(user_id) → users(id)`
- Performance Index: `task(user_id)` for fast filtering by user

**Constraints**:
- `user_id` NOT NULL: Every task must have an owner
- `title` NOT NULL: Every task must have a title
- Cascade behavior: DELETE user → DELETE all user's tasks (optional, consider retention)

---

## SQLModel Entity Definition

### Task (Core Model)

```python
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
    status: str = Field(default="Incomplete")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Properties**:
- Inherits from SQLModel: Acts as both SQLAlchemy ORM model and Pydantic validator
- `table=True`: Creates database table mapping
- All fields typed for both ORM and Pydantic
- Default factories for timestamps (set by database or application)

---

## Pydantic Schema Definitions

### TaskCreate (Request Schema)

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=2000)
```

**Usage**: POST /api/tasks request body
**Properties**:
- Accepts: title (required), description (optional)
- Does NOT accept: id, user_id, status, created_at, updated_at
- Title validation: non-empty, max 255 chars
- Description max 2000 chars (reasonable limit for todo description)

---

### TaskUpdate (Request Schema)

```python
from typing import Optional
from pydantic import BaseModel, Field

class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
```

**Usage**: PUT/PATCH /api/tasks/{id} request body
**Properties**:
- Accepts: title (optional), description (optional)
- Does NOT accept: id, user_id, status, created_at, updated_at
- Title: must be non-empty if provided
- Enables partial updates (can update only title, only description, or both)

---

### TaskResponse (Response Schema)

```python
from datetime import datetime
from pydantic import BaseModel, Field

class TaskResponse(BaseModel):
    """Schema for returning a task to the client."""
    id: int
    user_id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow ORM model to Pydantic conversion
```

**Usage**: All GET, POST, PUT, DELETE responses
**Properties**:
- Includes all task fields (id, user_id, title, description, status, timestamps)
- `from_attributes=True`: Enables conversion from SQLModel instance to Pydantic
- Read-only response (no validation needed on output)

---

### TaskList (Response Schema)

```python
from typing import List
from pydantic import BaseModel

class TaskList(BaseModel):
    """Schema for returning a list of tasks."""
    tasks: List[TaskResponse]
    total: int
```

**Usage**: GET /api/tasks list response
**Properties**:
- Returns array of TaskResponse objects
- Includes total count for pagination (future enhancement)

---

### ErrorResponse (Response Schema)

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
```

**Usage**: All error responses (400, 401, 403, 404, 500)
**Properties**:
- Simple detail message (provided by FastAPI HTTPException automatically)

---

## Data Validation Rules

### Task Validation

| Field | Validation | Error Code | Error Message |
|-------|-----------|-----------|---------------|
| `title` | Required, min_length=1, max_length=255 | 400 | "Title must not be empty" or "Title too long" |
| `description` | Optional, max_length=2000 | 400 | "Description too long" |
| `user_id` | Derived from JWT, not from request | 403 (if mismatch) | "Forbidden" |
| `status` | Must be "Incomplete" or "Complete" | 400 | "Invalid status" |
| `id` | Auto-generated by database | N/A | N/A |
| `created_at`, `updated_at` | Auto-set by database | N/A | N/A |

---

## Relationships

### Task ↔ User (One-to-Many)

```
User (1) ──── (Many) Task
  id ────────── user_id
```

**Relationship Direction**:
- User.id has many Task.user_id entries
- Task.user_id is a foreign key to User.id
- No back-reference from Task to User needed (task only knows owner's ID)
- No User table definition in this feature (managed by Frontend/Authentication)

**Data Isolation**:
- Every task belongs to exactly one user
- Users cannot access tasks with user_id != authenticated_user_id
- Query example: `SELECT * FROM task WHERE user_id = :user_id`

---

## State Transitions

### Task Status Lifecycle

```
┌─────────────┐
│ Incomplete  │  ← Default status on creation
│ (initial)   │
└──────┬──────┘
       │
       │ User marks complete
       ↓
┌─────────────┐
│  Complete   │
│ (terminal)  │
└──────┬──────┘
       │
       │ User marks incomplete
       ↓
┌─────────────┐
│ Incomplete  │
└─────────────┘
```

**States**:
- `"Incomplete"`: Task not yet completed (initial state)
- `"Complete"`: Task marked as completed

**Valid Transitions**:
- Incomplete → Complete (via mark/update)
- Complete → Incomplete (via mark/update)
- Any state → Any state (no restrictions on toggling)

**Implementation**: No state machine required; status is simple enum field

---

## Timestamps Management

### created_at

- Set automatically by database on row insert (DEFAULT CURRENT_TIMESTAMP)
- Never updated after creation
- Read-only from API perspective
- Used for audit trail and sorting by age

### updated_at

- Set automatically by database on row insert (DEFAULT CURRENT_TIMESTAMP)
- Updated automatically on every row modification (ON UPDATE CURRENT_TIMESTAMP)
- Read-only from API perspective
- Used for audit trail and conflict detection (optimistic locking)

---

## Constraints & Integrity

### Primary Key Constraint

```sql
PRIMARY KEY (id)
```

Ensures:
- Every task has a unique identifier
- No duplicate task IDs
- Fast lookups by ID

### Foreign Key Constraint

```sql
FOREIGN KEY (user_id) REFERENCES user(id)
```

Ensures:
- Every task belongs to an existing user
- Cannot create task with non-existent user_id
- Cannot delete user without handling their tasks (cascade delete or restrict)
- Maintains referential integrity

### NOT NULL Constraints

```sql
NOT NULL: user_id, title, status, created_at, updated_at
```

Ensures:
- Task always has owner (user_id)
- Task always has title (non-empty)
- Task always has status
- Timestamps always recorded

---

## Indexing Strategy

### Index 1: Primary Key (id)

```sql
PRIMARY KEY (id)
```
**Purpose**: Fast lookup by task ID
**Query Pattern**: `SELECT * FROM task WHERE id = ?`
**Performance**: O(1) lookup

### Index 2: Foreign Key (user_id)

```sql
INDEX ON (user_id)
```
**Purpose**: Fast filtering by user (list all user's tasks)
**Query Pattern**: `SELECT * FROM task WHERE user_id = ? ORDER BY created_at DESC`
**Performance**: O(log n) with index, O(n) without
**Critical for**: Every list endpoint (high volume query)

### Index 3: Composite (user_id, status) [Optional Future]

```sql
-- Deferred to Phase 2 if filtering by status becomes common
INDEX ON (user_id, status)
```
**Purpose**: Fast filtering by user AND status
**Query Pattern**: `SELECT * FROM task WHERE user_id = ? AND status = 'Incomplete'`
**Performance**: O(log n) with composite index

---

## Example Data

### Sample Task Record

```json
{
  "id": 1,
  "user_id": 42,
  "title": "Complete project report",
  "description": "Summarize Q4 findings and submit to management",
  "status": "Incomplete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:30:00Z"
}
```

### Sample Task (Updated)

```json
{
  "id": 1,
  "user_id": 42,
  "title": "Complete project report",
  "description": "Summarize Q4 findings and submit to management by EOD Friday",
  "status": "Complete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-11T09:15:00Z"
}
```

---

## Migration Considerations

### Initial Schema Creation

Use Alembic or manual SQL:

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'Incomplete',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX (user_id)
);
```

### Assumptions

- `user` table already exists (managed by Frontend/Better Auth)
- user_id field in `user` table is INTEGER or UUID (consistent with Task.user_id)
- Database supports CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP

---

## Performance & Scalability

### Storage Estimate

- Per task: ~300 bytes (id, user_id, title ~50 chars, description ~200 chars, status, timestamps)
- Per user (100 tasks): ~30 KB
- Per 1000 users: ~30 MB
- Scalable to 1M+ tasks with proper indexing and connection pooling

### Query Performance

| Query | Index | Complexity | Expected Time |
|-------|-------|-----------|---------------|
| Get by ID | Primary key | O(1) | <1ms |
| List by user | user_id index | O(log n) | 1-5ms |
| Create | None | O(1) | 5-10ms |
| Update | Primary key | O(1) | 5-10ms |
| Delete | Primary key | O(1) | 5-10ms |

**Assumptions**: Typical database, 10k-100k total tasks, good connection pooling

---

## Schema Diagram

```
┌─────────────────────────────────────────┐
│             user (external)             │
├─────────────────────────────────────────┤
│ id (PK): UUID/Int                       │
│ email: String                           │
│ [other fields managed by Frontend]      │
└────────────────────┬────────────────────┘
                     │ 1
                     │
                     │ Many
                     │
┌────────────────────↓────────────────────┐
│            task (this feature)          │
├─────────────────────────────────────────┤
│ id (PK): Int/UUID AUTO_INCREMENT        │
│ user_id (FK): Int/UUID NOT NULL →user.id│
│ title: VARCHAR(255) NOT NULL            │
│ description: TEXT DEFAULT ''            │
│ status: VARCHAR(20) DEFAULT 'Incomplete'│
│ created_at: TIMESTAMP AUTO              │
│ updated_at: TIMESTAMP AUTO              │
├─────────────────────────────────────────┤
│ PRIMARY KEY: (id)                       │
│ FOREIGN KEY: (user_id) → user(id)       │
│ INDEX: (user_id) - filtering by owner   │
└─────────────────────────────────────────┘
```

---

## Next Steps

1. **API Contracts**: Generate OpenAPI specification (contracts/openapi.yaml)
2. **Quick Start Guide**: Generate setup and first-run instructions
3. **Implementation**: Generate CRUD endpoints and database operations

# Feature Specification: Task CRUD API with Authentication

**Feature Branch**: `004-task-crud-api`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Authenticated, user-scoped Task CRUD API using FastAPI and SQLModel. This feature implements the backend API layer for Phase II, enabling multi-user task management with JWT-based authentication, user data isolation, and persistent PostgreSQL storage. The API must enforce that users can only access and modify their own tasks through proper authorization checks on every endpoint."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a new task (Priority: P1)

As an authenticated user, I want to create a new task with a title and optional description so that I can track work I need to complete.

**Why this priority**: Task creation is the foundational CRUD operation. Without the ability to add tasks, the entire feature has no value. This is independently testable and delivers core functionality.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, sending a create request with a title, and verifying the task is stored with a unique ID, the provided title and description, status "Incomplete", and the authenticated user's ID as the owner.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they create a task with a title and description, **Then** the API returns a 200 response with the created task including ID, title, description, status "Incomplete", and user_id matching the authenticated user.
2. **Given** a user is authenticated, **When** they create a task with only a title (no description), **Then** the API creates the task with an empty description field.
3. **Given** a user is authenticated, **When** they attempt to create a task without a title, **Then** the API returns a 400 error with a validation message.
4. **Given** a user is not authenticated (missing JWT token), **When** they attempt to create a task, **Then** the API returns a 401 Unauthorized response.

---

### User Story 2 - Retrieve all user tasks (Priority: P1)

As an authenticated user, I want to retrieve all my tasks so that I can see my complete task list.

**Why this priority**: Task listing is critical for users to view and manage their work. This is independently testable and essential for the MVP.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, making a list request, and verifying all tasks owned by that user are returned with complete information and no tasks from other users are visible.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token and has multiple tasks, **When** they retrieve their task list, **Then** the API returns a 200 response with all their tasks (filtered by user_id).
2. **Given** a user is authenticated with no tasks, **When** they retrieve their task list, **Then** the API returns a 200 response with an empty list.
3. **Given** User A is authenticated, **When** they retrieve their task list, **Then** only tasks with user_id matching User A are returned (no tasks from other users).
4. **Given** a user is not authenticated, **When** they attempt to retrieve tasks, **Then** the API returns a 401 Unauthorized response.

---

### User Story 3 - Retrieve a specific task (Priority: P1)

As an authenticated user, I want to retrieve a specific task by its ID so that I can view task details.

**Why this priority**: Individual task retrieval is essential for viewing full task information. This is independently testable and part of the core CRUD set.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, requesting a specific task by ID, and verifying the correct task data is returned only when the task belongs to the authenticated user.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a task with a specific ID, **When** they request that task, **Then** the API returns a 200 response with the complete task data.
2. **Given** a user is authenticated, **When** they request a task ID that does not exist, **Then** the API returns a 404 Not Found response.
3. **Given** a user is authenticated, **When** they request a task owned by another user, **Then** the API returns a 403 Forbidden response (not 404, to avoid information leakage).
4. **Given** a user is not authenticated, **When** they attempt to retrieve a task, **Then** the API returns a 401 Unauthorized response.

---

### User Story 4 - Update a task (Priority: P1)

As an authenticated user, I want to update my task's title and/or description so that I can modify task information.

**Why this priority**: Task updates are core CRUD functionality. Users must be able to modify their tasks. This is independently testable.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, sending an update request with new title/description, and verifying the task is updated with the new values while preserving other fields and user ownership.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a task, **When** they update the task's title, **Then** the API returns a 200 response with the updated task (title changed, other fields preserved).
2. **Given** a user is authenticated and owns a task, **When** they update the task's description, **Then** the API returns a 200 response with the updated task (description changed, other fields preserved).
3. **Given** a user is authenticated and owns a task, **When** they update both title and description, **Then** the API returns a 200 response with both fields updated.
4. **Given** a user is authenticated, **When** they attempt to update a task they do not own, **Then** the API returns a 403 Forbidden response.
5. **Given** a user is authenticated, **When** they attempt to update a non-existent task, **Then** the API returns a 404 Not Found response.
6. **Given** a user is not authenticated, **When** they attempt to update a task, **Then** the API returns a 401 Unauthorized response.

---

### User Story 5 - Delete a task (Priority: P1)

As an authenticated user, I want to delete a task so that I can remove completed or unwanted tasks.

**Why this priority**: Task deletion is core CRUD functionality. Users must be able to remove tasks. This is independently testable.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, sending a delete request for an owned task, and verifying the task is removed and no longer retrievable.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a task, **When** they delete that task, **Then** the API returns a 200 or 204 response and the task is no longer retrievable.
2. **Given** a user is authenticated, **When** they attempt to delete a task they do not own, **Then** the API returns a 403 Forbidden response.
3. **Given** a user is authenticated, **When** they attempt to delete a non-existent task, **Then** the API returns a 404 Not Found response.
4. **Given** a user is not authenticated, **When** they attempt to delete a task, **Then** the API returns a 401 Unauthorized response.

---

### User Story 6 - Mark task status (Priority: P2)

As an authenticated user, I want to mark a task as complete or incomplete so that I can track my progress.

**Why this priority**: Status management helps users track progress and organize their workflow. This is independently testable and adds value to the core CRUD operations, but is secondary to basic CRUD functionality.

**Independent Test**: Can be fully tested by authenticating with a valid JWT token, sending a status update request with "complete" or "incomplete", and verifying the task's status is updated while preserving other data.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and owns a task with status "Incomplete", **When** they mark it as complete, **Then** the API returns a 200 response with status changed to "Complete".
2. **Given** a user is authenticated and owns a task with status "Complete", **When** they mark it as incomplete, **Then** the API returns a 200 response with status changed to "Incomplete".
3. **Given** a user is authenticated, **When** they attempt to update status on a task they do not own, **Then** the API returns a 403 Forbidden response.
4. **Given** a user is authenticated, **When** they attempt to update status on a non-existent task, **Then** the API returns a 404 Not Found response.

---

### Edge Cases

- What happens when a user attempts to create a task with extremely long title/description? (Validation and length limits)
- How does the system handle concurrent requests from the same user? (Data consistency)
- What happens when a user's JWT token expires during an active session? (Token validation on every request)
- How does the system behave if the database connection is lost? (Error handling and recovery)
- What happens when a user attempts to modify a task ID in the request body to a different value? (Authorization must use authenticated user ID, not request body)

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT token on every protected endpoint (create, read, update, delete).
- **FR-002**: System MUST extract user identity from the JWT token signature without requiring database lookups.
- **FR-003**: System MUST create tasks with the authenticated user's ID automatically (not from request body).
- **FR-004**: System MUST enforce user data isolation: users can only access/modify tasks where user_id matches authenticated user ID.
- **FR-005**: System MUST store all tasks in PostgreSQL with SQLModel ORM.
- **FR-006**: System MUST validate that task title is not empty on creation and updates.
- **FR-007**: System MUST support filtering task list by status ("Incomplete" or "Complete").
- **FR-008**: System MUST return appropriate HTTP status codes:
  - 200/201 for successful operations
  - 400 for validation errors (invalid input)
  - 401 for missing/invalid JWT token
  - 403 for unauthorized access (accessing another user's task)
  - 404 for resource not found
  - 500 for server errors
- **FR-009**: System MUST return error responses with descriptive messages.
- **FR-010**: System MUST use RESTful API patterns: POST for create, GET for read, PUT/PATCH for update, DELETE for delete.
- **FR-011**: System MUST persist task data immediately (no eventual consistency issues).
- **FR-012**: System MUST handle task description as optional field (default to empty string).
- **FR-013**: System MUST set default status to "Incomplete" on task creation.
- **FR-014**: System MUST generate unique task IDs on creation (UUID or database auto-increment).

### Key Entities

- **Task**:
  - `id` (UUID or integer): Unique task identifier
  - `user_id` (UUID or integer): Foreign key to User (required for data isolation)
  - `title` (string, required, non-empty): Task title
  - `description` (string, optional): Task description, defaults to empty string
  - `status` (enum: "Incomplete" or "Complete"): Task state, defaults to "Incomplete"
  - `created_at` (timestamp): When task was created
  - `updated_at` (timestamp): When task was last modified
  - Constraint: Primary key on `id`, foreign key `user_id` references Users table

- **User** (referenced, not fully specified in this feature):
  - `id` (UUID or integer): Unique user identifier (extracted from JWT)
  - Relationship: One-to-Many with Tasks

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All CRUD operations complete within 500ms for typical payloads.
- **SC-002**: System enforces user data isolation on 100% of protected endpoints (no data leakage).
- **SC-003**: API returns correct HTTP status code for all error scenarios (401 for missing token, 403 for unauthorized, 404 for missing resource).
- **SC-004**: Users can create, retrieve, update, and delete their own tasks independently without affecting other users' data.
- **SC-005**: All API endpoints require valid JWT authentication (no anonymous access).
- **SC-006**: Task data persists correctly across database restarts and multiple application instances.

---

## Assumptions

1. **Authentication**: JWT tokens are issued by the Frontend (Better Auth) with a shared secret. Backend verifies signature using the same secret without requiring database lookups.
2. **User ID Storage**: User ID is encoded in the JWT payload and extracted on backend (not stored separately in request body).
3. **Database Setup**: PostgreSQL database and tables are already provisioned with proper schema for Tasks and Users.
4. **HTTP Framework**: FastAPI provides all necessary decorators and middleware for routing and error handling.
5. **Status Values**: Only two valid statuses exist: "Incomplete" and "Complete" (enum validation).
6. **Task Uniqueness**: Task IDs are globally unique across all users.
7. **Timestamps**: created_at and updated_at are managed by the database (auto-populated, not by application).
8. **Concurrency**: Database handles concurrent writes atomically (ACID properties).

---

## Dependencies & Constraints

- **Technology Stack**: FastAPI (web framework), SQLModel (ORM), PostgreSQL (database), Python 3.12+
- **Authentication**: JWT tokens with shared secret (provided by Frontend)
- **Data Validation**: Request payloads must be validated before processing
- **Constraint**: No implementation using other frameworks or databases
- **Constraint**: Backend must remain stateless (no session storage on server)
- **External**: Assumes Frontend already implements user signup/signin and JWT issuance

---

## Out of Scope

- User management (signup, signin, profile) - handled by Frontend
- Password hashing and storage - handled by Frontend via Better Auth
- Task search, sorting, or advanced filtering beyond status
- Bulk operations or batch imports
- Task attachments or media
- Task sharing or collaboration features
- Task notifications or reminders
- Rate limiting or usage quotas

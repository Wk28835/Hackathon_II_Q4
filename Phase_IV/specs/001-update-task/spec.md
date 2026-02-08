# Feature Specification: Update Task

**Feature Branch**: `001-update-task`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "update task title, description or both"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update task title (Priority: P1)

As a user, I want to update the title of an existing task so that I can correct typos or provide a more accurate description.

**Why this priority**: Title correction is a common use case when task details change or initial input was incorrect.

**Independent Test**: Can be fully tested by updating a task's title and verifying the change is reflected when listing tasks.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy groceries", **When** the user updates the title to "Buy organic groceries", **Then** the task's title is changed and the change persists.
2. **Given** a task exists, **When** the user updates the title to an empty string, **Then** an error message is displayed and the title is not changed.
3. **Given** a task exists, **When** the user updates the title to only whitespace, **Then** an error message is displayed and the title is not changed.

---

### User Story 2 - Update task description (Priority: P1)

As a user, I want to update the description of an existing task so that I can add more details or correct information.

**Why this priority**: Description updates allow users to elaborate on task details over time.

**Independent Test**: Can be fully tested by updating a task's description and verifying the change is reflected when listing tasks.

**Acceptance Scenarios**:

1. **Given** a task exists with description "Milk", **When** the user updates the description to "Milk, Eggs, Bread", **Then** the task's description is changed.
2. **Given** a task exists, **When** the user clears the description, **Then** the task's description becomes an empty string.
3. **Given** a task exists, **When** the user updates only the description, **Then** the task's title remains unchanged.

---

### User Story 3 - Update both title and description (Priority: P2)

As a user, I want to update both the title and description of a task in a single command so that I can make comprehensive changes efficiently.

**Why this priority**: Convenience for users who need to make multiple changes to the same task.

**Independent Test**: Can be fully tested by updating both title and description and verifying both changes are reflected.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user provides both new title and new description, **Then** both fields are updated simultaneously.
2. **Given** a task exists, **When** the user provides an invalid title while updating both, **Then** neither field is updated and an error is shown.

---

### User Story 4 - Task not found error (Priority: P1)

As a user, I want to receive clear feedback when trying to update a non-existent task so that I know the operation failed.

**Why this priority**: Users need to know when their command didn't work and why.

**Independent Test**: Can be fully tested by attempting to update a task with an invalid ID and verifying an appropriate error message.

**Acceptance Scenarios**:

1. **Given** no task exists with ID "invalid-id", **When** the user attempts to update that task, **Then** an error message "Task not found" is displayed.
2. **Given** the user provides a malformed UUID, **When** attempting to update, **Then** an error message is displayed.

---

### Edge Cases

- What happens when the new title is the same as the current title? [Assumed: No-op, success message shown]
- What happens when updating a task that was just added in the same session? [Assumed: Works normally]
- What happens when the task ID format is invalid? [Assumed: Error message about invalid ID format]

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an "update" command to modify existing tasks.
- **FR-002**: System MUST require a task ID to identify which task to update.
- **FR-003**: System MUST allow updating title only via `--title` flag.
- **FR-004**: System MUST allow updating description only via `--description` flag.
- **FR-005**: System MUST allow updating both title and description in a single command.
- **FR-006**: System MUST validate that the new title is not empty or whitespace-only.
- **FR-007**: System MUST display an error message when title validation fails.
- **FR-008**: System MUST display a success message with updated task details.
- **FR-009**: System MUST display "Task not found" when the specified ID doesn't exist.
- **FR-010**: System MUST persist the updated task to storage.

### Key Entities *(include if feature involves data)*

- **Task**: Existing entity
  - id: Unique identifier
  - title: Task title
  - description: Task details
  - status: "Incomplete" or "Complete"

- **Update Request**: Data structure for update operation
  - task_id: UUID of task to update
  - new_title: Optional new title
  - new_description: Optional new description

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update a task title within 5 seconds of issuing the command.
- **SC-002**: 100% of valid updates are persisted and reflected in subsequent list commands.
- **SC-003**: Users receive immediate feedback (within 2 seconds) for both success and error scenarios.
- **SC-004**: 95% of users successfully update a task on first attempt when using valid input.
- **SC-005**: Error messages are clear, with 90% of users understanding how to correct their input.

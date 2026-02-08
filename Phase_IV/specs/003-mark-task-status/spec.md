# Feature Specification: Mark Task Status

**Date**: 2025-12-31
**Status**: Draft
**Feature**: Allow users to mark a todo task as complete or incomplete using its ID via the CLI

## Overview

This feature enables users to change the completion status of tasks in their todo list using the command-line interface. Users can mark tasks as complete or incomplete by providing the task's unique identifier (UUID) and a status flag. Upon successful status update, a confirmation message is displayed. If the provided ID does not match any existing task, a clear error message is shown.

## User Scenarios & Testing

### Primary User Flow

1. User lists tasks to find the ID of the task they want to mark
2. User runs the mark command with the task ID and desired status
3. System updates the task's completion status
4. System displays a confirmation message showing the updated task details

### Acceptance Scenarios

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Mark complete | User has incomplete task in list | User provides valid task ID with complete flag | Task status updated to Complete, confirmation shown |
| Mark incomplete | User has complete task in list | User provides valid task ID with incomplete flag | Task status updated to Incomplete, confirmation shown |
| Task not found | User has tasks in their list | User provides non-existent task ID | Error message displayed, no status change |
| Invalid ID format | User types command | User provides malformed ID string | Error message indicating invalid ID format |
| Toggle status | User wants to change status | User provides task ID with opposite status | Task status updated, confirmation shows new status |

### Edge Cases

- Marking a task that is already marked as the requested status
- Marking the last task in the list
- Marking a task that was just added
- Providing an empty string as task ID
- Providing whitespace-only string as task ID
- Case sensitivity of status flag values

## Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR1 | User can mark a task complete using `python main.py mark <task-id> --complete` | Command accepts task ID and complete flag, status updated |
| FR2 | User can mark a task incomplete using `python main.py mark <task-id> --incomplete` | Command accepts task ID and incomplete flag, status updated |
| FR3 | System validates task ID format before attempting update | Invalid UUID format produces error message, no change occurs |
| FR4 | System verifies task exists before attempting update | Non-existent ID produces error message, no change occurs |
| FR5 | System displays confirmation message after successful status update | Message includes task title, old status, and new status |
| FR6 | System displays error message for non-existent task | Message clearly indicates task was not found |
| FR7 | System displays error message for invalid ID format | Message indicates ID format is invalid |

## Success Criteria

1. **Functional Completeness**: Users can successfully mark any task as complete or incomplete with a single command
2. **Error Handling**: 100% of invalid inputs (non-existent ID, malformed ID) result in clear error messages and no data loss
3. **User Experience**: All users can understand how to mark tasks from the CLI help and success/error messages
4. **Data Integrity**: Task status updates are permanent and persisted; other task data remains unaffected

## Key Entities

### Task (Existing)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (UUID4) |
| `title` | string | Task title |
| `description` | string | Task details |
| `status` | string | "Incomplete" or "Complete" |

## Assumptions

1. Task IDs remain UUID4 format as implemented in existing features
2. Status values are restricted to "Incomplete" and "Complete" only
3. Only the task matching the exact ID is modified (no cascading updates)
4. The CLI follows the same command structure pattern as existing commands (add, list, update, delete)
5. Users will use the list command to find task IDs before marking status
6. The `--complete` and `--incomplete` flags are mutually exclusive

## Out of Scope

- Bulk status updates for multiple tasks at once
- Status update by title or other attributes (only by ID)
- Custom status values beyond "Incomplete" and "Complete"
- Automatic status based on due dates or other criteria
- Status history or audit trail

## Dependencies

- Existing Task dataclass with id, title, description, status fields
- Existing TaskList storage class with in-memory list and JSON file persistence
- Existing validation module for input validation
- Existing UUID validation patterns from update and delete features

## Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | Status update operation completes in under 1 second |
| Reliability | No data corruption if update fails mid-operation |
| Usability | Error messages clearly explain what went wrong and how to fix it |
| Consistency | Command follows existing CLI patterns (positional args, optional flags) |

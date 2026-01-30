# Implementation Plan: Update Task

**Feature Branch**: `001-update-task`
**Created**: 2025-12-30
**Feature Spec**: [spec.md](./spec.md)

## Technical Context

**Architecture Type**: CLI command extending existing todo application

**Dependencies**:
- Builds on `001-add-task` and `001-view-tasks` features
- Reuses Task dataclass, TaskList storage, validation functions
- Uses existing JSON file persistence

**Update Operation**:
- Find task by ID in TaskList
- Update fields as specified
- Persist changes to tasks.json

**Key Technical Decisions**:
- ID-based lookup: Linear search through TaskList.tasks
- Partial updates: Only specified fields are changed
- Validation: Title validation before any update

**Known Unknowns**:
- N/A - Requirements are clear and straightforward

---

## Constitution Check

**Principles from constitution.md**: [File not found - using standard principles]

| Principle | Status | Notes |
|-----------|--------|-------|
| User Value First | ✅ PASS | All requirements directly serve user needs |
| Simplicity | ✅ PASS | Minimal, focused implementation |
| Testability | ✅ PASS | All scenarios are independently testable |
| Single Responsibility | ✅ PASS | Each function has one clear purpose |

**Gate Evaluation**:
- ✅ No gate violations detected
- ✅ Scope is appropriately bounded
- ✅ Feature can be implemented incrementally

---

## Phase 0: Research & Clarifications

### Findings

This feature extends the existing todo application with update capability:

1. **Task Lookup**: Need to find task by ID in the TaskList
2. **Partial Updates**: Update only specified fields (title and/or description)
3. **Validation**: Apply title validation if title is being updated
4. **Persistence**: Save changes to tasks.json after update

### research.md

**Decision**: Linear search for task lookup

**Rationale**:
- Task list is small (typically < 100 tasks)
- UUID lookup is simple and fast enough
- No need for complex indexing

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| Linear search | Simple, no extra code | O(n) lookup |
| Dictionary index | O(1) lookup | More complex, memory |
| UUID library | Standard | Overkill for this use case |

---

## Phase 1: Design

### data-model.md

```python
# UpdateRequest (data class or NamedTuple)
class UpdateRequest(NamedTuple):
    task_id: str          # UUID string
    new_title: str | None # None means don't update
    new_description: str | None # None means don't update
```

**Validation Rules**:
- If new_title is provided: must pass validate_title()
- task_id must be a valid UUID format
- At least one of new_title or new_description must be provided

### contracts/

No external API contracts needed - CLI command only.

### quickstart.md

```bash
# Update title only
python main.py update <task-id> --title "New title"

# Update description only
python main.py update <task-id> --description "New description"

# Update both
python main.py update <task-id> --title "New title" --description "New description"

# Example output on success:
# Task updated successfully:
# ID: <id>
# Title: New title
# Description: New description

# Example output on error:
# Error: Task not found.

# Example output for validation error:
# Error: Title must not be empty.
```

---

## Phase 2: Implementation Tasks

### Task List

#### Phase 2.1: CLI Extension

- [ ] **TASK-001**: Update `src/cli.py` with update command
  - Add `update` subparser to command parser
  - Required positional argument: task_id
  - Optional `--title` flag for new title
  - Optional `--description` / `-d` flag for new description
  - Add help text for each option

#### Phase 2.2: Update Handler

- [ ] **TASK-002**: Create `src/update_handler.py` for update logic
  - `find_task_by_id(task_id)` function returning Task or None
  - `update_task(task, new_title, new_description)` function
  - Returns tuple: (success: bool, message: str)

#### Phase 2.3: Main Integration

- [ ] **TASK-003**: Update `src/main.py` with update command handler
  - Initialize TaskList from existing storage
  - Parse update arguments
  - Validate task ID format
  - Find and update task
  - Display success/error message

#### Phase 2.4: Testing

- [ ] **TASK-004**: Update `tests/test_add_task.py` with update tests
  - Test update title only
  - Test update description only
  - Test update both fields
  - Test update with empty title (error)
  - Test update non-existent task (error)
  - Test update with invalid ID format (error)
  - Test persistence of updates

---

## Generated Artifacts

| File | Status |
|------|--------|
| [plan.md](./plan.md) | ✅ Complete |
| [research.md](./research.md) | ✅ Complete |
| [data-model.md](./data-model.md) | ✅ Complete |
| `quickstart.md` | ✅ Inline |
| `contracts/` | N/A (CLI app) |

---

## Next Steps

Run `/speckit.implement` to execute the implementation tasks.

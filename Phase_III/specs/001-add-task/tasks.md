# Tasks: Add Task Feature

**Feature**: Add Task
**Branch**: 001-add-task
**Created**: 2025-12-30
**Completed**: 2025-12-30

## Dependency Graph

```
Phase 1 (Setup)
    |
    v
Phase 2 (Foundational) <-- Required by all User Stories
    |
    +---> Phase 3 (US1: Add Task)
    |
    +---> Phase 4 (US2: Error Handling)
    |
    +---> Phase 5 (US3: Confirmation)
    |
    v
Phase 6 (Polish)
```

**User Story Dependencies**:
- US1 (Add Task): Requires Phase 2
- US2 (Error Handling): Requires Phase 2
- US3 (Confirmation): Requires Phase 2 and US1

**Parallel Execution Opportunities**:
- Phase 2 tasks can be executed in parallel (different files, no dependencies)
- US1 and US2 can run in parallel (both depend only on Phase 2)

---

## Phase 1: Setup

**Goal**: Initialize project structure for Python CLI application

### Tasks

- [x] T001 Create `src/` directory structure
- [x] T002 Create `src/__init__.py` package marker
- [x] T003 Create `tests/` directory structure
- [x] T004 Create `tests/__init__.py` package marker
- [x] T005 Create `.gitignore` with Python patterns

**Phase Completion Criteria**: Project directories exist and .gitignore is configured
**Status**: ✅ COMPLETED

---

## Phase 2: Foundational

**Goal**: Create core components required by all user stories

**Independent Test**: Can be tested by importing Task, TaskList, and validate_title from their modules

### Tasks

- [x] T010 [P] Create `src/task.py` with Task dataclass
  - Fields: id (UUID), title (str), description (str), status (str)
  - Add `__repr__` for debugging
  - Add `to_dict()` method for serialization

- [x] T011 [P] Create `src/validation.py` with `validate_title()` function
  - Check for None, empty string, whitespace-only
  - Return tuple: (is_valid: bool, error_message: str | None)

- [x] T012 [P] Create `src/storage.py` with TaskList class
  - `tasks: List[Task]` attribute for in-memory storage
  - `add_task(title, description)` method returning Task
  - Unique ID generation using uuid4
  - Default status: "Incomplete"

**Phase Completion Criteria**: All core components importable and functional
**Status**: ✅ COMPLETED

---

## Phase 3: User Story 1 - Add Task

**Goal**: Allow users to add tasks with title and optional description

**Independent Test**: Can create a task via CLI and verify it appears in storage

### Tasks

- [x] T020 [US1] Create `src/cli.py` with argument parser
  - `add` command with required title positional argument
  - `--description` optional flag for description
  - Parse and return namespace with title and description

- [x] T021 [US1] Create `src/main.py` entry point
  - Initialize TaskList storage
  - Route `add` command to task creation
  - Display success message on task creation

**Story Completion Criteria**:
- `python main.py add "Buy groceries"` creates a task with ID
- `python main.py add "Task" --description "Details"` creates task with description
- Tasks are stored in memory and retrievable
**Status**: ✅ COMPLETED

---

## Phase 4: User Story 2 - Error Handling

**Goal**: Provide clear feedback when title is empty or whitespace

**Independent Test**: Can attempt to create task with invalid title and see error message

### Tasks

- [x] T030 [US2] Integrate title validation in CLI
  - Call validate_title() before task creation
  - Display error message if validation fails
  - Exit with error code on validation failure

**Story Completion Criteria**:
- `python main.py add ""` outputs "Error: Title must not be empty."
- `python main.py add "   "` outputs "Error: Title must not be empty."
- No task is created on validation failure
**Status**: ✅ COMPLETED

---

## Phase 5: User Story 3 - Confirmation Message

**Goal**: Show success message with task title and ID after creation

**Independent Test**: Can verify success message format after task creation

### Tasks

- [x] T040 [US3] Format success message in main.py
  - Message format: "Task '<title>' added successfully with ID <id>."
  - Display message after successful task creation

**Story Completion Criteria**:
- `python main.py add "Buy groceries"` outputs "Task 'Buy groceries' added successfully with ID <uuid>."
**Status**: ✅ COMPLETED

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete testing and finalize implementation

### Tasks

- [x] T050 Create `tests/test_add_task.py` with unit tests
  - Test successful task creation with title only
  - Test successful task creation with description
  - Test empty title validation
  - Test whitespace-only title validation
  - Test unique ID generation
  - Test default status value
  - Test in-memory storage persistence

- [x] T051 Verify all acceptance scenarios from spec.md
  - Scenario 1: Empty list, task with title and description
  - Scenario 2: Existing tasks, new task with unique ID
  - Scenario 3: Task with title only (empty description)
  - Scenario 4: Empty title error message
  - Scenario 5: Whitespace title error message
  - Scenario 6: Success message with title and ID

**Phase Completion Criteria**: All tests pass and acceptance scenarios verified
**Status**: ✅ COMPLETED

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 14 |
| Completed Tasks | 14 |
| Setup Tasks | 5 |
| Foundational Tasks | 3 |
| User Story 1 Tasks | 2 |
| User Story 2 Tasks | 1 |
| User Story 3 Tasks | 1 |
| Polish Tasks | 2 |

**Parallel Opportunities**: 3 tasks in Phase 2 ran in parallel

**Test Results**: 22/22 tests passing

**Implementation Complete**: All phases finished, all acceptance scenarios verified

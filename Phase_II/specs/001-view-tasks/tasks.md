# Tasks: View Tasks Feature

**Feature**: View Tasks
**Branch**: 001-view-tasks
**Created**: 2025-12-30
**Completed**: 2025-12-30

## Dependency Graph

```
Phase 1 (Setup)
    |
    v
Phase 2 (Foundational) <-- Required by all User Stories
    |
    +---> Phase 3 (US1: View all tasks)
    |
    +---> Phase 4 (US2: Filter by status)
    |
    +---> Phase 5 (US3: Empty state)
    |
    v
Phase 6 (Polish)
```

**User Story Dependencies**:
- US1 (View all tasks): Requires Phase 2
- US2 (Filter by status): Requires Phase 2 and US1 (shares display logic)
- US3 (Empty state): Requires Phase 2 (can be tested independently)

**Parallel Execution Opportunities**:
- T020 and T040 can run in parallel (different files, no dependencies)
- T030 depends on T020 (both modify main.py)

---

## Phase 1: Setup

**Goal**: Verify project structure and dependencies

### Tasks

- [x] T001 Verify `src/` directory exists with existing modules from 001-add-task
- [x] T002 Verify `tests/` directory exists with existing test file
- [x] T003 Install pytest if not already available

**Phase Completion Criteria**: Project structure verified and pytest available
**Status**: ✅ COMPLETED

---

## Phase 2: Foundational

**Goal**: Create list display handler module used by all user stories

**Independent Test**: Can be tested by importing list_handler functions and verifying output format

### Tasks

- [x] T010 [P] Create `src/list_handler.py` with display logic
  - `format_task_table(tasks)` function returning formatted table string
  - `format_empty_message()` function returning "No tasks found. Add a task to get started."
  - `truncate_text(text, max_length)` helper function
  - Column widths: ID (36), Title (20), Description (25), Status (12)
  - Handle tabulate library with custom fallback

**Phase Completion Criteria**: list_handler module can format tasks into table or empty message
**Status**: ✅ COMPLETED

---

## Phase 3: User Story 1 - View All Tasks

**Goal**: Allow users to view all tasks with ID, title, description, and status

**Independent Test**: Can run list command and see all tasks in table format

### Tasks

- [x] T020 [US1] Update `src/cli.py` with list command
  - Add `list` subparser to command parser
  - Add `--status` / `-s` optional flag with choices: all, incomplete, complete
  - Set default status to "all"

- [x] T021 [US1] Update `src/main.py` with list command handler
  - Add `handle_list(args)` function
  - Initialize TaskList storage
  - Get all tasks from storage
  - Pass tasks to list_handler for display
  - Print formatted output

**Story Completion Criteria**:
- `python main.py list` displays all tasks in table format
- Output shows ID, Title, Description, Status columns
- Tasks with varying description lengths display correctly
**Status**: ✅ COMPLETED

---

## Phase 4: User Story 2 - Filter by Status

**Goal**: Allow users to filter tasks by incomplete or complete status

**Independent Test**: Can run `python main.py list -s incomplete` and see only incomplete tasks

### Tasks

- [x] T030 [US2] Implement status filtering in main.py handler
  - Parse --status / -s flag value
  - Apply case-insensitive filter to tasks list
  - Handle "incomplete", "complete", "all" values
  - Pass filtered tasks to list_handler

- [x] T031 [US2] Handle empty filter results
  - When filter returns no tasks, show empty state message
  - Message: "No tasks found matching filter '<status>'."

**Story Completion Criteria**:
- `python main.py list --status incomplete` shows only incomplete tasks
- `python main.py list -s complete` shows only complete tasks
- `python main.py list --status all` shows all tasks
**Status**: ✅ COMPLETED

---

## Phase 5: User Story 3 - Empty State

**Goal**: Show helpful message when no tasks exist

**Independent Test**: Can run `python main.py list` with empty storage and see informative message

### Tasks

- [x] T040 [US3] Ensure empty message displays when no tasks exist
  - Check if TaskList is empty
  - Call format_empty_message() instead of format_task_table()
  - Message: "No tasks found. Add a task to get started."

- [x] T041 [US3] Ensure empty message displays for filtered results
  - When status filter matches no tasks, show filter-specific message
  - Message: "No tasks found matching filter '<filter>'."

**Story Completion Criteria**:
- `python main.py list` with no tasks shows empty state message
- `python main.py list -s incomplete` with no incomplete tasks shows filter message
**Status**: ✅ COMPLETED

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Complete testing and finalize implementation

### Tasks

- [x] T050 Update `tests/test_view_tasks.py` with view tests
  - Test list command with multiple tasks
  - Test list command with empty tasks
  - Test filtering by incomplete status
  - Test filtering by complete status
  - Test filtering by all status
  - Test table formatting with various task lengths
  - Test empty state message display

- [x] T051 Verify all acceptance scenarios from spec.md
  - Scenario 1: List all tasks displays ID, title, description, status
  - Scenario 2: List all tasks shows both complete and incomplete
  - Scenario 3: Long descriptions display correctly
  - Scenario 4: Filter incomplete shows only incomplete
  - Scenario 5: Filter complete shows only complete
  - Scenario 6: Empty filter shows appropriate message
  - Scenario 7: No tasks shows "No tasks found" message

**Phase Completion Criteria**: All tests pass and acceptance scenarios verified
**Status**: ✅ COMPLETED

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 11 |
| Completed Tasks | 11 |
| Setup Tasks | 3 |
| Foundational Tasks | 1 |
| User Story 1 Tasks | 2 |
| User Story 2 Tasks | 2 |
| User Story 3 Tasks | 2 |
| Polish Tasks | 2 |

**Test Results**: 22/22 tests passing

**CLI Commands**:
```bash
python main.py list                  # List all tasks
python main.py list --status all     # List all tasks (explicit)
python main.py list -s incomplete    # List incomplete tasks
python main.py list --status complete # List complete tasks
```

**Example Output**:
```
ID                                   Title                Description               Status
------------------------------------ -------------------- ------------------------- ------------
5e47ec6b-ced8-459d-afa7-e00ca5941745 Buy groceries        Milk, Eggs, Bread         Incomplete
c2ae56ba-128d-4e8c-9385-9aedb68cdb8f Call mom                                       Incomplete
```

**Implementation Complete**: All user stories finished and verified

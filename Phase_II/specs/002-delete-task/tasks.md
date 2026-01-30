# Tasks: Delete Task

**Input**: Design documents from `/specs/002-delete-task/`
**Prerequisites**: plan.md (completed), spec.md (completed), data-model.md (completed)

**Tests**: Included - tests are part of the implementation following project standards

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: CLI Argument Parsing (US1)

**Goal**: Add delete command argument parsing to CLI module

**Independent Test**: Run `python src/main.py delete --help` and verify the help message displays correctly

### Tests for CLI Parsing

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Add TestDeleteCLI class in tests/test_add_task.py with parse_delete_args tests

### Implementation for CLI Parsing

- [x] T002 [US1] Add DeleteTaskArgs NamedTuple in src/cli.py
- [x] T003 [US1] Add parse_delete_args() function in src/cli.py
- [x] T004 [US1] Add delete subparser to create_parser() in src/cli.py

**Checkpoint**: CLI parsing complete - delete command is discoverable via --help

---

## Phase 2: Delete Handler Module (US1)

**Goal**: Implement delete logic in a new handler module

**Independent Test**: Import delete_handler functions and verify they exist with correct signatures

### Tests for Delete Handler

- [x] T005 [P] [US1] Add TestIsValidUUID class in tests/test_add_task.py
- [x] T006 [P] [US1] Add TestFindTaskByID class in tests/test_add_task.py
- [x] T007 [P] [US1] Add TestDeleteTask class in tests/test_add_task.py
- [x] T008 [P] [US1] Add TestFormatDeleteSuccess class in tests/test_add_task.py

### Implementation for Delete Handler

- [x] T009 [US1] Create src/delete_handler.py with is_valid_uuid() function
- [x] T010 [US1] Add find_task_by_id() function to src/delete_handler.py
- [x] T011 [US1] Add delete_task() function to src/delete_handler.py
- [x] T012 [US1] Add format_delete_success() function to src/delete_handler.py

**Checkpoint**: Delete handler module complete - all functions can be imported and called

---

## Phase 3: Main Entry Point Integration (US1)

**Goal**: Connect delete command to handler in main.py

**Independent Test**: Run `python src/main.py delete <valid-uuid>` and verify exit code and output

### Tests for Integration

- [x] T013 [US1] Add TestDeleteIntegration class in tests/test_add_task.py with full workflow tests

### Implementation for Main Integration

- [x] T014 [US1] Import delete handler functions in src/main.py
- [x] T015 [US1] Add "delete" command routing in main() function in src/main.py
- [x] T016 [US1] Implement handle_delete(args) function in src/main.py

**Checkpoint**: Full delete workflow works end-to-end

---

## Phase 4: Integration Tests (US1)

**Goal**: Verify all delete scenarios work correctly

### Final Integration Tests

- [x] T017 [US1] Test successful task deletion via main()
- [x] T018 [US1] Test deletion with invalid UUID format
- [x] T019 [US1] Test deletion of non-existent task ID
- [x] T020 [US1] Test task persistence after deletion

**Checkpoint**: All acceptance scenarios verified working

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and validation

- [x] T021 [P] Update quickstart.md if command syntax changed
- [x] T022 Run pytest tests/ to verify all tests pass
- [x] T023 Verify CLI help displays delete command correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (CLI)**: No dependencies - start here
- **Phase 2 (Handler)**: Depends on Phase 1 completion
- **Phase 3 (Integration)**: Depends on Phase 2 completion
- **Phase 4 (Tests)**: Depends on Phase 3 completion
- **Phase 5 (Polish)**: Depends on all phases complete

### Within Each User Story

- CLI parsing before handler implementation
- Handler implementation before integration
- Integration before final tests
- Story complete before polish phase

### Parallel Opportunities

- All test tasks marked [P] can run in parallel
- T002-T004 (CLI) can proceed sequentially but T002 must complete first
- T009-T012 (Handler) have no dependencies on each other except T009 (is_valid_uuid)

---

## Parallel Example

```bash
# Launch CLI tests in parallel:
Task: "Add TestDeleteCLI class in tests/test_add_task.py"
Task: "Add TestIsValidUUID class in tests/test_add_task.py"

# Launch handler tests in parallel:
Task: "Add TestFindTaskByID class in tests/test_add_task.py"
Task: "Add TestDeleteTask class in tests/test_add_task.py"
Task: "Add TestFormatDeleteSuccess class in tests/test_add_task.py"
```

---

## Implementation Strategy

### MVP First (User Story Only - Single Feature)

1. Complete Phase 1: CLI Argument Parsing
2. Complete Phase 2: Delete Handler Module
3. Complete Phase 3: Main Entry Point Integration
4. Complete Phase 4: Integration Tests
5. Complete Phase 5: Polish
6. **STOP and VALIDATE**: Run full test suite
7. Deploy/demo if ready

### Single User Story Workflow

This feature has only ONE user story (US1: Delete Task), so the workflow is linear:
1. CLI parsing → Handler → Integration → Tests → Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to the Delete Task user story
- All tasks must complete before the feature is fully functional
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at each checkpoint to validate progress
- No cross-story dependencies (single story feature)

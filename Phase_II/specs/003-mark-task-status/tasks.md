# Tasks: Mark Task Status

**Input**: Design documents from `/specs/003-mark-task-status/`
**Prerequisites**: plan.md (completed), spec.md (completed), data-model.md (completed)

**Tests**: Included - tests are part of the implementation following project standards

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: CLI Argument Parsing (US1)

**Goal**: Add mark command argument parsing to CLI module with mutually exclusive status flags

**Independent Test**: Run `python src/main.py mark --help` and verify the help message displays correctly with --complete and --incomplete flags

### Tests for CLI Parsing

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T001 [P] [US1] Add TestMarkCLI class in tests/test_add_task.py with parse_mark_args tests

### Implementation for CLI Parsing

- [x] T002 [US1] Add MarkTaskArgs NamedTuple in src/cli.py
- [x] T003 [US1] Add parse_mark_args() function in src/cli.py with mutually exclusive group
- [x] T004 [US1] Add mark subparser to create_parser() in src/cli.py

**Checkpoint**: CLI parsing complete - mark command is discoverable via --help

---

## Phase 2: Mark Handler Module (US1)

**Goal**: Implement mark status logic in a new handler module

**Independent Test**: Import mark_handler functions and verify they exist with correct signatures

### Tests for Mark Handler

- [x] T005 [P] [US1] Add TestMarkTask class in tests/test_add_task.py
- [x] T006 [P] [US1] Add TestFormatMarkSuccess class in tests/test_add_task.py

### Implementation for Mark Handler

- [x] T007 [US1] Create src/mark_handler.py with mark_task() function
- [x] T008 [US1] Add format_mark_success() function to src/mark_handler.py

**Checkpoint**: Mark handler module complete - all functions can be imported and called

---

## Phase 3: Main Entry Point Integration (US1)

**Goal**: Connect mark command to handler in main.py

**Independent Test**: Run `python src/main.py mark <valid-uuid> --complete` and verify exit code and output

### Tests for Integration

- [x] T009 [US1] Add TestMarkIntegration class in tests/test_add_task.py with full workflow tests

### Implementation for Main Integration

- [x] T010 [US1] Import mark handler functions in src/main.py
- [x] T011 [US1] Add "mark" command routing in main() function in src/main.py
- [x] T012 [US1] Implement handle_mark(args) function in src/main.py

**Checkpoint**: Full mark workflow works end-to-end

---

## Phase 4: Integration Tests (US1)

**Goal**: Verify all mark scenarios work correctly

### Final Integration Tests

- [x] T013 [US1] Test marking task as complete via main()
- [x] T014 [US1] Test marking task as incomplete via main()
- [x] T015 [US1] Test marking with invalid UUID format
- [x] T016 [US1] Test marking non-existent task ID
- [x] T017 [US1] Test task persistence after status change

**Checkpoint**: All acceptance scenarios verified working

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and validation

- [x] T018 [P] Update quickstart.md if command syntax changed
- [x] T019 Run pytest tests/ to verify all tests pass
- [x] T020 Verify CLI help displays mark command correctly

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
- T007-T008 (Handler) have no dependencies on each other

---

## Parallel Example

```bash
# Launch CLI tests in parallel:
Task: "Add TestMarkCLI class in tests/test_add_task.py"

# Launch handler tests in parallel:
Task: "Add TestMarkTask class in tests/test_add_task.py"
Task: "Add TestFormatMarkSuccess class in tests/test_add_task.py"
```

---

## Implementation Strategy

### MVP First (User Story Only - Single Feature)

1. Complete Phase 1: CLI Argument Parsing
2. Complete Phase 2: Mark Handler Module
3. Complete Phase 3: Main Entry Point Integration
4. Complete Phase 4: Integration Tests
5. Complete Phase 5: Polish
6. **STOP and VALIDATE**: Run full test suite
7. Deploy/demo if ready

### Single User Story Workflow

This feature has only ONE user story (US1: Mark Task Status), so the workflow is linear:
1. CLI parsing → Handler → Integration → Tests → Polish

---

## Notes

- [P] tasks = different files, no dependencies
- [US1] label maps task to the Mark Task Status user story
- All tasks must complete before the feature is fully functional
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at each checkpoint to validate progress
- No cross-story dependencies (single story feature)

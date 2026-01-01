# Implementation Plan: Delete Task

**Branch**: `002-delete-task` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-delete-task/spec.md`

## Summary

Enable users to delete existing todo tasks via CLI command `python main.py delete <task-id>`. The feature validates the task ID format, verifies task existence, removes the task from storage, and displays a confirmation message. Error cases (invalid ID format, non-existent task) display clear error messages without data loss.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: Python standard library (argparse, uuid, json)
**Storage**: In-memory list with JSON file persistence (TaskList class)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single Python project (CLI application)
**Performance Goals**: Deletion operation completes in under 1 second
**Constraints**: Permanent deletion (no undo), ID-based deletion only, immediate execution (no confirmation prompts)
**Scale/Scope**: Single-user CLI, typically <100 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Check | Status | Notes |
|-------|--------|-------|
| All features use Spec-Kit Plus | PASS | Following spec-driven development |
| In-memory storage only | PASS | No database required |
| Error handling for invalid inputs | PASS | Validates ID format and existence |
| CLI interface user-friendly | PASS | Clear success/error messages |
| Unique auto-generated IDs | PASS | Uses existing UUID4 implementation |

**Phase 1 Re-check**: All checks still pass - design follows established patterns.

**Result**: All gates pass - no violations to track.

## Project Structure

### Documentation (this feature)

```text
specs/002-delete-task/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # N/A - no unknowns requiring research
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # N/A - CLI command, no API contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── cli.py               # Add parse_delete_args(), update create_parser()
├── main.py              # Add handle_delete() function and routing
├── delete_handler.py    # NEW - is_valid_uuid(), find_task_by_id(), delete_task(), format_delete_success()
├── storage.py           # Existing TaskList class
├── task.py              # Existing Task dataclass
├── validation.py        # Existing validate_title()
├── list_handler.py      # Existing
├── update_handler.py    # Existing

tests/
└── test_add_task.py     # Add delete tests (TestDelete*, TestDeleteCLI, TestDeleteIntegration)
```

**Structure Decision**: The delete feature follows the existing handler pattern established by `update_handler.py`. A new `delete_handler.py` module will contain all delete-specific logic, mirroring the update feature structure.

## Phase 0: Research

**Status**: Not required - no unknowns requiring research.

The delete feature leverages existing patterns:
- UUID validation: Already implemented in `update_handler.py` (`is_valid_uuid`)
- Task lookup: Already implemented in `update_handler.py` (`find_task_by_id`)
- Storage persistence: Already implemented in `TaskList._save()`
- CLI argument parsing: Follows existing patterns in `cli.py`

## Phase 1: Design

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Delete handler module | Create `delete_handler.py` | Mirrors `update_handler.py` pattern, keeps code organized |
| Deletion method | List.remove() by task object | Efficient O(n) operation, task object available from lookup |
| Return on success | Exit code 0 | Consistent with add/update/list commands |
| Return on error | Exit code 1 | Standard error handling |
| Confirmation message | Show deleted task title and ID | Helps user verify correct task was deleted |

### Implementation Tasks (Phase 2)

**TASK-001**: Update `src/cli.py`
- Add `DeleteTaskArgs` NamedTuple
- Add `parse_delete_args()` function
- Add `delete` subparser to `create_parser()`

**TASK-002**: Create `src/delete_handler.py`
- `is_valid_uuid(val: str) -> bool` - Reuse from update_handler or create shared utility
- `find_task_by_id(tasks: List[Task], task_id: str) -> Task | None` - Reuse from update_handler
- `delete_task(tasks: List[Task], task: Task) -> None` - Remove task from list
- `format_delete_success(task: Task) -> str` - Format confirmation message

**TASK-003**: Update `src/main.py`
- Import delete handler functions
- Add "delete" command routing in `main()`
- Add `handle_delete(args) -> int` function

**TASK-004**: Update `tests/test_add_task.py`
- Add delete handler unit tests
- Add CLI parsing tests for delete command
- Add integration tests for delete functionality

## Phase 2: Tasks Generation

Run `/speckit.tasks specs/002-delete-task` to generate the detailed task breakdown.

## Next Steps

1. Run `/speckit.tasks specs/002-delete-task` to generate tasks.md
2. Run `/speckit.implement specs/002-delete-task` to execute implementation

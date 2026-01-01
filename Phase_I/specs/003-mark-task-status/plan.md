# Implementation Plan: Mark Task Status

**Branch**: `003-mark-task-status` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-mark-task-status/spec.md`

## Summary

Enable users to mark todo tasks as complete or incomplete via CLI command `python main.py mark <task-id> --complete` or `--incomplete`. The feature validates the task ID format, verifies task existence, updates the status, and displays a confirmation message showing old and new status. Error cases (invalid ID format, non-existent task) display clear error messages without data loss.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: Python standard library (argparse, uuid, json)
**Storage**: In-memory list with JSON file persistence (TaskList class)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single Python project (CLI application)
**Performance Goals**: Status update operation completes in under 1 second
**Constraints**: Permanent status change, ID-based targeting only, mutually exclusive status flags
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
| Status limited to Incomplete/Complete | PASS | As per constitution |

**Phase 1 Re-check**: All checks still pass - design follows established patterns.

**Result**: All gates pass - no violations to track.

## Project Structure

### Documentation (this feature)

```text
specs/003-mark-task-status/
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
├── cli.py               # Add parse_mark_args(), update create_parser()
├── main.py              # Add handle_mark() function and routing
├── mark_handler.py      # NEW - is_valid_uuid(), find_task_by_id(), mark_task(), format_mark_success()
├── storage.py           # Existing TaskList class
├── task.py              # Existing Task dataclass
├── validation.py        # Existing validate_title()
├── list_handler.py      # Existing
├── update_handler.py    # Existing
├── delete_handler.py    # Existing

tests/
└── test_add_task.py     # Add mark tests (TestMark*, TestMarkCLI, TestMarkIntegration)
```

**Structure Decision**: The mark feature follows the existing handler pattern established by update_handler.py and delete_handler.py. A new `mark_handler.py` module will contain all mark-specific logic.

## Phase 0: Research

**Status**: Not required - no unknowns requiring research.

The mark feature leverages existing patterns:
- UUID validation: Already implemented in update_handler.py (is_valid_uuid)
- Task lookup: Already implemented in update_handler.py (find_task_by_id)
- Storage persistence: Already implemented in TaskList._save()
- CLI argument parsing: Follows existing patterns in cli.py
- Status field: Already exists on Task dataclass

## Phase 1: Design

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Mark handler module | Create `mark_handler.py` | Mirrors update/delete handler pattern |
| Status update method | Direct attribute assignment | Simple and efficient |
| Mutual exclusivity | argparse mutually exclusive group | Ensures user provides exactly one status |
| Return on success | Exit code 0 | Consistent with add/update/list/delete |
| Return on error | Exit code 1 | Standard error handling |
| Confirmation message | Show task title, old status, new status | Helps user verify correct task updated |

### Implementation Tasks (Phase 2)

**TASK-001**: Update `src/cli.py`
- Add `MarkTaskArgs` NamedTuple
- Add `parse_mark_args()` function with mutually exclusive --complete/--incomplete
- Add `mark` subparser to `create_parser()`

**TASK-002**: Create `src/mark_handler.py`
- `is_valid_uuid(val: str) -> bool` - Reuse from update_handler
- `find_task_by_id(tasks: List[Task], task_id: str) -> Task | None` - Reuse from update_handler
- `mark_task(task: Task, new_status: str) -> None` - Update task.status
- `format_mark_success(task: Task, old_status: str) -> str` - Format confirmation

**TASK-003**: Update `src/main.py`
- Import mark handler functions
- Add "mark" command routing in `main()`
- Add `handle_mark(args) -> int` function

**TASK-004**: Update `tests/test_add_task.py`
- Add mark handler unit tests
- Add CLI parsing tests for mark command
- Add integration tests for mark functionality

## Phase 2: Tasks Generation

Run `/speckit.tasks specs/003-mark-task-status` to generate the detailed task breakdown.

## Next Steps

1. Run `/speckit.tasks specs/003-mark-task-status` to generate tasks.md
2. Run `/speckit.implement specs/003-mark-task-status` to execute implementation

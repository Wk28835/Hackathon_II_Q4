# Implementation Plan: View Tasks

**Feature Branch**: `001-view-tasks`
**Created**: 2025-12-30
**Feature Spec**: [spec.md](./spec.md)

## Technical Context

**Architecture Type**: CLI command extending existing Add Task feature

**Dependencies**:
- Builds on `001-add-task` feature (Task dataclass, TaskList storage)
- Uses same Python CLI infrastructure (argparse)

**Display Format**: Tabular output using text table format

**Key Technical Decisions**:
- Task display: Fixed-width column table for alignment
- Filtering: Before display, filter the TaskList
- Empty state: Simple informative message

**Known Unknowns**:
- N/A - Requirements are clear and can use existing Task entity

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

This feature extends the existing Add Task implementation:

1. **Task Entity**: Reuses existing Task dataclass from 001-add-task
2. **Storage**: Reuses existing TaskList for task retrieval
3. **Display**: Uses Python string formatting for tabular output

### research.md

**Decision**: Use tabulate library or custom table formatting

**Rationale**:
- tabulate provides clean, aligned tables with minimal code
- Fallback to custom formatting if tabulate not available
- Consistent with CLI tool design patterns

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| tabulate | Clean output, feature-rich | External dependency |
| pandas | Powerful | Overkill for CLI |
| Custom f-strings | No dependency | More code to maintain |
| PrettyTable | Table-specific | External dependency |

**Sources**:
- Python CLI best practices
- tabulate PyPI documentation

---

## Phase 1: Design

### data-model.md

```python
# Reuses existing Task entity from 001-add-task
Task = {
    "id": "uuid4-string",
    "title": "string",
    "description": "string",
    "status": "Incomplete" | "Complete"
}

# Task List View (read-only representation)
TaskListView = List[Task]
```

**Validation Rules**:
- Status filtering: case-insensitive match
- Empty list: special display message
- Long text: truncate with ellipsis for display

### contracts/

No external API contracts needed - this is a CLI command extension.

### quickstart.md

```bash
# List all tasks
python main.py list

# List only incomplete tasks
python main.py list --status incomplete
python main.py list -s incomplete

# List only complete tasks
python main.py list --status complete
python main.py list -s complete

# Example output with tasks:
# ID                                    Title          Description      Status
# ------------------------------------  -------------  ---------------  ---------
# 550e8400-e29b-41d4-a716-446655440000  Buy groceries  Milk, Eggs, Bread  Incomplete

# Example output with no tasks:
# No tasks found. Add a task to get started.
```

---

## Phase 2: Implementation Tasks

### Task List

#### Phase 2.1: CLI Extension

- [ ] **TASK-001**: Update `src/cli.py` with list command
  - Add `list` subcommand to parser
  - Add `--status` / `-s` optional flag
  - Accept values: all, incomplete, complete (default: all)

#### Phase 2.2: List Handler

- [ ] **TASK-002**: Create `src/list_handler.py` for display logic
  - `format_task_table(tasks)` function
  - `format_empty_message()` function
  - `truncate_text(text, max_length)` helper
  - Column widths: ID (36), Title (15), Description (15), Status (10)

#### Phase 2.3: Main Integration

- [ ] **TASK-003**: Update `src/main.py` with list command handler
  - Initialize TaskList from existing storage
  - Apply status filter based on args
  - Route to list_handler for display

#### Phase 2.4: Testing

- [ ] **TASK-004**: Update `tests/test_add_task.py` with view tests
  - Test list command with tasks
  - Test list command with empty tasks
  - Test filtering by incomplete status
  - Test filtering by complete status
  - Test table formatting

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

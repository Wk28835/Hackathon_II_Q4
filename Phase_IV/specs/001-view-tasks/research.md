# Research: View Tasks Feature

## Overview

This document captures research findings for implementing the "View Tasks" feature.

## Task Display Format

**Decision**: Use tabulate library with fallback to custom f-string formatting

**Rationale**:
- tabulate produces clean, aligned tables with minimal code
- Falls back gracefully if library not available
- Industry-standard for CLI table display
- Supports various table formats (simple, grid, pipe)

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| tabulate | Clean output, feature-rich, simple API | External dependency |
| Custom f-strings | No dependency | More code to maintain, less consistent |
| PrettyTable | Table-specific | External dependency |
| pandas DataFrame | Powerful | Overkill, large dependency |

**Implementation**:
```python
try:
    from tabulate import tabulate
    def format_table(tasks):
        headers = ["ID", "Title", "Description", "Status"]
        rows = [[t.id, t.title, t.description, t.status] for t in tasks]
        return tabulate(rows, headers=headers, tablefmt="simple")
except ImportError:
    # Custom fallback implementation
    pass
```

---

## Status Filtering

**Decision**: Simple case-insensitive string matching

**Rationale**:
- Users expect flexible input (Incomplete, incomplete, INCOMPLETE)
- Simple implementation using `.lower()` comparison
- Maps directly to FR-003 and FR-004 requirements

**Implementation**:
```python
def filter_by_status(tasks, status_filter):
    if status_filter == "all":
        return tasks
    return [t for t in tasks if t.status.lower() == status_filter.lower()]
```

---

## Empty State Handling

**Decision**: Simple informative message without table

**Rationale**:
- Users need clear guidance when no tasks exist
- Consistent with spec requirement FR-005
- No table header needed when no data

**Message**:
```
No tasks found. Add a task to get started.
```

---

## Text Truncation

**Decision**: Truncate long text with ellipsis for readability

**Rationale**:
- Prevents terminal wrapping issues
- Preserves readability of table format
- Users can see task details elsewhere if needed

**Implementation**:
```python
def truncate(text, max_length=20):
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
```

---

## Summary

All technical decisions made based on:
- Minimal external dependencies
- User readability and experience
- Alignment with feature specification
- Maintainability of the codebase

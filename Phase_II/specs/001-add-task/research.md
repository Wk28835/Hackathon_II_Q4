# Research: Add Task Feature

## Overview

This document captures research findings for implementing the "Add Task" feature.

## Task ID Generation

**Decision**: Use Python's `uuid.uuid4()` for unique task identifiers

**Rationale**:
- `uuid4` generates random UUIDs with negligible collision probability
- Self-contained - no external dependencies needed
- String format is human-readable and easy to debug
- Meets spec requirement for "unique auto-generated ID"

**Alternatives Considered**:
| Approach | Pros | Cons |
|----------|------|------|
| UUID4 | Unique, no coordination needed | 36-char string (longer) |
| Auto-increment | Short, sequential | Loses uniqueness across restarts |
| Timestamp | Simple | Potential collisions at scale |
| Snowflake ID | Ordered, scalable | Complex implementation |

**Sources**:
- Python `uuid` module documentation
- RFC 4122 (UUID specification)

---

## Input Validation Best Practices

**Decision**: Use `str.strip()` combined with length check for title validation

**Rationale**:
- Strips leading/trailing whitespace
- Empty string after strip means invalid
- Simple, readable, no external dependencies

**Implementation**:
```python
def validate_title(title: str) -> tuple[bool, str]:
    if not title or not title.strip():
        return False, "Title must not be empty"
    return True, None
```

---

## State Management

**Decision**: Simple Python list in memory

**Rationale**:
- Meets spec requirement for "in-memory tasks list"
- No database complexity
- Fast read/write operations
- Suitable for CLI tool use case

**Structure**:
```python
tasks: list[dict] = []
# or with dataclass
tasks: list[Task] = []
```

---

## CLI Design Patterns

**Decision**: Use `argparse` (standard library) for CLI

**Rationale**:
- Built into Python standard library
- Handles argument parsing, help text, error messages
- No external dependencies required

**Command Structure**:
```bash
python main.py add "Task Title" [--description "Task description"]
```

---

## Summary

All technical decisions made based on:
- Simplicity and maintainability
- Standard library usage (minimal dependencies)
- Clear alignment with feature specification

# Research: Update Task Feature

## Overview

This document captures research findings for implementing the "Update Task" feature.

## Task Lookup by ID

**Decision**: Linear search through TaskList.tasks

**Rationale**:
- Task lists are typically small (< 100 tasks)
- Linear search is simple and maintainable
- No additional data structures needed
- Python's `uuid` module for ID validation

**Implementation**:
```python
def find_task_by_id(tasks: List[Task], task_id: str) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None
```

---

## Partial Update Logic

**Decision**: Only update fields that are explicitly provided

**Rationale**:
- Users may want to update just title or just description
- Consistent with traditional PATCH semantics
- Allows flexible update patterns

**Implementation**:
```python
def update_task(task: Task, new_title: str | None, new_description: str | None) -> None:
    if new_title is not None:
        task.title = new_title
    if new_description is not None:
        task.description = new_description
```

---

## UUID Validation

**Decision**: Use Python's `uuid` module to validate UUID format

**Rationale**:
- Built into Python standard library
- Handles all UUID versions (1, 3, 4, 5)
- Clear error messages on invalid format

**Implementation**:
```python
import uuid

def is_valid_uuid(val: str) -> bool:
    try:
        uuid.UUID(val)
        return True
    except ValueError:
        return False
```

---

## Summary

All technical decisions made based on:
- Simplicity and maintainability
- Reuse of existing patterns from Add/View tasks
- Python standard library usage
- Clear error handling for user feedback

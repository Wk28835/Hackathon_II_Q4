Feature: View Tasks
Description: Allows the user to view all todo tasks in the CLI, showing ID, title, description, and completion status.

Input:
  - No input required (list command with optional filters)

Output:
  - List of task objects with fields:
    - id: string (unique identifier)
    - title: string
    - description: string
    - status: string ("Incomplete" or "Complete")

Validation:
  - If no tasks exist, show informative message.
  - Status can be filtered (all, incomplete, complete).

Behavior:
  - Display all tasks in a formatted table or list.
  - Show task ID, title, description, and status for each task.
  - Support filtering by status (all, incomplete, complete).

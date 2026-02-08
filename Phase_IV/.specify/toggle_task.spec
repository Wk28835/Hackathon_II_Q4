Feature: Toggle Task Completion
Description: Allows the user to mark a task as complete or incomplete.

Input:
  - task_id: string
      Description: Unique identifier of the task.

Output:
  - task: object
      Description: Updated task with toggled status.

Validation:
  - Task ID must exist.

Behavior:
  - Find the task by ID in the in-memory task list.
  - If status is "Incomplete", change it to "Complete".
  - If status is "Complete", change it to "Incomplete".
  - Return a message: "Task with ID <id> marked as <status>."
  - If task does not exist, return an error message.

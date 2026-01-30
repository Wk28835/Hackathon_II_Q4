Feature: Update Task
Description: Allows the user to update the title and/or description of an existing task.

Input:
  - task_id: string
      Description: Unique identifier of the task.
  - title: string (optional)
      Description: New title for the task.
  - description: string (optional)
      Description: New description for the task.

Output:
  - task: object
      Description: Updated task object.
      Fields:
        - id: string
        - title: string
        - description: string
        - status: string

Validation:
  - Task ID must exist.
  - If title is provided, it must not be empty.

Behavior:
  - Locate the task by ID in the in-memory task list.
  - Update the provided fields only.
  - Keep existing values if fields are not provided.
  - Return a success message: "Task with ID <id> updated successfully."
  - If task does not exist, return an error message.

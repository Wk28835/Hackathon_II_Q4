Feature: Delete Task
Description: Allows the user to delete an existing task from the in-memory Todo list using its ID.

Input:
  - task_id: string
      Description: Unique identifier of the task to be deleted.

Output:
  - message: string
      Description: Confirmation or error message.

Validation:
  - Task ID must exist in the task list.
  - If the task ID does not exist, return an error message.

Behavior:
  - Search for the task by ID in the in-memory task list.
  - If found, remove the task from the list.
  - Return a success message: "Task with ID <id> deleted successfully."
  - If not found, return: "Task with ID <id> not found."

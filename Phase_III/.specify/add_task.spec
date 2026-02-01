Feature: Add Task
Description: Allows the user to add a new task to the in-memory Todo list.

Input:
  - title: string
      Description: Title of the task. Must not be empty.
  - description: string
      Description: Detailed description of the task.

Output:
  - task: object
      Fields:
        - id: string (unique auto-generated ID)
        - title: string
        - description: string
        - status: string ("Incomplete" by default)

Validation:
  - Title must not be empty. If empty, show error message.
  - Description can be empty.

Behavior:
  - Generate a unique ID for each task.
  - Add the new task to the in-memory tasks list.
  - Return a success message: "Task '<title>' added successfully with ID <id>."

Feature: View Tasks
Description: Displays all tasks currently stored in memory.

Input:
  - None

Output:
  - tasks: list
      Description: List of all tasks.
      Each task includes:
        - id
        - title
        - description
        - status

Behavior:
  - If no tasks exist, display: "No tasks available."
  - Display each task in a readable format.
  - Clearly show completion status (Complete / Incomplete).

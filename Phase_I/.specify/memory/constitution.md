# Phase I: Todo In-Memory Python Console App Constitution

## 1. Project Overview
This project is the first phase of the "Evolution of Todo" hackathon.  
It demonstrates building a simple CLI Todo application using **Spec-Driven Development** with Claude Code and Spec-Kit Plus.

**Objectives:**
- Implement all basic-level features: Add, Delete, Update, View, Mark Complete.
- Store tasks in memory (no database required).
- Follow clean code principles and proper Python project structure.
- Use spec-driven development only; **no manual coding**.

---

## 2. Coding Standards
All generated Python code must follow these standards:
- PEP8 formatting (indentation = 4 spaces).
- Meaningful variable and function names.
- Functions should follow single responsibility principle.
- Add docstrings and comments for clarity.
- No hardcoded values for task IDs; always use auto-generated unique IDs.
- Ensure error handling for invalid inputs.

---

## 3. Project Structure
The project directory should be organized as follows:


**Task object structure:**
- `id`: string (unique task identifier)
- `title`: string (task title)
- `description`: string (task description)
- `status`: string ("Incomplete" or "Complete")

---

## 4. Feature Rules
- Implement all **basic features** using **Claude Code + Spec-Kit Plus**.
- Do not write manual Python code for core features.
- Refine specifications if generated code does not meet requirements.
- All features must operate on **in-memory tasks only**.
- Ensure the CLI interface is user-friendly and clearly displays prompts and messages.

---

## 5. Development Guidelines
- Use a **Python 3.13+ virtual environment**.
- Test each feature individually before integrating.
- Implement a **CLI menu in `main.py`** to call all features.
- Maintain a backup of all spec files in `specs_history/`.
- Document how each spec is used in `CLAUDE.md`.
- Handle edge cases:
  - Adding a task with empty title → show error
  - Deleting/updating/toggling a task ID that does not exist → show error
  - Viewing an empty task list → display "No tasks available"

---

## 6. CLI Menu Guidelines
The CLI menu should have the following options:
- Each option must call the respective feature function.
- Menu should loop until user chooses Exit.
- Display informative messages for all operations.

---

## 7. Documentation
- `README.md`: Provide instructions on setting up the environment and running the app.
- `CLAUDE.md`: Document how each spec was used with Claude Code to generate Python code.
- Keep documentation updated with any changes in specs or features.

---

## 8. Task Management Guidelines
- All tasks are stored in memory using a Python list or dictionary.
- Each task must have a **unique ID** generated automatically.
- Task status can only be `"Incomplete"` or `"Complete"`.
- Functions should return meaningful messages upon success or failure.

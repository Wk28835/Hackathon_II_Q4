"""MCP tool schemas for Claude tool calling."""
TOOLS = [
    {
        "name": "list_tasks",
        "description": "List user's tasks. Optional status filter.",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["Incomplete", "Complete"],
                    "description": "Filter by status. Omit for all.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "create_task",
        "description": "Create a new task for the user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title (required)"},
                "description": {
                    "type": "string",
                    "description": "Task description (optional)",
                },
            },
            "required": ["title"],
        },
    },
    {
        "name": "update_task",
        "description": "Update an existing task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {
                    "type": "string",
                    "description": "New description (optional)",
                },
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "delete_task",
        "description": "Delete a task.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID to delete"}
            },
            "required": ["task_id"],
        },
    },
    {
        "name": "mark_task_status",
        "description": "Mark task as complete or incomplete.",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "Task ID"},
                "status": {
                    "type": "string",
                    "enum": ["Complete", "Incomplete"],
                    "description": "New status",
                },
            },
            "required": ["task_id", "status"],
        },
    },
]

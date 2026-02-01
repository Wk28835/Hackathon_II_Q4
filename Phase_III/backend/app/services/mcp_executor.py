"""MCP tool executor for Gemini tool calls."""
from typing import Any, Dict
import json
from uuid import UUID

from app.crud.task import (create_task, delete_task, list_tasks, update_task,
                           update_task_status)
from app.database import get_session


async def execute_mcp_tool(tool_call: Dict[str, Any], user_id: str) -> Any:
    """Execute MCP tool call based on tool name and return result."""
    name = tool_call.get("name")
    args = tool_call.get("arguments", {})

    try:
        # Create a new session for each tool execution
        async for session in get_session():
            if name == "list_tasks":
                status = args.get("status")
                # Handle 'all' status or None
                if status == "all":
                    status = None

                tasks = await list_tasks(session, user_id, status)
                # Convert tasks to list of dicts for JSON serialization
                task_list = [task.model_dump() for task in tasks]
                return task_list

            elif name == "create_task":
                title = args.get("title")
                if not title:
                    return {"error": "Title is required"}
                description = args.get("description", "")

                task = await create_task(session, user_id, title, description)
                return task.model_dump()

            elif name == "update_task":
                try:
                    # Gemini sends integer, but check what type it actually is
                    task_id_val = args.get("task_id")
                    if task_id_val is None:
                        return {"error": "Task ID is required"}
                    
                    # DEBUG: Log what Gemini is actually sending
                    print(f"DEBUG: Gemini sent task_id: {task_id_val}, type: {type(task_id_val)}")
                    
                    # Convert to string first to handle both int and float
                    task_id_str = str(task_id_val)
                    
                    # CRITICAL: Remove any decimal points if it's a float
                    if '.' in task_id_str:
                        task_id_str = task_id_str.split('.')[0]
                    
                    # Now try to convert to UUID or use as-is based on your DB
                    # Option A: If using UUIDs:
                    # task_id = UUID(task_id_str)
                    
                    # Option B: If using integer IDs (more likely):
                    task_id = int(task_id_str)
                        
                except ValueError as e:
                    return {"error": f"Invalid Task ID format: {str(e)}. Received: {task_id_val}"}

                # CRITICAL: Force title to string to fix the 'float' error
                title = args.get("title")
                if title is not None:
                    if isinstance(title, (int, float)):
                        title = str(int(title)) if isinstance(title, float) else str(title)
                    else:
                        title = str(title)
                
                description = args.get("description")
                if description is not None:
                    description = str(description)

                task = await update_task(session, task_id, user_id, title, description)
                if task:
                    return task.model_dump()
                return {"error": f"Task {task_id} not found"}

            elif name == "delete_task":
                try:
                    task_id_val = args.get("task_id")
                    if task_id_val is None:
                        return {"error": "Task ID is required"}
                    
                    # Convert to string first
                    task_id_str = str(task_id_val)
                    
                    # Remove decimal points if present
                    if '.' in task_id_str:
                        task_id_str = task_id_str.split('.')[0]
                    
                    # Convert to appropriate type
                    # If using UUIDs: task_id = UUID(task_id_str)
                    # If using integer IDs:
                    task_id = int(task_id_str)
                        
                except ValueError as e:
                    return {"error": f"Invalid Task ID format: {str(e)}. Received: {task_id_val}"}

                success = await delete_task(session, task_id, user_id)
                if success:
                    return {"message": f"Task {task_id} deleted successfully"}
                return {"error": f"Task {task_id} not found"}

            elif name == "mark_task_status":
                try:
                    task_id_val = args.get("task_id")
                    if task_id_val is None:
                        return {"error": "Task ID is required"}
                    
                    # Convert to string first
                    task_id_str = str(task_id_val)
                    
                    # Remove decimal points if present
                    if '.' in task_id_str:
                        task_id_str = task_id_str.split('.')[0]
                    
                    # Convert to appropriate type
                    # If using UUIDs: task_id = UUID(task_id_str)
                    # If using integer IDs:
                    task_id = int(task_id_str)
                        
                except ValueError as e:
                    return {"error": f"Invalid Task ID format: {str(e)}. Received: {task_id_val}"}

                status = args.get("status")
                if status not in ["complete", "incomplete"]:
                    return {"error": "Status must be 'complete' or 'incomplete'"}

                task = await update_task_status(session, task_id, user_id, status)
                if task:
                    return task.model_dump()
                return {"error": f"Task {task_id} not found"}

    except Exception as e:
        return {"error": f"Tool execution failed: {str(e)}"}
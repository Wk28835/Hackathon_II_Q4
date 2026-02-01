"""Gemini API integration for Todo AI Chatbot."""
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from fastapi.encoders import jsonable_encoder

from app.config import settings


def initialize_gemini_client():
    """Initialize Gemini client with API key."""
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY not configured in environment")

    genai.configure(api_key=settings.gemini_api_key)
    return genai


# Define MCP tools for Gemini function calling
MCP_TOOLS = [
    {
        "name": "list_tasks",
        "description": "List all tasks for the current user. Optional status filter can be 'incomplete', 'complete', or 'all'.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["incomplete", "complete", "all"],
                    "description": "Filter tasks by status"
                }
            },
            "required": []
        }
    },
    {
        "name": "create_task",
        "description": "Create a new task for the current user",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title of the task"},
                "description": {"type": "string", "description": "Optional description"}
            },
            "required": ["title"]
        }
    },
    {
    "name": "update_task",
    "description": "Update an existing task by its integer ID",
    "parameters": {
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",  # Change from string to integer
                "description": "The exact numeric integer ID of the task. Do not use decimals.)"
            },
            "title": {"type": "string"},
            "description": {"type": "string"}
        },
        "required": ["task_id"]
    }
},
    {
        "name": "delete_task",
        "description": "Delete a task by its integer ID",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer", # Change from string to integer
                    "description": "The exact numeric integer ID of the task. Do not use decimals."
                }
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "mark_task_status",
        "description": "Mark a task as complete or incomplete using its integer ID",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer", # Change from string to integer
                    "description": "The exact numeric integer ID of the task. Do not use decimals."
                },
                "status": {
                    "type": "string",
                    "enum": ["complete", "incomplete"]
                }
            },
            "required": ["task_id", "status"]
        }
    }
]


def get_gemini_tools():
    """Convert MCP tools to Gemini function declarations."""
    return [genai.types.FunctionDeclaration(**tool) for tool in MCP_TOOLS]


class GeminiService:
    """Service for interacting with Gemini API with function calling."""

    def __init__(self):
        self.primary_model_name = "gemini-2.5-flash"
        self.fallback_model_name = "gemini-2.5-flash-lite"
        self.client = None
        
        try:
            self.client = initialize_gemini_client()
            # Initialize both models to avoid delay during failover
            self.primary_model = self._create_model(self.primary_model_name)
            self.fallback_model = self._create_model(self.fallback_model_name)
        except Exception as e:
            print(f"Warning: Gemini Service initialization failed: {e}")
            self.primary_model = None

    def _create_model(self, model_name: str):
        """Helper to create a model instance with standard config."""
        return genai.GenerativeModel(
            model_name=model_name,
            tools=get_gemini_tools(),
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            },
            safety_settings=[
                {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
                {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_NONE},
                {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_NONE},
                {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
            ]
        )

    def format_messages_for_gemini(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        gemini_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            f_call = msg.get("function_call")
            f_resp = msg.get("function_response")

            if role == "function":
                if f_resp:
                    # Gemini expects: {"name": "...", "response": {"content": ...}}
                    gemini_messages.append({
                        "role": "function",
                        "parts": [{
                            "function_response": {
                                "name": f_resp.get("name"),
                                "response": f_resp.get("response") if isinstance(f_resp.get("response"), dict) else {"content": f_resp.get("response")}
                            }
                        }]
                    })
            elif role == "assistant":
                parts = []
                if content: parts.append({"text": content})
                if f_call:
                    parts.append({
                        "function_call": {
                            "name": f_call["name"],
                            "args": jsonable_encoder(f_call["arguments"])
                        }
                    })
                if parts: gemini_messages.append({"role": "model", "parts": parts})
            else:  # user
                gemini_messages.append({"role": "user", "parts": [{"text": content}]})
        return gemini_messages

    async def generate_chat_response(
            self,
            messages: List[Dict[str, Any]]
        ) -> Dict[str, Any]:
            """Generate chat response with automatic fallback if quota exceeded."""
            if not self.primary_model:
                return {"content": "Gemini service is not available."}

            # Attempt with Primary Model first
            try:
                return await self._execute_request(self.primary_model, messages)
            except Exception as e:
                error_str = str(e).lower()
                # Check for Quota (429) or Server Errors (500, 503)
                if "429" in error_str or "quota" in error_str or "503" in error_str:
                    print(f"Primary model ({self.primary_model_name}) limit reached. Falling back to {self.fallback_model_name}...")
                    try:
                        return await self._execute_request(self.fallback_model, messages)
                    except Exception as fallback_error:
                        raise Exception(f"Fallback model also failed: {str(fallback_error)}")
                
                # If it's a different kind of error (like logic error), just raise it
                raise Exception(f"Gemini API error: {str(e)}")

    async def _execute_request(self, model: genai.GenerativeModel, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
            """Core logic to send request and parse response."""
            history = self.format_messages_for_gemini(messages[:-1])
            chat = model.start_chat(history=history)
            
            last_msg = messages[-1]
            prompt = last_msg.get("content") or " "
            
            response = chat.send_message(prompt)

            function_calls = []
            text_content = ""

            for part in response.parts:
                if hasattr(part, "function_call") and part.function_call:
                    function_calls.append({
                        "name": part.function_call.name,
                        "arguments": jsonable_encoder(dict(part.function_call.args))
                    })
                elif hasattr(part, "text") and part.text:
                    text_content += part.text

            return {
                "content": text_content,
                "function_calls": function_calls if function_calls else None,
                "raw_response": str(response)
            }

    def create_function_response_message(self, function_name: str, result: Any) -> Dict[str, Any]:
        """Create a function response message for Gemini."""
        clean_result = jsonable_encoder(result)
        return {
            "role": "function",
            "content": json.dumps(clean_result), 
            "function_response": {
                "name": function_name,
                "response": {"content": clean_result}
            }
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        return MCP_TOOLS


# Create global instance
gemini_service = GeminiService()
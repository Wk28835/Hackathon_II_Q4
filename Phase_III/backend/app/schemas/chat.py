"""Pydantic schemas for Todo AI Chatbot with Gemini function calling."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.chat import Conversation, Message


class ConversationCreate(BaseModel):
    title: str = Field(..., max_length=255)

class ConversationRead(BaseModel):
    id: UUID
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    role: str = Field(..., max_length=20)  # 'user', 'assistant', 'function'
    content: str = Field(..., max_length=4000)
    function_call: Optional[Dict[str, Any]] = Field(None)
    function_response: Optional[Dict[str, Any]] = Field(None)


class MessageRead(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    function_call: Optional[Dict[str, Any]]
    function_response: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class MessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    tools_enabled: bool = Field(default=True)


class ConversationListResponse(BaseModel):
    id: UUID
    title: str
    preview: str = Field(..., max_length=100)
    updated_at: datetime
    unread: bool = Field(default=False)


class ChatResponse(BaseModel):
    message_id: UUID
    content: str
    function_calls: Optional[List[Dict[str, Any]]] = Field(None)
    function_responses: Optional[List[Dict[str, Any]]] = Field(None)


class ToolRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    arguments: Dict[str, Any] = Field(default_factory=dict)

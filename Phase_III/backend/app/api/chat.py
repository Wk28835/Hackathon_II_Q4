"""Chat API endpoints for Todo AI Chatbot with Gemini."""
from typing import List, Optional
from uuid import UUID

from fastapi.encoders import jsonable_encoder
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.database import get_session
from app.schemas.chat import (
    ConversationCreate,
    ConversationRead,
    ChatResponse,
    MessageRequest,
    ConversationListResponse,
    MessageRead
)
from app.crud.chat import (
    create_conversation,
    get_conversation_history,
    add_message,
    get_conversation,
    get_user_conversations,
    get_conversation_preview
)
from app.services.gemini_service import gemini_service
from app.services.mcp_executor import execute_mcp_tool

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationRead)
async def create_chat_conversation(
    conversation_create: ConversationCreate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new conversation."""
    conversation = await create_conversation(session, current_user_id, conversation_create.title)
    return conversation


@router.get("/conversations", response_model=List[ConversationListResponse])
async def list_conversations(
    limit: int = 20,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """List all conversations for the current user."""
    conversations = await get_user_conversations(session, current_user_id, limit)

    response = []
    for conv in conversations:
        preview = await get_conversation_preview(session, conv)
        response.append(ConversationListResponse(
            id=conv.id,
            title=conv.title,
            preview=preview,
            updated_at=conv.updated_at,
            unread=False  # TODO: Implement unread status tracking
        ))

    return response


@router.get("/{conversation_id}/messages", response_model=List[MessageRead])
async def get_messages(
    conversation_id: UUID,
    limit: int = 50,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get conversation history."""
    # Verify access first
    conversation = await get_conversation(session, current_user_id, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    messages = await get_conversation_history(session, conversation_id, current_user_id, limit)
    return messages


@router.post("/{conversation_id}/messages", response_model=ChatResponse)
async def send_chat_message(
    conversation_id: UUID,
    message_request: MessageRequest,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Send message to conversation and get AI response."""
    # Add user message
    try:
        user_message = await add_message(
            session=session,
            conversation_id=conversation_id,
            role="user",
            content=message_request.message,
            user_id=current_user_id
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

    # Get history for context
    history = await get_conversation_history(session, conversation_id, current_user_id)

    # Convert SQLModel messages to dicts for service
    history_dicts = []
    for msg in history:
        msg_dict = {
            "role": msg.role,
            "content": msg.content,
            "function_call": msg.function_call,
            "function_response": msg.function_response
        }
        history_dicts.append(msg_dict)

    # Call Gemini service
    try:
        gemini_response = await gemini_service.generate_chat_response(
            messages=history_dicts,
        #    tools_enabled=message_request.tools_enabled
        )
    except Exception as e:
        # Log error and return error message to user
        # In a real app, we might want to retry or handle specific errors
        error_msg = f"I encountered an error processing your request: {str(e)}"
        ai_message = await add_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content=error_msg,
            user_id=current_user_id
        )
        return ChatResponse(
            message_id=ai_message.id,
            content=error_msg
        )

    # Check for function calls
    function_calls = gemini_response.get("function_calls")

    if function_calls:
        ai_content = gemini_response.get("content") or "Processing..."
        
        tool_results = []
        
        for call in function_calls:
            # 1. Execute the tool (this returns a Task object with datetimes)
            result = await execute_mcp_tool(call, current_user_id)
            
            def clean_data(data):
                if isinstance(data, dict):
                    return {k: str(v) if v is not None else None for k, v in data.items()}
                return str(data) if data is not None else None
    
            # 2. CONVERT TO JSON-SAFE DATA (The Fix)
            # This turns datetimes into strings and objects into dicts
            clean_result = clean_data(result)

            tool_results.append({"name": call["name"], "result": clean_result})

            # 3. Save assistant message (the intent to call a function)
            await add_message(
                session=session,
                conversation_id=conversation_id,
                role="assistant",
                content=json.dumps(clean_result), 
                function_response={
                        "name": call["name"], 
                        "response": {"content": clean_result} # Match the service change
                    }, # Safe for JSON column
                user_id=current_user_id
            )

            # 4. Save function response (the result of the tool)
            await add_message(
                session=session,
                conversation_id=conversation_id,
                role="function",
                content=json.dumps(clean_result), # Safe for VARCHAR column
                function_response={
                    "name": call["name"], 
                    "response": clean_result # Safe for JSON column
                },
                user_id=current_user_id
            )

        # 5. Get the final response from Gemini (History now contains only strings)
        updated_history = await get_conversation_history(session, conversation_id, current_user_id)
        
        # Convert history objects to dicts for Gemini
        history_dicts = []
        for msg in updated_history:
            history_dicts.append({
                "role": msg.role,
                "content": msg.content,
                "function_call": msg.function_call,
                "function_response": msg.function_response
            })

        # Call Gemini again for final answer (Note: no tools_enabled argument)
        final_response = await gemini_service.generate_chat_response(
            messages=history_dicts
        )

        final_content = final_response.get("content", "I completed the action.")

        # Save final AI response
        final_msg = await add_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content=final_content,
            user_id=current_user_id
        )

        return ChatResponse(
            message_id=final_msg.id,
            content=final_msg.content,
            function_calls=function_calls,
            function_responses=tool_results
        )

    else:
        # No function calls, just a text response
        content = gemini_response.get("content", "")

        ai_message = await add_message(
            session=session,
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            user_id=current_user_id
        )

        return ChatResponse(
            message_id=ai_message.id,
            content=content
        )
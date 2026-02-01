"""CRUD operations for chat conversations and messages with Gemini function calling."""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import Conversation, Message


async def create_conversation(session: AsyncSession, user_id: str, title: str) -> Conversation:
    """Create a new conversation for the user."""
    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation_history(session: AsyncSession, conversation_id: UUID, user_id: str, limit: int = 50) -> List[Message]:
    """Get conversation history for the authenticated user (most recent messages)."""
    # Join with Conversation to filter by user_id
    stmt = select(Message).join(Conversation).where(
        Message.conversation_id == conversation_id,
        Conversation.user_id == user_id
    ).order_by(Message.created_at.desc()).limit(limit)

    result = await session.execute(stmt)
    messages = result.scalars().all()
    return messages[::-1]  # Reverse to chronological order


async def add_message(
    session: AsyncSession,
    conversation_id: UUID,
    role: str,
    content: str,
    function_call: Optional[Dict[str, Any]] = None,
    function_response: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None
) -> Message:
    """Add a message to the conversation (user isolation via conversation owner check)."""
    # Verify conversation ownership
    conversation_stmt = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
    result = await session.execute(conversation_stmt)
    conversation = result.scalars().first()

    if not conversation:
        raise ValueError("Conversation not found or unauthorized")

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        function_call=function_call,
        function_response=function_response,
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)

    # Update conversation updated_at
    conversation.updated_at = message.created_at
    session.add(conversation)
    await session.commit()
    return message


async def get_conversation(session: AsyncSession, user_id: str, conversation_id: UUID) -> Conversation:
    """Get a specific conversation for a user."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_conversations(session: AsyncSession, user_id: str, limit: int = 20) -> List[Conversation]:
    """Get all conversations for a user with preview and unread status."""
    stmt = select(Conversation).where(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc()).limit(limit)

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_conversation_preview(session: AsyncSession, conversation: Conversation) -> str:
    """Get preview text for a conversation (last message content)."""
    stmt = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.desc()).limit(1)

    result = await session.execute(stmt)
    last_message = result.scalars().first()

    if not last_message:
        return "No messages yet"

    # Truncate for preview
    preview = last_message.content
    if len(preview) > 100:
        preview = preview[:97] + "..."

    return preview
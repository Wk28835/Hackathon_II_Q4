"""Test utilities for chat tests."""
import uuid


async def create_sample_conversation(session, user_id: str):
    """Create a sample conversation for testing."""
    from app.models.chat import Conversation

    conversation = Conversation(user_id=user_id, title="Test Conversation")
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation.id


async def add_sample_messages(session, conversation_id: uuid.UUID, count: int = 3):
    """Add sample messages to conversation."""
    from app.models.chat import Message

    for i in range(count):
        message = Message(
            conversation_id=conversation_id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Sample message {i}",
        )
        session.add(message)
    await session.commit()

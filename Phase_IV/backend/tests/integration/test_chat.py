"""Integration tests for chat functionality."""

from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_debug_routes(client: AsyncClient):
    """Debug routes."""
    from app.main import app

    for route in app.routes:
        print(f"Route: {route.path} {route.methods}")

    # Also check health
    resp = client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient, auth_headers):
    """Test creating a new conversation."""
    response = client.post(
        "/api/chat/conversations",
        headers=auth_headers,
        json={"title": "Test Chat"},
    )
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Chat"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_conversation_unauthorized(client: AsyncClient):
    """Test creating conversation without auth."""
    response = client.post(
        "/api/chat/conversations",
        json={"title": "Test Chat"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_send_message(client: AsyncClient, auth_headers):
    """Test sending a message and getting AI response."""
    # Create conversation first
    create_resp = client.post(
        "/api/chat/conversations",
        headers=auth_headers,
        json={"title": "Test Chat"},
    )
    conversation_id = create_resp.json()["id"]

    # Mock Claude API
    with patch("app.api.chat.client") as mock_client:
        # Mock message response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello! How can I help you?")]
        mock_response.tool_calls = None
        mock_client.messages.create.return_value = mock_response

        response = client.post(
            f"/api/chat/{conversation_id}/messages",
            headers=auth_headers,
            json={"role": "user", "content": "Hi"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) >= 2
        assert data["messages"][-2]["role"] == "user"
        assert data["messages"][-2]["content"] == "Hi"
        assert data["messages"][-1]["role"] == "assistant"
        assert data["messages"][-1]["content"] == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_user_isolation(client: AsyncClient, auth_headers, other_auth_headers):
    """Test that users cannot access others' conversations."""
    # User 1 creates conversation
    create_resp = client.post(
        "/api/chat/conversations",
        headers=auth_headers,
        json={"title": "User 1 Chat"},
    )
    conversation_id = create_resp.json()["id"]

    # User 2 tries to send message
    response = client.post(
        f"/api/chat/{conversation_id}/messages",
        headers=other_auth_headers,
        json={"role": "user", "content": "Spying"},
    )
    # Should be 404 (not found) or 403. Current impl filters by user_id in get/add so mostly likely raise Error or return 404-like
    # Current add_message raises ValueError if not found/unauthorized.
    # API endpoints don't catch ValueError explicitly (500).
    # We should update CRUD to maybe return None or API to handle it.
    # Let's check api implementation.

    # In api.chat:
    # user_message = await add_message(...)
    # add_message verifies ownership and raises ValueError("Conversation not found or unauthorized").
    # FastAPI default exception handler returns 500 for unhandled exceptions.
    # We should update API to handle ValueError -> 404/403.

    # In api.chat, we catch ValueError and return 404
    assert response.status_code == 404

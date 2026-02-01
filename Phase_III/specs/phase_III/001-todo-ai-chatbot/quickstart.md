# Quickstart: Todo AI Chatbot

## Backend Extension

1. Add chat models to backend/app/models/chat.py
2. Add crud/chat.py
3. Add api/chat.py endpoints
4. uvicorn app.main:app --reload

## Test Chat

```bash
# Create conversation
curl -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Daily planning"}' \
  http://localhost:8000/api/chat/conversations

# Send message
curl -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"message": "List my incomplete tasks"}' \
  http://localhost:8000/api/chat/<conversation_id>/messages
```

Expected response: AI lists tasks using MCP tools.
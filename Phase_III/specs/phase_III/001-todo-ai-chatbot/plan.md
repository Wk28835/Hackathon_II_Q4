# Implementation Plan: Todo AI Chatbot

## Technical Context

**Feature Scope**: Extend Phase II backend with stateless chat API. Frontend unchanged. AI chatbot uses MCP tools (Claude Code tools: Read, Edit, Bash for task ops) exclusively for task interaction. Conversation/Message models added to Postgres.

**Dependencies**:
- Phase II backend (FastAPI)
- Claude API (Opus 4.5)
- MCP tools (Claude Code CLI tools)
- Neon Postgres (add Conversation, Message tables)

**Integrations**:
- Backend: Claude API proxy with tool injection
- Database: Extend with chat models
- Auth: Reuse Phase II JWT

**Unknowns**:
- Exact MCP tool definitions for task CRUD (use Read/Edit for tasks.json or DB?)
- Claude API tool calling format for MCP
- Conversation context length limit

## Constitution Check

**Spec-Driven**: ✅ spec.md complete, validated
**Security-First**: ✅ User isolation via JWT
**Clean Separation**: ✅ Backend API only
**Stateless Backend**: ✅ Conversation ID retrieves context from DB
**No Manual Code**: ✅ Claude Code only
**Testing Required**: ✅ Unit + integration planned

**GATES PASSED**: Proceed.

## Phase 0: Research Summary

**MCP Tools**: Claude Code tools (Read, Edit, Write, Bash). For tasks: Edit backend DB via Edit tool or Bash for pytest.

**Claude Tool Calling**: JSON schema tools in prompt. Backend sends user message + history + tools to Claude, parses tool_calls, executes via MCP, feeds back.

**Stateless Chat**: REST POST /api/chat with conversation_id, message, JWT. Retrieve history, call Claude, store response.

## Phase 1: Data Model

**Conversation**:
- id: UUID PK
- user_id: VARCHAR FK (Phase II user)
- title: VARCHAR (AI generated)
- created_at, updated_at: TIMESTAMP

**Message**:
- id: UUID PK
- conversation_id: UUID FK
- role: ENUM ('user', 'assistant', 'tool')
- content: TEXT
- tool_calls: JSONB (MCP calls)
- created_at: TIMESTAMP

## Phase 2: API Contracts

**POST /api/chat/conversations**
- Body: {title: str}
- Response: {conversation_id: UUID}
- Auth: JWT

**POST /api/chat/{conversation_id}/messages**
- Body: {message: str}
- Response: {messages: [Message], conversation: Conversation}
- Auth: JWT

OpenAPI in contracts/openapi.yaml.

## Phase 3: Backend Implementation

1. Add models/conversation.py, schemas/chat.py
2. crud/chat.py (create_conversation, add_message, get_history)
3. api/chat.py (endpoints)
4. Integrate Claude API with tool schema for MCP
5. Execute tool calls via subprocess Claude Code CLI

## Quickstart.md

```bash
# Backend
uvicorn app.main:app --reload

# Test chat
curl -H "Authorization: Bearer <jwt>" POST /api/chat/conversations -d '{"title": "Daily tasks"}'
curl -H "Authorization: Bearer <jwt>" POST /api/chat/{id}/messages -d '{"message": "List my tasks"}'
```

**Ready for implementation.**
# Todo AI Chatbot - Gemini Integration

## User Scenarios & Testing

**Primary User Flow**:
1. User authenticates and starts a conversation with the AI chatbot.
2. User asks natural language questions about their tasks (e.g., "What tasks do I have?", "Create a task to buy milk", "Mark task #3 complete").
3. Gemini AI responds conversationally while using MCP tools to query/modify tasks.
4. Conversation context is preserved across messages within the same session.
5. User ends conversation or starts a new one.

**Edge Cases**:
- User asks about tasks belonging to other users → AI responds "I can only manage your tasks".
- Invalid task operations → AI explains error and suggests corrections.
- Empty task list → AI responds "You have no tasks. Would you like to create one?".
- Long conversations → Context maintained up to 50 recent messages.

**Acceptance Testing**:
- 10 test conversations covering CRUD operations.
- Verify AI never directly modifies database (only via MCP tools).
- Verify statelessness: Restart server, resume conversation via ID → same context.
- Validate Gemini API integration and tool calling functionality.

## Functional Requirements

1. **Conversation Initiation**: Users can start new conversations via API.
2. **Message Exchange**: Users send messages; Gemini AI responds using conversation history and tool calling.
3. **Gemini Tool Calling**: Gemini AI exclusively uses MCP tools for all task operations (list, create, update, delete, status) via function calling capabilities.
4. **Context Preservation**: Conversation state stored in database (last 50 messages as system/user/assistant messages).
5. **User Isolation**: AI only accesses tasks owned by the authenticated user via user-scoped MCP tools.
6. **Stateless Server**: Server requires conversation ID; retrieves full context from DB.
7. **Error Handling**: Gemini gracefully handles MCP tool errors, explains to users.
8. **Gemini API Integration**: Use Google Generative AI SDK with function calling capabilities.

## Success Criteria

- Users complete task operations via chat in <10 seconds per operation.
- 95% of natural language task requests correctly mapped to MCP tool calls.
- Conversation context accurate for 100% of sessions up to 50 messages.
- Server restart causes 0 data loss (stateless verified).
- AI correctly denies 100% of cross-user task requests.
- Chat API latency <2 seconds for 99th percentile response.
- Gemini API integration stable with fallback error handling.

## Key Entities

**Conversation**:
- id: UUID (primary key)
- user_id: string (foreign key to authenticated user)
- title: string (auto-generated from first message)
- created_at: timestamp
- updated_at: timestamp

**Message**:
- id: UUID (primary key)
- conversation_id: UUID (foreign key)
- role: "user" | "assistant" | "function"
- content: text
- function_call: JSON (function name and arguments)
- function_response: JSON (function execution result)
- created_at: timestamp

## Gemini Agent Architecture

### 1. Gemini Model Configuration
- **Model**: gemini-1.5-pro (supports function calling)
- **SDK**: google-generativeai (Python)
- **API Key**: GEMINI_API_KEY from environment
- **Tool Calling**: Function declarations for MCP tools
- **Context Window**: Up to 50 messages (truncation strategy)

### 2. Stateless Chat API Design
```typescript
// Request
POST /api/chat/{conversation_id}/messages
{
  "message": "What are my pending tasks?",
  "tools_enabled": true // Enable MCP tool calling
}

// Response
{
  "message_id": "uuid",
  "content": "You have 3 pending tasks: ...",
  "tools_used": [{"name": "list_tasks", "args": {}}]
}
```

### 3. MCP Tool Invocation Flow
1. User sends message
2. Backend retrieves conversation history + available MCP tools
3. Gemini generates response with function calls
4. System executes function calls (MCP tools)
5. Function responses sent back to Gemini
6. Gemini generates final response
7. Complete message chain stored in DB

### 4. Gemini Tool Schema
```python
MCP_TOOLS = [
    {
        "name": "list_tasks",
        "description": "List all tasks for the current user",
        "parameters": {"type": "object", "properties": {"status": {"type": "string"}}}
    },
    {
        "name": "create_task",
        "description": "Create a new task for the current user",
        "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}}}
    }
    # ... other task operations
]
```

## Frontend Chatbot UI Components

### Required Routes
- `/chat` - Main chat interface
- `/chat/[id]` - Individual conversation view

### UI Components
1. **ChatContainer**: Main wrapper with conversation list sidebar
2. **MessageList**: Scrollable message display with user/assistant bubbles
3. **InputBox**: Message input with tool status indicators
4. **ConversationSidebar**: List of conversations with timestamps
5. **ToolCallIndicator**: Shows when MCP tools are being executed

### Message Schema (Frontend ↔ Backend)
```typescript
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'function';
  content: string;
  timestamp: string;
  function_call?: {
    name: string;
    args: Record<string, any>;
  };
  function_response?: {
    name: string;
    result: any;
    error?: string;
  };
}

interface ChatConversation {
  id: string;
  title: string;
  preview: string;
  updated_at: string;
  unread: boolean;
}
```

## Security & Isolation

- **User Context**: Each conversation includes user_id for data isolation
- **Tool Execution**: MCP tools receive authenticated user context
- **Rate Limiting**: Gemini API calls and chat operations
- **Input Validation**: Sanitize user messages and tool parameters

## Assumptions

- User authentication handled by Phase II backend (JWT token provides user_id).
- MCP tools available via standard interface (list_tasks, create_task, etc.).
- Conversation history limited to 50 messages (older archived or summarized).
- Gemini model capable of function calling and conversation memory.
- All task operations routed exclusively through MCP tools (no direct DB access).
- GEMINI_API_KEY available in environment variables for backend.

## Phase III Status
**IN PROGRESS** - Gemini integration pending implementation
**NOT COMPLETE** - Awaiting backend and frontend changes
# Data Model: Todo AI Chatbot

## Conversation Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Conversation ID |
| user_id | VARCHAR(64) | FK (users.id), NOT NULL | Owner |
| title | VARCHAR(255) | NOT NULL | Auto-generated |
| created_at | TIMESTAMP | NOT NULL, default now() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, default now() | Last message time |

## Message Table

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Message ID |
| conversation_id | UUID | FK (conversations.id), NOT NULL | Parent conversation |
| role | ENUM('user','assistant','tool') | NOT NULL | Sender |
| content | TEXT | NOT NULL | Message text |
| tool_calls | JSONB | NULL | MCP tool calls |
| created_at | TIMESTAMP | NOT NULL, default now() | Timestamp |

Indexes:
- conversation_id
- (conversation_id, created_at DESC)
# Task Breakdown: Todo AI Chatbot

## Phase 1: Setup (5 tasks)

- [ ] T001 Create chat directory structure backend/app/chat/
- [ ] T002 Add chat models to backend/app/models/chat.py
- [ ] T003 Add chat schemas to backend/app/schemas/chat.py
- [ ] T004 Create backend/app/crud/chat.py
- [ ] T005 Add chat router backend/app/api/chat.py

## Phase 2: Foundational (8 tasks)

- [ ] T006 [P] Implement Claude API integration backend/app/services/claude.py
- [ ] T007 [P] Define MCP tool schemas backend/app/services/mcp_tools.py
- [ ] T008 [P] Implement MCP tool executor backend/app/services/mcp_executor.py
- [ ] T009 Update alembic migration for chat tables backend/alembic/versions/add_chat_tables.py
- [ ] T010 Add chat endpoints to main router backend/app/main.py
- [ ] T011 Configure Claude API key in backend/app/config.py
- [ ] T012 Add chat pytest fixtures backend/tests/conftest.py
- [ ] T013 Add chat test utils backend/tests/utils/chat.py

## Phase 3: Conversation Initiation (US1) (6 tasks)

- [ ] T014 [US1] Implement create_conversation backend/app/crud/chat.py
- [ ] T015 [US1] Implement POST /api/chat/conversations backend/app/api/chat.py
- [ ] T016 [US1] Add create_conversation tests backend/tests/integration/test_chat.py
- [ ] T017 [US1] Validate conversation creation response
- [ ] T018 [US1] Test user isolation for conversation creation
- [ ] T019 [US1] Log conversation creation events

## Phase 4: Message Exchange (US2) (12 tasks)

- [ ] T020 [US2] Implement get_conversation_history backend/app/crud/chat.py
- [ ] T021 [US2] Implement add_message backend/app/crud/chat.py
- [ ] T022 [US2] Implement POST /api/chat/{id}/messages backend/app/api/chat.py
- [ ] T023 [US2] Integrate Claude API call backend/app/services/claude.py
- [ ] T024 [US2] Parse Claude tool calls backend/app/services/mcp_executor.py
- [ ] T025 [US2] Execute MCP tools and feed back to Claude backend/app/services/mcp_executor.py
- [ ] T026 [US2] Store assistant response and tool calls backend/app/crud/chat.py
- [ ] T027 [US2] Add message exchange tests backend/tests/integration/test_chat.py
- [ ] T028 [US2] Test context preservation (50 message limit)
- [ ] T029 [US2] Test stateless resumption (conversation_id only)
- [ ] T030 [US2] Test error handling for Claude API failures
- [ ] T031 [US2] Limit context to 50 recent messages backend/app/crud/chat.py

## Phase 5: User Isolation & Error Handling (US5, US7) (8 tasks)

- [ ] T032 [US5] Add user_id filtering to get_history backend/app/crud/chat.py
- [ ] T033 [US5] Test cross-user conversation access denied backend/tests/security/test_chat.py
- [ ] T034 [US7] Handle MCP tool errors gracefully backend/app/services/mcp_executor.py
- [ ] T035 [US7] AI explain tool errors to user backend/app/services/claude.py
- [ ] T036 [US7] Test invalid MCP tool responses backend/tests/integration/test_chat.py
- [ ] T037 [US5] 403 for unauthorized conversation access backend/app/api/chat.py
- [ ] T038 [US7] Graceful degradation if Claude unavailable
- [ ] T039 [US7] Rate limiting on chat endpoints backend/app/api/chat.py

## Phase 6: Polish & Testing (10 tasks)

- [ ] T040 Add chat logging middleware backend/app/middleware/chat_logging.py
- [ ] T041 [P] Add performance tests backend/tests/performance/test_chat.py
- [ ] T042 [P] Add security tests backend/tests/security/test_chat_auth.py
- [ ] T043 Update OpenAPI docs backend/app/api/chat.py
- [ ] T044 Add chat to Alembic migration script backend/alembic/versions/
- [ ] T045 Create chat quickstart backend/docs/chat.md
- [ ] T046 Update main README.md with chat section
- [ ] T047 Add chat env vars to .env.example
- [ ] T048 Run full pytest suite backend/tests/
- [ ] T049 Verify statelessness (restart server, resume chat)

**Total Tasks**: 49
**Parallel Opportunities**: 12 [P] tasks identified
**MVP Scope**: Phase 1-3 (basic chat works)
**Independent Test Criteria**: Each US has dedicated test tasks

**Implementation Strategy**: MVP first (basic message exchange), then polish. Backend-only extension of Phase II.
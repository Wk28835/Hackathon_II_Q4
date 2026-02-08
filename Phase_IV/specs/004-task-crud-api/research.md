# Research: Task CRUD API Implementation Analysis

**Feature**: Authenticated, user-scoped Task CRUD API
**Date**: 2026-01-10
**Phase**: Phase 0 - Technical Research & Decisions

---

## Executive Summary

This document consolidates research findings and technical decisions for the Task CRUD API backend. All design choices align with Phase II Constitution principles and specification requirements. No unresolved clarifications remain.

---

## Technology Stack Research

### FastAPI Selection

**Decision**: Use FastAPI as the web framework

**Why Chosen**:
- Phase II Constitution mandates "FastAPI. Business logic, API layer, and authorization enforcement."
- Explicit requirement in Constitution §3.1 Architectural Principles
- Native async support for concurrent request handling
- Built-in OpenAPI/Swagger documentation generation
- Dependency injection system ideal for JWT verification

**Alternatives Considered**:
- Django REST Framework: Heavier, batteries-included, but violates Constitution specificity
- Flask: Too minimal for security requirements
- Starlette: Lower-level alternative to FastAPI (not recommended)

**Implementation Impact**: Core web framework, all routing uses FastAPI decorators, dependency injection for auth

---

### SQLModel + SQLAlchemy Selection

**Decision**: Use SQLModel ORM with SQLAlchemy Core

**Why Chosen**:
- Phase II Constitution mandates "SQLModel ORM" for database access
- SQLModel provides both ORM capabilities AND Pydantic validation in single model class
- Excellent integration with FastAPI for automatic schema generation
- SQLAlchemy maturity and robustness
- Supports PostgreSQL-specific features (UUIDs, JSON, etc.)

**Alternatives Considered**:
- Pure SQLAlchemy without Pydantic: Requires separate validation layer
- Tortoise ORM: Less mature, limited FastAPI integration
- Raw psycopg2: Violates "use ORM" requirement

**Implementation Impact**:
- Single model class serves as SQLAlchemy table + Pydantic validator
- Task model defines all fields, types, and validation rules
- Database migrations via Alembic (optional, schema-first approach acceptable)

---

### PostgreSQL with Neon Serverless

**Decision**: Use Neon Serverless PostgreSQL (provided)

**Why Chosen**:
- Phase II Constitution mandates "Neon Serverless PostgreSQL (SQLModel ORM)"
- Serverless architecture matches cloud-first deployment model
- No infrastructure management required
- Supports connection pooling (critical for concurrent requests)
- Scales automatically with demand

**Alternatives Considered**:
- Self-managed PostgreSQL: More operational overhead
- MySQL/MariaDB: Violates Constitution requirement
- NoSQL (MongoDB, DynamoDB): Violates relational constraint

**Implementation Impact**:
- Connection pooling via SQLModel session management
- Async connection handling for concurrent requests
- DATABASE_URL environment variable points to Neon instance
- Schema: users table (managed by Frontend), tasks table (owned by backend)

---

### JWT Authentication with python-jose

**Decision**: Use python-jose for JWT verification

**Why Chosen**:
- Phase II Constitution mandates "JWT-based identity verification"
- Shared secret (`BETTER_AUTH_SECRET`) used by both Frontend and Backend
- No database lookups required (stateless)
- Signature verification proves token authenticity
- Standard cryptographic practices (HMAC-SHA256)

**Alternatives Considered**:
- PyJWT: Similar capability, python-jose has better async support
- cryptography library directly: Lower-level, more code required

**Implementation Impact**:
- Dependency injection function `get_current_user()` in each protected endpoint
- Token claims parsed: `sub` claim extracted as user_id
- 401 Unauthorized returned for invalid/missing tokens
- No session database needed

---

## Authentication & Authorization Pattern

**Decision**: JWT signature verification + user_id extraction

**Research Findings**:
1. **Token Issuance**: Frontend (Better Auth) issues JWT with `sub=user_id` claim
2. **Token Storage**: Frontend stores token, Frontend sends in Authorization header
3. **Backend Verification**: Backend verifies signature using shared secret (BETTER_AUTH_SECRET)
4. **User Extraction**: Backend extracts `sub` claim → authenticated_user_id
5. **Data Filtering**: All queries filter by extracted user_id (e.g., `WHERE task.user_id = :user_id`)

**Security Properties**:
- Token cannot be forged (requires secret key)
- Token cannot be tampered with (signature fails)
- User ID cannot be spoofed (comes from verified token only)
- No session state means horizontal scaling works
- Stateless verification is fast (no database lookup)

**Implementation**:
```python
# Pseudo-code pattern
def get_current_user(token: str = Depends(HTTPBearer())):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("sub")
    return user_id

@router.get("/api/tasks")
async def list_tasks(user_id: int = Depends(get_current_user)):
    # Query: SELECT * FROM tasks WHERE user_id = :user_id
    return tasks
```

---

## HTTP Status Code Strategy

**Decision**: Strict status codes per Phase II Constitution §5

**Mapping**:
- **200 OK**: Successful GET, PUT, DELETE operations
- **201 Created**: Successful POST (task creation)
- **204 No Content**: DELETE without response body (alternative to 200)
- **400 Bad Request**: Validation error (missing title, invalid JSON)
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Authenticated but unauthorized (e.g., accessing another user's task)
- **404 Not Found**: Resource doesn't exist (for authorized users)
- **500 Internal Server Error**: Unexpected backend error

**Important Distinction** (per spec):
- 403 for cross-user access (even though resource exists) - prevents information leakage
- 404 for genuinely non-existent resources
- Always verify user_id BEFORE checking existence

**Implementation**:
```python
# Pseudo-code
async def get_task(task_id, user_id):
    task = await db.get_task(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    if task.user_id != user_id:
        raise HTTPException(403, "Forbidden")  # Don't reveal existence
    return task
```

---

## Data Model & User Isolation

**Decision**: Task model with mandatory user_id foreign key

**Research Findings**:
1. **Task Entity**: Minimal but sufficient for CRUD operations
   - `id`: Primary key (UUID or auto-increment integer)
   - `user_id`: Foreign key to users table (mandatory, indexed)
   - `title`: String, non-empty (NOT NULL constraint)
   - `description`: String, optional (nullable or empty string default)
   - `status`: Enum {"Incomplete", "Complete"} (NOT NULL, default "Incomplete")
   - `created_at`, `updated_at`: Timestamps (auto-managed by DB)

2. **User Isolation Enforcement**:
   - Every query explicitly filters: `WHERE task.user_id = :user_id`
   - Not achieved through result filtering (weak), must be in SQL query
   - Database constraint: tasks.user_id cannot be NULL
   - Index on (user_id) for performance

3. **Foreign Key Relationship**:
   - Task.user_id → User.id (Neon PostgreSQL)
   - Cascade delete optional (retention policies may require soft delete)

**Implementation**:
```python
# SQLModel Task definition
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str = Field(min_length=1)
    description: str = ""
    status: str = Field(default="Incomplete")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Request/Response Schema Design

**Decision**: Separate request (create/update) and response schemas

**Why Chosen**:
- **TaskCreate**: Accepts title + description, Backend adds user_id and status
- **TaskUpdate**: Accepts optional title + description (partial updates)
- **TaskResponse**: Returns full task object including id, user_id, timestamps
- Prevents clients from sending unnecessary/dangerous fields
- Explicit schema clarity for API consumers

**Schema Patterns**:
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
```

---

## Async/Concurrency Handling

**Decision**: Use FastAPI async endpoints with async database sessions

**Why Chosen**:
- FastAPI built for async Python (using Starlette)
- SQLModel supports async sessions with AsyncSession
- Better resource utilization for I/O-bound operations
- Handles many concurrent requests efficiently
- Aligns with serverless deployment model

**Implementation**:
```python
@router.get("/api/tasks")
async def list_tasks(user_id: int = Depends(get_current_user),
                     session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return result.scalars().all()
```

---

## Testing Strategy Research

**Decision**: Three-tier testing pyramid

**Why Chosen**:
- Spec explicitly requires: "Unit tests and API-level integration tests"
- Security tests critical: "Authentication and Cross-User Data Access failure cases must be explicitly tested"
- Pyramid structure: Many unit tests, fewer integration tests, security at both levels

**Test Categories**:

1. **Unit Tests** (many, fast):
   - Model validation (SQLModel constraints)
   - Schema validation (Pydantic)
   - Helper functions (JWT parsing)

2. **Integration Tests** (moderate):
   - Full API endpoint tests with test database
   - Happy path scenarios (CRUD operations)
   - Error scenarios (400/401/403/404)

3. **Security Tests** (focused):
   - Missing JWT token → 401
   - Invalid JWT token → 401
   - Cross-user access attempt → 403
   - Token expiration handling
   - User_id manipulation in request body (must use JWT value)

**Implementation Framework**: pytest with httpx for async testing

---

## Error Handling Strategy

**Decision**: FastAPI HTTPException with appropriate status codes

**Why Chosen**:
- FastAPI provides built-in exception handling
- HTTPException maps to appropriate status codes
- Consistent error response format
- Middleware can add logging/tracing

**Error Scenarios**:
- **400 Bad Request**: Pydantic validation fails (automatic)
- **401 Unauthorized**: HTTPException(status_code=401, detail="Missing or invalid token")
- **403 Forbidden**: HTTPException(status_code=403, detail="Forbidden")
- **404 Not Found**: HTTPException(status_code=404, detail="Task not found")
- **500 Internal Server Error**: Unhandled exceptions (logged, generic error returned)

---

## Performance Considerations

**Decision**: Optimize for sub-500ms response times (per SC-001)

**Techniques**:
1. **Connection Pooling**: SQLModel session management with connection pool
2. **Query Optimization**: Index on user_id for fast filtering
3. **Async Operations**: Non-blocking I/O prevents thread starvation
4. **JWT Verification**: Signature-only (no DB lookup) for speed
5. **Response Serialization**: FastAPI automatic JSON encoding

**Benchmarking**: Test with typical payloads (title ~50 chars, description ~200 chars, 100-1000 tasks per user)

---

## Deployment Considerations

**Decision**: Stateless design enables cloud deployment

**Why Chosen**:
- No session storage means horizontal scaling works
- Multiple instances share nothing (stateless)
- Database connection pooling handles concurrency
- Environment-based configuration (no hardcoded values)

**Requirements**:
- Environment variables: DATABASE_URL, BETTER_AUTH_SECRET
- Cold start optimization (avoid large imports at module level)
- Container image (Dockerfile) for cloud deployment
- Logging/monitoring integration (optional, future enhancement)

---

## Security Research Summary

**Threat**: User A reads/modifies User B's tasks
**Mitigation**: User_id extracted from JWT, all queries filtered by user_id, 403 response for cross-user access
**Verification**: Security tests explicitly verify 403 responses for unauthorized access

**Threat**: Forged JWT tokens
**Mitigation**: Signature verification using BETTER_AUTH_SECRET, invalid tokens → 401
**Verification**: Unit tests verify JWT parsing/validation

**Threat**: User manipulates user_id in request body
**Mitigation**: User_id comes ONLY from JWT token, never from request body
**Verification**: Schemas don't accept user_id, only title/description

**Threat**: Missing authentication
**Mitigation**: All endpoints require JWT via Depends(get_current_user)
**Verification**: No endpoints exposed without authentication decorator

---

## Resolved Clarifications

✅ **All specification requirements have clear, resolved decisions**

| Requirement | Decision | Rationale |
|-------------|----------|-----------|
| Auth method | JWT signature verification | Phase II Constitution mandate |
| Storage | PostgreSQL + SQLModel | Phase II Constitution mandate |
| Framework | FastAPI | Phase II Constitution mandate |
| User isolation | Query-level filtering + 403 | Security-first principle |
| Status codes | 401/403/404 explicit mapping | Phase II Constitution §5 |
| Async handling | FastAPI async/await | Concurrency requirement |
| Testing | Unit + Integration + Security | Spec requirement |

---

## Outstanding Items

None. All design decisions are:
- ✅ Constitution-compliant
- ✅ Specification-aligned
- ✅ Security-first
- ✅ Ready for implementation

---

## Next Phase Inputs

- **Phase 1 Output**: data-model.md, contracts/openapi.yaml, quickstart.md
- **Phase 2 Output**: tasks.md (implementation task breakdown)
- **Phase 3**: Code generation via Claude Code

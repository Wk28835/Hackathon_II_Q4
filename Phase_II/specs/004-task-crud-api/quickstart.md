# Quick Start Guide: Task CRUD API

**Feature**: Authenticated, user-scoped Task CRUD API
**Date**: 2026-01-10
**Stack**: FastAPI + SQLModel + PostgreSQL

---

## Overview

This quick start guide provides instructions to set up the Task CRUD API backend for local development and testing. The API provides RESTful endpoints for authenticated users to manage their tasks with JWT-based authentication.

---

## Prerequisites

- Python 3.12+
- PostgreSQL database (local or Neon Serverless)
- pip (Python package manager)
- curl or Postman (for testing endpoints)
- JWT token from authentication service (Better Auth)

---

## Setup Instructions

### 1. Clone and Navigate to Backend Directory

```bash
cd backend/
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file in backend directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Authentication
BETTER_AUTH_SECRET=your-shared-secret-key-here

# API Settings
API_PORT=8000
API_HOST=127.0.0.1
```

### 5. Initialize Database

```bash
# Using Alembic (if migrations are set up)
alembic upgrade head

# Or manually create tables:
# psql -f scripts/init_db.sql
```

### 6. Run the Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 7. Access API Documentation

Open browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Testing the API

### Prerequisites for Testing

You need a valid JWT token. For local testing, generate a test token:

```bash
# Using python-jose (example script)
from jose import jwt
from datetime import datetime, timedelta

SECRET = "your-shared-secret-key-here"
payload = {
    "sub": 42,  # User ID
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
```

### Test 1: Create a Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "user_id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Incomplete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:30:00Z"
}
```

### Test 2: List All Tasks

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 42,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "Incomplete",
    "created_at": "2026-01-10T14:30:00Z",
    "updated_at": "2026-01-10T14:30:00Z"
  }
]
```

### Test 3: Get Specific Task

```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 42,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Incomplete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:30:00Z"
}
```

### Test 4: Update a Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy organic groceries",
    "description": "Organic milk, free-range eggs, whole grain bread"
  }'
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 42,
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs, whole grain bread",
  "status": "Incomplete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:35:00Z"
}
```

### Test 5: Mark Task as Complete

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Complete"
  }'
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 42,
  "title": "Buy organic groceries",
  "description": "Organic milk, free-range eggs, whole grain bread",
  "status": "Complete",
  "created_at": "2026-01-10T14:30:00Z",
  "updated_at": "2026-01-10T14:40:00Z"
}
```

### Test 6: Delete a Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response** (204 No Content):
```
[Empty body]
```

---

## Security Tests

### Test 7: Missing JWT Token (401 Unauthorized)

```bash
curl -X GET http://localhost:8000/api/tasks
```

**Expected Response** (401):
```json
{
  "detail": "Not authenticated"
}
```

### Test 8: Invalid JWT Token (401 Unauthorized)

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer invalid_token"
```

**Expected Response** (401):
```json
{
  "detail": "Invalid authentication credentials"
}
```

### Test 9: Cross-User Access Attempt (403 Forbidden)

```bash
# Create task as User 42
# Then attempt to access as User 99
# (Would need two different JWT tokens with different user IDs)

curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer OTHER_USER_JWT_TOKEN"
```

**Expected Response** (403):
```json
{
  "detail": "Forbidden"
}
```

---

## Running Tests

### Unit Tests

```bash
pytest tests/unit/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v
```

### Security Tests

```bash
pytest tests/security/ -v
```

### All Tests

```bash
pytest tests/ -v --cov=app --cov-report=html
```

---

## Database Verification

### Check Connected Database

```bash
psql -U user -d todo_db -c "SELECT * FROM task;"
```

### View Task Table Schema

```bash
psql -U user -d todo_db -c "\d task"
```

**Expected Output**:
```
                                     Table "public.task"
   Column   |           Type           | Collation | Nullable | Default
------------+--------------------------+-----------+----------+---------
 id         | integer                  |           | not null | ...
 user_id    | integer                  |           | not null |
 title      | character varying(255)   |           | not null |
 description| text                     |           |          | ''::text
 status     | character varying(20)    |           | not null | 'Incomplete'::...
 created_at | timestamp with time zone |           | not null | ...
 updated_at | timestamp with time zone |           | not null | ...
```

---

## Development Workflow

### Make Code Changes

Edit files in `app/` directory:
- `app/main.py`: FastAPI app setup
- `app/models/task.py`: SQLModel Task entity
- `app/api/routes.py`: Endpoint handlers
- `app/crud/task.py`: Database operations

### Test Changes

```bash
# Run specific test file
pytest tests/integration/test_api.py -v

# Run with live server
uvicorn app.main:app --reload
```

### Create Migrations (if using Alembic)

```bash
alembic revision --autogenerate -m "Add task table"
alembic upgrade head
```

---

## Troubleshooting

### Error: "could not connect to server"

**Problem**: Database connection failed

**Solution**:
- Check DATABASE_URL in .env
- Verify PostgreSQL is running
- Check credentials (user, password, database name)

```bash
psql -U user -h localhost -d todo_db -c "SELECT 1"
```

### Error: "NotAuthenticated"

**Problem**: Missing JWT token

**Solution**:
- Add Authorization header with Bearer token
- Verify token is not expired
- Use valid test token

### Error: "Forbidden" on own task

**Problem**: user_id in token doesn't match task's user_id

**Solution**:
- Verify JWT token's `sub` claim matches task owner
- Create new task while authenticated
- Check that task exists and belongs to you

### Server won't start

**Problem**: Port 8000 already in use

**Solution**:
```bash
# Use different port
uvicorn app.main:app --port 8001

# Or kill process using port 8000
# Linux/macOS:
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows:
netstat -ano | findstr :8000
```

---

## Performance Testing

### Simple Load Test (Apache Bench)

```bash
# Install apache2-utils (Linux) or httpd (macOS)
ab -n 100 -c 10 -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/tasks
```

### Expected Results

- Requests per second: >100
- Time per request: <100ms (average)
- Success rate: 100%

---

## Next Steps

1. **Run All Tests**: Ensure >90% test coverage
2. **Review Swagger Docs**: Validate API contracts at /docs
3. **Deploy to Staging**: Move to cloud environment
4. **Load Testing**: Run with realistic user load
5. **Security Audit**: Penetration testing for JWT/authorization

---

## API Reference

For complete API documentation, see:
- **OpenAPI Specification**: `contracts/openapi.yaml`
- **Swagger UI**: http://localhost:8000/docs
- **Data Model**: `data-model.md`

---

## Support

For issues or questions, refer to:
- Phase II Constitution: `../.specify/memory/constitution.md`
- Feature Specification: `spec.md`
- Implementation Plan: `plan.md`

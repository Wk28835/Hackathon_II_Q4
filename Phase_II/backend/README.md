# Task CRUD API

Authenticated, user-scoped Task CRUD API built with FastAPI and SQLModel for Phase II of the Evolution of Todo hackathon.

## Features

✅ **JWT-Based Authentication**: Stateless token verification using shared secret
✅ **User Data Isolation**: Automatic filtering of tasks by authenticated user
✅ **Complete CRUD Operations**: Create, read (all and single), update, delete, and status management
✅ **Async/Await**: Built on FastAPI's async capabilities for high concurrency
✅ **PostgreSQL Storage**: Persistent data with SQLModel ORM
✅ **Comprehensive Testing**: Unit, integration, security, and performance tests
✅ **API Documentation**: Auto-generated Swagger UI and ReDoc

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

```bash
# Clone repository
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your PostgreSQL connection details

# Initialize database
python -m app.database

# Run server
uvicorn app.main:app --reload
```

**API available at**: http://localhost:8000
**Swagger UI**: http://localhost:8000/docs
**ReDoc**: http://localhost:8000/redoc

### Using Docker Compose

```bash
docker-compose up -d

# API available at http://localhost:8000
```

## API Endpoints

All endpoints require JWT authentication in `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks` | List all user's tasks |
| GET | `/api/tasks/{id}` | Get specific task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/{id}/status` | Mark task complete/incomplete |
| GET | `/health` | Health check (no auth required) |

## Example Usage

### Create Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

### List Tasks

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <jwt-token>"

# Filter by status
curl -X GET "http://localhost:8000/api/tasks?status=Incomplete" \
  -H "Authorization: Bearer <jwt-token>"
```

### Get Task

```bash
curl -X GET http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <jwt-token>"
```

### Update Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy organic groceries"
  }'
```

### Mark Complete

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/status \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "Complete"}'
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <jwt-token>"
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test category
pytest tests/security/ -v        # Security tests
pytest tests/integration/ -v      # Integration tests

# With coverage report
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage

- ✅ **Authentication**: Missing token, invalid token
- ✅ **Authorization**: Cross-user access attempts, 403 responses
- ✅ **CRUD Operations**: Create, read, update, delete workflows
- ✅ **Validation**: Empty title, too-long descriptions
- ✅ **Status Transitions**: Mark complete/incomplete
- ✅ **Concurrency**: 100+ concurrent operations

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/
│   │   └── task.py          # Task entity
│   ├── schemas/
│   │   └── task.py          # Request/response schemas
│   ├── crud/
│   │   └── task.py          # CRUD operations
│   ├── api/
│   │   ├── auth.py          # JWT verification
│   │   └── routes.py        # Endpoint handlers
│   └── middleware/
│       └── error_handler.py # Error handling
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── security/            # Auth & authorization tests
│   ├── integration/         # Workflow & CRUD tests
│   └── performance/         # Load tests (optional)
├── scripts/
│   └── init_db.sql          # Database schema
├── requirements.txt
├── .env.example
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Security

### Authentication

- JWT tokens signed with shared secret (`BETTER_AUTH_SECRET`)
- Token verified on every protected endpoint
- Missing/invalid tokens return 401 Unauthorized

### Authorization

- User_id extracted from JWT token (not from request body)
- All queries filtered by user_id (user data isolation)
- Unauthorized access returns 403 Forbidden
- No information leakage (403 for cross-user attempts, not 404)

### Best Practices

- ✅ Stateless backend (no session storage)
- ✅ HTTPS/TLS required in production
- ✅ Strong `BETTER_AUTH_SECRET` (256+ bits)
- ✅ Regular secret rotation
- ✅ Request validation on all inputs
- ✅ Comprehensive error handling

## Development

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed development guide.

### Code Quality

```bash
# Format
black app/ tests/

# Lint
flake8 app/ tests/

# Type check
mypy app/

# Sort imports
isort app/ tests/
```

## Performance

Target metrics (per specification):

- ✅ Task operations < 500ms
- ✅ Supports concurrent multi-user requests
- ✅ Connection pooling enabled (20 connections + 40 overflow)
- ✅ Async/await for non-blocking I/O

## Deployment

### Docker

```bash
# Build image
docker build -t task-crud-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e BETTER_AUTH_SECRET=... \
  task-crud-api
```

### Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Use strong `BETTER_AUTH_SECRET`
- [ ] Configure PostgreSQL for high availability
- [ ] Enable HTTPS/TLS
- [ ] Set up monitoring and logging
- [ ] Configure CORS properly
- [ ] Run security audit
- [ ] Load test with expected user volume

## Documentation

- **Specification**: `../specs/004-task-crud-api/spec.md`
- **Implementation Plan**: `../specs/004-task-crud-api/plan.md`
- **Data Model**: `../specs/004-task-crud-api/data-model.md`
- **API Spec**: `../specs/004-task-crud-api/contracts/openapi.yaml`
- **Quick Start**: `../specs/004-task-crud-api/quickstart.md`

## Phase II Constitution Alignment

✅ Implements all Phase II principles:
- Spec-driven development
- Security-first (JWT + user isolation)
- Clean separation (backend-only)
- FastAPI + SQLModel + PostgreSQL
- Stateless architecture
- Comprehensive testing

## License

Part of Evolution of Todo hackathon (Phase II)

## Support

For issues or questions, refer to:
- Phase II Constitution: `../.specify/memory/constitution.md`
- Feature Specification: `../specs/004-task-crud-api/spec.md`
- DEVELOPMENT.md (this directory)

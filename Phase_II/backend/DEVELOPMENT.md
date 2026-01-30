# Development Guide: Task CRUD API

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start database and API
docker-compose up -d

# Run migrations (if using Alembic)
docker-compose exec api alembic upgrade head

# API will be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env
# Edit .env with your actual values

# 4. Run database migrations (if needed)
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload

# API available at http://localhost:8000
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/integration/test_crud_workflow.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run security tests only
pytest tests/security/ -v -m security

# Run integration tests only
pytest tests/integration/ -v -m integration
```

## Common Development Tasks

### Add a New Endpoint

1. Define request/response schemas in `app/schemas/`
2. Implement CRUD function in `app/crud/task.py`
3. Add route handler in `app/api/routes.py`
4. Write tests in `tests/integration/` and `tests/security/`

### Update Database Schema

1. Create migration: `alembic revision --autogenerate -m "description"`
2. Review and edit generated migration in `alembic/versions/`
3. Run migration: `alembic upgrade head`

### Debug Issues

```bash
# Enable debug logging
DEBUG=true LOG_LEVEL=DEBUG uvicorn app.main:app --reload

# Check database connection
psql $DATABASE_URL -c "SELECT 1"

# View logs
docker-compose logs -f api
```

## Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/

# Sort imports
isort app/ tests/
```

## Database Management

### Reset Database

```bash
# Using Docker Compose
docker-compose down -v
docker-compose up -d

# Local development
# Delete local database file and restart
rm instance/todo_db.db
```

### View Database Contents

```bash
# Connect to database
psql postgresql://taskuser:taskpass@localhost:5432/todo_db

# List tables
\dt

# Query tasks
SELECT * FROM task;

# Query specific user's tasks
SELECT * FROM task WHERE user_id = 42;
```

## Environment Variables

Required for development:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-here
API_PORT=8000
API_HOST=127.0.0.1
DEBUG=true
LOG_LEVEL=INFO
```

## Troubleshooting

### Database Connection Failed

```bash
# Check if PostgreSQL is running
psql --version

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### Port 8000 Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001 --reload
```

### Virtual Environment Issues

```bash
# Deactivate and remove
deactivate
rm -rf venv

# Recreate
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Implementation Plan**: `../specs/004-task-crud-api/plan.md`
- **Data Model**: `../specs/004-task-crud-api/data-model.md`

## Production Checklist

Before deploying to production:

- [ ] Set `DEBUG=false`
- [ ] Set `LOG_LEVEL=WARNING`
- [ ] Configure `CORS` origins properly
- [ ] Use strong `BETTER_AUTH_SECRET` (rotate from development)
- [ ] Use production PostgreSQL database
- [ ] Enable HTTPS/TLS
- [ ] Configure authentication headers properly
- [ ] Set up monitoring and alerting
- [ ] Perform load testing
- [ ] Security audit

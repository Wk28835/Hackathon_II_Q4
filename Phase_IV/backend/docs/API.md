# Task CRUD API

This document mirrors the OpenAPI contract at:
- `specs/004-task-crud-api/contracts/openapi.yaml`

## Authentication

All `/api/*` endpoints require:

- `Authorization: Bearer <jwt>`

The backend validates the JWT signature using `BETTER_AUTH_SECRET`.

## Endpoints

- `POST /api/tasks` – Create task
- `GET /api/tasks` – List tasks (optional `?status=Incomplete|Complete`)
- `GET /api/tasks/{task_id}` – Get task by id
- `PUT /api/tasks/{task_id}` – Update task
- `DELETE /api/tasks/{task_id}` – Delete task
- `PATCH /api/tasks/{task_id}/status` – Update task status

## Schemas

See `openapi.yaml` for full schema definitions:

- `Task`
- `TaskCreate`
- `TaskUpdate`
- `TaskStatusUpdate`
- `ErrorResponse`

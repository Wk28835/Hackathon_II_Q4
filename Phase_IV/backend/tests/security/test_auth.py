"""Security and authentication tests for Task CRUD API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestAuthenticationRequired:
    """Test that all endpoints require authentication."""

    @pytest.mark.security
    def test_create_task_missing_jwt(self):
        """Test: POST /api/tasks without JWT token → 401 Unauthorized."""
        response = client.post(
            "/api/tasks",
            json={"title": "Test task"},
        )
        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.security
    def test_list_tasks_missing_jwt(self):
        """Test: GET /api/tasks without JWT token → 401 Unauthorized."""
        response = client.get("/api/tasks")
        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.security
    def test_get_task_missing_jwt(self):
        """Test: GET /api/tasks/1 without JWT token → 401 Unauthorized."""
        response = client.get("/api/tasks/1")
        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.security
    def test_update_task_missing_jwt(self):
        """Test: PUT /api/tasks/1 without JWT token → 401 Unauthorized."""
        response = client.put(
            "/api/tasks/1",
            json={"title": "Updated title"},
        )
        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.security
    def test_delete_task_missing_jwt(self):
        """Test: DELETE /api/tasks/1 without JWT token → 401 Unauthorized."""
        response = client.delete("/api/tasks/1")
        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.security
    def test_mark_status_missing_jwt(self):
        """Test: PATCH /api/tasks/1/status without JWT token → 401 Unauthorized."""
        response = client.patch(
            "/api/tasks/1/status",
            json={"status": "Complete"},
        )
        assert response.status_code == 401
        assert "detail" in response.json()


class TestInvalidJWTToken:
    """Test that invalid JWT tokens are rejected."""

    @pytest.mark.security
    def test_create_task_invalid_jwt(self, invalid_jwt_token):
        """Test: POST /api/tasks with invalid JWT token → 401 Unauthorized."""
        response = client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {invalid_jwt_token}"},
            json={"title": "Test task"},
        )
        assert response.status_code == 401

    @pytest.mark.security
    def test_list_tasks_invalid_jwt(self, invalid_jwt_token):
        """Test: GET /api/tasks with invalid JWT token → 401 Unauthorized."""
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {invalid_jwt_token}"},
        )
        assert response.status_code == 401

    @pytest.mark.security
    def test_get_task_invalid_jwt(self, invalid_jwt_token):
        """Test: GET /api/tasks/1 with invalid JWT token → 401 Unauthorized."""
        response = client.get(
            "/api/tasks/1",
            headers={"Authorization": f"Bearer {invalid_jwt_token}"},
        )
        assert response.status_code == 401


class TestHealthEndpoint:
    """Test health check endpoint."""

    @pytest.mark.security
    def test_health_check_no_auth(self):
        """Test: GET /health without JWT token → 200 OK (no auth required)."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "version": "1.0.0"}

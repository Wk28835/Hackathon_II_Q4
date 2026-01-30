"""Integration tests for Task CRUD API endpoints.

This file exists to match the tasks.md artifact list:
- T041: Create comprehensive API integration tests in backend/tests/integration/test_api.py

Note: The repo previously used test_crud_workflow.py for these tests.
"""

import pytest


# Use dependency-injected TestClient from conftest.py


class TestCompleteCRUDWorkflow:
    """Test complete CRUD workflow for a single user."""

    @pytest.mark.integration
    def test_create_list_get_update_delete_workflow(self, client, auth_headers):
        """Test: Complete CRUD workflow (create → list → get → update → delete)."""
        # 1. Create a task
        create_response = client.post(
            "/api/tasks",
            headers=auth_headers,
            json={
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
            },
        )
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        assert task["title"] == "Buy groceries"
        assert task["description"] == "Milk, eggs, bread"
        assert task["status"] == "Incomplete"

        # 2. List tasks
        list_response = client.get(
            "/api/tasks",
            headers=auth_headers,
        )
        assert list_response.status_code == 200
        tasks = list_response.json()
        assert len(tasks) >= 1
        assert any(t["id"] == task_id for t in tasks)

        # 3. Get specific task
        get_response = client.get(
            f"/api/tasks/{task_id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 200
        retrieved_task = get_response.json()
        assert retrieved_task["id"] == task_id

        # 4. Update task
        update_response = client.put(
            f"/api/tasks/{task_id}",
            headers=auth_headers,
            json={
                "title": "Buy organic groceries",
                "description": "Organic milk, free-range eggs, whole grain bread",
            },
        )
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Buy organic groceries"

        # 5. Delete task
        delete_response = client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_headers,
        )
        assert delete_response.status_code == 204


class TestMultiUserIsolation:
    """Test multi-user isolation and data leakage prevention."""

    @pytest.mark.integration
    def test_other_user_task_access_denied(self, client, auth_headers, other_user_task_id):
        """Test: User cannot access another user's task (403 or 404 depending on policy)."""
        response = client.get(
            f"/api/tasks/{other_user_task_id}",
            headers=auth_headers,
        )
        assert response.status_code in (403, 404)


class TestValidationErrors:
    """Test validation error scenarios."""

    @pytest.mark.integration
    def test_create_task_empty_title(self, client, auth_headers):
        """Test: POST /api/tasks with empty title → validation error."""
        response = client.post(
            "/api/tasks",
            headers=auth_headers,
            json={"title": ""},
        )
        assert response.status_code in (400, 422)

    @pytest.mark.integration
    def test_mark_status_invalid_status(self, client, auth_headers, sample_task_id):
        """Test: PATCH /api/tasks/{id}/status with invalid status → 400."""
        response = client.patch(
            f"/api/tasks/{sample_task_id}/status",
            headers=auth_headers,
            json={"status": "Invalid"},
        )
        assert response.status_code == 400

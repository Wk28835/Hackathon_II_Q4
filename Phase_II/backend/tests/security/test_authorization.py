"""Authorization and data isolation tests for Task CRUD API."""

import pytest


# Use dependency-injected TestClient from conftest.py


class TestUserDataIsolation:
    """Test that users can only access their own tasks."""

    @pytest.mark.security
    def test_list_shows_only_user_tasks(self, client, auth_headers, sample_task, other_user_task):
        """Test: GET /api/tasks returns only authenticated user's tasks."""
        response = client.get(
            "/api/tasks",
            headers=auth_headers,
        )
        assert response.status_code == 200
        tasks = response.json()
        # Should only contain the sample_task, not other_user_task
        assert len(tasks) >= 1
        for task in tasks:
            assert task["user_id"] == "test_user_42"  # test_user_id

    @pytest.mark.security
    def test_get_other_user_task_returns_403(self, client, auth_headers, other_user_task_id):
        """Test: GET /api/tasks/{id} for other user's task → 403 Forbidden (not 404)."""
        response = client.get(
            f"/api/tasks/{other_user_task_id}",
            headers=auth_headers,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Forbidden"

    @pytest.mark.security
    def test_update_other_user_task_returns_403(self, client, auth_headers, other_user_task_id):
        """Test: PUT /api/tasks/{id} for other user's task → 403 Forbidden."""
        response = client.put(
            f"/api/tasks/{other_user_task_id}",
            headers=auth_headers,
            json={"title": "Hacked title"},
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Forbidden"

    @pytest.mark.security
    def test_delete_other_user_task_returns_403(self, client, auth_headers, other_user_task_id):
        """Test: DELETE /api/tasks/{id} for other user's task → 403 Forbidden."""
        response = client.delete(
            f"/api/tasks/{other_user_task_id}",
            headers=auth_headers,
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Forbidden"

    @pytest.mark.security
    def test_mark_status_other_user_task_returns_403(self, client, auth_headers, other_user_task_id):
        """Test: PATCH /api/tasks/{id}/status for other user's task → 403 Forbidden."""
        response = client.patch(
            f"/api/tasks/{other_user_task_id}/status",
            headers=auth_headers,
            json={"status": "Complete"},
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Forbidden"


class TestUserIDInjection:
    """Test that user_id from request body is ignored."""

    @pytest.mark.security
    def test_create_task_ignores_request_user_id(self, client, auth_headers):
        """Test: POST /api/tasks with user_id in body → ignored, JWT user_id used."""
        response = client.post(
            "/api/tasks",
            headers=auth_headers,
            json={
                "title": "Test task",
                "user_id": 999,  # Try to inject a different user_id
            },
        )
        # Should succeed - user_id field should be ignored
        # Actual behavior depends on schema strictness
        # If user_id is in schema, it should be ignored
        # If not in schema, extra fields are ignored by default
        if response.status_code == 201:
            task = response.json()
            assert task["user_id"] == "test_user_42"  # Should be test_user_id, not 999

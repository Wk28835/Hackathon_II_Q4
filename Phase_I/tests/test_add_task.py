"""Unit tests for the Add Task feature."""

import sys
from io import StringIO
from unittest.mock import patch

import pytest

from src.cli import create_parser, parse_add_args, parse_list_args
from src.storage import TaskList
from src.task import Task
from src.validation import validate_title
from src.list_handler import format_task_table, format_empty_message, format_filter_empty_message, truncate_text
from src.update_handler import is_valid_uuid, find_task_by_id, update_task, format_update_success

class TestTask:
    """Tests for the Task dataclass."""

    def test_task_creation_with_defaults(self):
        """Test creating a task with only required fields."""
        task = Task(title="Test task")
        assert task.title == "Test task"
        assert task.description == ""
        assert task.status == "Incomplete"
        assert task.id is not None

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        task = Task(title="Test task", description="Test description", status="Incomplete")
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.status == "Incomplete"

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(title="Buy groceries", description="Milk, Eggs")
        task_dict = task.to_dict()
        assert isinstance(task_dict, dict)
        assert task_dict["title"] == "Buy groceries"
        assert task_dict["description"] == "Milk, Eggs"
        assert task_dict["status"] == "Incomplete"
        assert "id" in task_dict

    def test_task_repr(self):
        """Test task string representation."""
        task = Task(title="Test")
        repr_str = repr(task)
        assert "Task" in repr_str
        assert "Test" in repr_str


class TestTaskList:
    """Tests for the TaskList class."""

    def test_empty_task_list(self):
        """Test creating an empty task list."""
        task_list = TaskList()
        assert len(task_list) == 0

    def test_add_task(self):
        """Test adding a task to the list."""
        task_list = TaskList()
        task = task_list.add_task("Buy groceries")
        assert len(task_list) == 1
        assert task.title == "Buy groceries"

    def test_add_task_with_description(self):
        """Test adding a task with description."""
        task_list = TaskList()
        task = task_list.add_task("Buy groceries", "Milk, Eggs, Bread")
        assert len(task_list) == 1
        assert task.description == "Milk, Eggs, Bread"

    def test_unique_ids(self):
        """Test that each task gets a unique ID."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task2 = task_list.add_task("Task 2")
        assert task1.id != task2.id

    def test_default_status(self):
        """Test that default status is Incomplete."""
        task_list = TaskList()
        task = task_list.add_task("Test task")
        assert task.status == "Incomplete"

    def test_task_list_iteration(self):
        """Test iterating over task list."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")
        tasks = list(task_list)
        assert len(tasks) == 2


class TestValidation:
    """Tests for the validation module."""

    def test_valid_title(self):
        """Test validation with a valid title."""
        is_valid, error = validate_title("Buy groceries")
        assert is_valid is True
        assert error is None

    def test_empty_title(self):
        """Test validation with empty string."""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert error == "Title must not be empty."

    def test_whitespace_only_title(self):
        """Test validation with whitespace-only string."""
        is_valid, error = validate_title("   ")
        assert is_valid is False
        assert error == "Title must not be empty."

    def test_none_title(self):
        """Test validation with None."""
        is_valid, error = validate_title(None)
        assert is_valid is False
        assert error == "Title must not be empty."

    def test_title_with_spaces_and_text(self):
        """Test validation with text that has leading/trailing spaces."""
        is_valid, error = validate_title("  Buy groceries  ")
        assert is_valid is True
        assert error is None


class TestCLI:
    """Tests for the CLI module."""

    def test_parse_add_args_title_only(self):
        """Test parsing add command with title only."""
        args = parse_add_args(["Buy groceries"])
        assert args.title == "Buy groceries"
        assert args.description == ""

    def test_parse_add_args_with_description(self):
        """Test parsing add command with description."""
        args = parse_add_args(["Buy groceries", "--description", "Milk, Eggs"])
        assert args.title == "Buy groceries"
        assert args.description == "Milk, Eggs"

    def test_parse_add_args_short_description_flag(self):
        """Test parsing add command with short -d flag."""
        args = parse_add_args(["Buy groceries", "-d", "Milk, Eggs"])
        assert args.title == "Buy groceries"
        assert args.description == "Milk, Eggs"

    def test_create_parser_has_add_command(self):
        """Test that parser has add subcommand."""
        parser = create_parser()
        # Should not raise when parsing valid add command
        args = parser.parse_args(["add", "Test task"])
        assert args.command == "add"
        assert args.title == "Test task"


class TestMain:
    """Integration tests for the main module."""

    def test_successful_task_creation(self):
        """Test successful task creation output."""
        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "add", "Buy groceries"]):
            with patch("sys.stdout", captured):
                from src.main import main

                exit_code = main()
        output = captured.getvalue()
        assert exit_code == 0
        assert "Buy groceries" in output
        assert "added successfully" in output
        assert "ID" in output

    def test_empty_title_error(self):
        """Test error output for empty title."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "add", ""]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main

                    exit_code = main()
        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Title must not be empty" in error_str

    def test_whitespace_title_error(self):
        """Test error output for whitespace-only title."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "add", "   "]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main

                    exit_code = main()
        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Title must not be empty" in error_str


class TestTruncateText:
    """Tests for the truncate_text function."""

    def test_short_text_unchanged(self):
        """Test that short text is not truncated."""
        result = truncate_text("Hello", 10)
        assert result == "Hello"

    def test_long_text_truncated(self):
        """Test that long text is truncated with ellipsis."""
        result = truncate_text("This is a very long text", 10)
        assert result == "This is a ..."
        assert len(result) == 13  # 10 chars + 3 for ellipsis

    def test_exact_length_text(self):
        """Test text at exact max length."""
        result = truncate_text("Hello", 5)
        assert result == "Hello"


class TestFormatTaskTable:
    """Tests for the format_task_table function."""

    def test_empty_list_returns_empty_message(self):
        """Test that empty list shows empty message."""
        result = format_task_table([])
        assert "No tasks found" in result

    def test_single_task(self):
        """Test formatting a single task."""
        task = Task(title="Test task", description="Test description")
        result = format_task_table([task])
        assert "Test task" in result
        assert "Test description" in result
        assert "Incomplete" in result
        # Check UUID is present (first 8 chars should be visible)
        assert task.id[:8] in result

    def test_multiple_tasks(self):
        """Test formatting multiple tasks."""
        task1 = Task(title="Task 1", description="Desc 1")
        task2 = Task(title="Task 2", description="Desc 2", status="Complete")
        result = format_task_table([task1, task2])
        assert "Task 1" in result
        assert "Task 2" in result
        assert "Incomplete" in result
        assert "Complete" in result

    def test_long_title_truncated(self):
        """Test that long titles are truncated."""
        task = Task(title="A very long task title that should be truncated")
        result = format_task_table([task])
        assert "..." in result
        assert "truncated" not in result  # Original text not fully present


class TestFormatEmptyMessage:
    """Tests for empty state messages."""

    def test_empty_message(self):
        """Test the empty state message."""
        result = format_empty_message()
        assert "No tasks found" in result
        assert "Add a task" in result

    def test_filter_empty_message(self):
        """Test the filter-specific empty message."""
        result = format_filter_empty_message("incomplete")
        assert "No tasks found" in result
        assert "incomplete" in result


class TestTaskList:
    """Tests for the TaskList class."""

    def test_filter_all(self):
        """Test filtering by 'all' returns all tasks."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2", status="Complete")

        result = task_list.filter_by_status("all")
        assert len(result) == 2

    def test_filter_incomplete(self):
        """Test filtering by 'incomplete'."""
        task_list = TaskList()
        task_list.add_task("Task 1")  # Default: Incomplete
        task2 = task_list.add_task("Task 2")
        task2.status = "Complete"

        result = task_list.filter_by_status("incomplete")
        assert len(result) == 1
        assert result[0].title == "Task 1"

    def test_filter_complete(self):
        """Test filtering by 'complete'."""
        task_list = TaskList()
        task1 = task_list.add_task("Task 1")
        task1.status = "Complete"
        task_list.add_task("Task 2")  # Default: Incomplete

        result = task_list.filter_by_status("complete")
        assert len(result) == 1
        assert result[0].title == "Task 1"

    def test_filter_case_insensitive(self):
        """Test that filtering is case-insensitive."""
        task_list = TaskList()
        task = task_list.add_task("Task")
        task.status = "COMPLETE"

        result = task_list.filter_by_status("Complete")
        assert len(result) == 1

        result = task_list.filter_by_status("complete")
        assert len(result) == 1


class TestCLI:
    """Tests for the CLI module."""

    def test_parse_list_args_all(self):
        """Test parsing list command with all status."""
        args = parse_list_args([])
        assert args.status == "all"

    def test_parse_list_args_incomplete(self):
        """Test parsing list command with incomplete status."""
        args = parse_list_args(["--status", "incomplete"])
        assert args.status == "incomplete"

    def test_parse_list_args_short_flag(self):
        """Test parsing list command with short flag."""
        args = parse_list_args(["-s", "complete"])
        assert args.status == "complete"

    def test_create_parser_has_list_command(self):
        """Test that parser has list subcommand."""
        parser = create_parser()
        args = parser.parse_args(["list", "--status", "incomplete"])
        assert args.command == "list"
        assert args.status == "incomplete"

    def test_create_parser_has_add_command(self):
        """Test that parser still has add subcommand."""
        parser = create_parser()
        args = parser.parse_args(["add", "Test task"])
        assert args.command == "add"
        assert args.title == "Test task"


class TestMain:
    """Integration tests for the main module."""

    def test_list_command_with_tasks(self):
        """Test list command displays tasks."""
        # Create a TaskList with a task and verify list output
        from src.storage import TaskList
        from src.list_handler import format_task_table

        task_list = TaskList()
        task_list.add_task("Test task", "Test description")

        # Format the tasks as the list command would
        output = format_task_table(list(task_list))

        assert "Test task" in output
        assert "Test description" in output
        assert "Incomplete" in output

    def test_list_command_empty(self):
        """Test list command with no tasks shows empty message."""
        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "list"]):
            with patch("sys.stdout", captured):
                from src.main import main

                exit_code = main()
        output = captured.getvalue()
        assert exit_code == 0
        assert "No tasks found" in output

    def test_list_command_filter_incomplete(self):
        """Test list command with incomplete filter."""
        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "list", "--status", "incomplete"]):
            with patch("sys.stdout", captured):
                from src.main import main

                exit_code = main()
        output = captured.getvalue()
        assert exit_code == 0
        assert "No tasks found" in output  # No incomplete tasks yet

    def test_list_command_filter_complete(self):
        """Test list command with complete filter."""
        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "list", "-s", "complete"]):
            with patch("sys.stdout", captured):
                from src.main import main

                exit_code = main()
        output = captured.getvalue()
        assert exit_code == 0
        assert "No tasks found" in output  # No complete tasks yet


class TestIsValidUUID:
    """Tests for the is_valid_uuid function."""

    def test_valid_uuid(self):
        """Test that valid UUIDs are accepted."""
        assert is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True

    def test_invalid_uuid_format(self):
        """Test that invalid formats are rejected."""
        assert is_valid_uuid("invalid-id") is False
        assert is_valid_uuid("12345") is False
        assert is_valid_uuid("") is False

    def test_partial_uuid(self):
        """Test that partial UUIDs are rejected."""
        assert is_valid_uuid("550e8400-e29b-41d4-a716") is False


class TestFindTaskByID:
    """Tests for the find_task_by_id function."""

    def test_find_existing_task(self):
        """Test finding a task that exists."""
        task_list = TaskList()
        task = task_list.add_task("Test task", "Test description")
        result = find_task_by_id(list(task_list), task.id)
        assert result is not None
        assert result.title == "Test task"

    def test_find_non_existent_task(self):
        """Test finding a task that doesn't exist."""
        task_list = TaskList()
        task_list.add_task("Test task")
        result = find_task_by_id(list(task_list), "00000000-0000-0000-0000-000000000000")
        assert result is None

    def test_find_in_empty_list(self):
        """Test finding in an empty task list."""
        task_list = TaskList()
        result = find_task_by_id(list(task_list), "550e8400-e29b-41d4-a716-446655440000")
        assert result is None


class TestUpdateTask:
    """Tests for the update_task function."""

    def test_update_title_only(self):
        """Test updating only the title."""
        task = Task(title="Original title", description="Original description")
        update_task(task, new_title="New title", new_description=None)
        assert task.title == "New title"
        assert task.description == "Original description"

    def test_update_description_only(self):
        """Test updating only the description."""
        task = Task(title="Original title", description="Original description")
        update_task(task, new_title=None, new_description="New description")
        assert task.title == "Original title"
        assert task.description == "New description"

    def test_update_both_fields(self):
        """Test updating both title and description."""
        task = Task(title="Original title", description="Original description")
        update_task(task, new_title="New title", new_description="New description")
        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_with_empty_description(self):
        """Test updating with empty description."""
        task = Task(title="Title", description="Old description")
        update_task(task, new_title=None, new_description="")
        assert task.title == "Title"
        assert task.description == ""


class TestFormatUpdateSuccess:
    """Tests for the format_update_success function."""

    def test_format_update_success(self):
        """Test formatting update success message."""
        task = Task(title="Updated task", description="Updated description")
        result = format_update_success(task)
        assert "Task updated successfully" in result
        assert "Updated task" in result
        assert "Updated description" in result
        assert task.id[:8] in result


class TestUpdateCLI:
    """Tests for the update command CLI parsing."""

    def test_parse_update_args_task_id_only(self):
        """Test parsing update command with task_id only."""
        from src.cli import parse_update_args
        args = parse_update_args(["550e8400-e29b-41d4-a716-446655440000"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.title is None
        assert args.description is None

    def test_parse_update_args_with_title(self):
        """Test parsing update command with title."""
        from src.cli import parse_update_args
        args = parse_update_args(["550e8400-e29b-41d4-a716-446655440000", "--title", "New title"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.title == "New title"
        assert args.description is None

    def test_parse_update_args_with_description(self):
        """Test parsing update command with description."""
        from src.cli import parse_update_args
        args = parse_update_args(["550e8400-e29b-41d4-a716-446655440000", "--description", "New desc"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.title is None
        assert args.description == "New desc"

    def test_parse_update_args_short_description_flag(self):
        """Test parsing update command with short -d flag."""
        from src.cli import parse_update_args
        args = parse_update_args(["550e8400-e29b-41d4-a716-446655440000", "-d", "New desc"])
        assert args.description == "New desc"

    def test_parse_update_args_both_fields(self):
        """Test parsing update command with both fields."""
        from src.cli import parse_update_args
        args = parse_update_args([
            "550e8400-e29b-41d4-a716-446655440000",
            "--title", "New title",
            "--description", "New desc"
        ])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.title == "New title"
        assert args.description == "New desc"

    def test_create_parser_has_update_command(self):
        """Test that parser has update subcommand."""
        parser = create_parser()
        args = parser.parse_args([
            "update", "550e8400-e29b-41d4-a716-446655440000",
            "--title", "New title"
        ])
        assert args.command == "update"
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.title == "New title"


class TestUpdateIntegration:
    """Integration tests for the update command."""

    def test_update_title_success(self):
        """Test successful title update via main."""
        from src.storage import TaskList

        # Create a task first
        task_list = TaskList()
        task = task_list.add_task("Original title", "Original description")

        captured = StringIO()
        with patch.object(sys, "argv", [
            "main.py", "update", task.id, "--title", "Updated title"
        ]):
            with patch("sys.stdout", captured):
                from src.main import main
                exit_code = main()

        output = captured.getvalue()
        assert exit_code == 0
        assert "Task updated successfully" in output
        assert "Updated title" in output

        # Verify persistence
        task_list = TaskList()
        updated_task = find_task_by_id(list(task_list), task.id)
        assert updated_task.title == "Updated title"

    def test_update_description_success(self):
        """Test successful description update via main."""
        from src.storage import TaskList

        task_list = TaskList()
        task = task_list.add_task("Task title", "Original description")

        captured = StringIO()
        with patch.object(sys, "argv", [
            "main.py", "update", task.id, "--description", "New description"
        ]):
            with patch("sys.stdout", captured):
                from src.main import main
                exit_code = main()

        output = captured.getvalue()
        assert exit_code == 0
        assert "New description" in output

    def test_update_empty_title_error(self):
        """Test error when updating with empty title."""
        from src.storage import TaskList

        task_list = TaskList()
        task = task_list.add_task("Task title")

        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "update", task.id, "--title", ""]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Title must not be empty" in error_str

    def test_update_invalid_uuid_error(self):
        """Test error for invalid UUID format."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "update", "invalid-id", "--title", "New title"]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Invalid task ID format" in error_str

    def test_update_task_not_found_error(self):
        """Test error when task not found."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", [
            "main.py", "update", "00000000-0000-0000-0000-000000000000", "--title", "New title"
        ]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Task not found" in error_str


class TestDeleteCLI:
    """Tests for the delete command CLI parsing."""

    def test_parse_delete_args_task_id_only(self):
        """Test parsing delete command with task_id only."""
        from src.cli import parse_delete_args
        args = parse_delete_args(["550e8400-e29b-41d4-a716-446655440000"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"

    def test_create_parser_has_delete_command(self):
        """Test that parser has delete subcommand."""
        from src.cli import create_parser
        parser = create_parser()
        args = parser.parse_args(["delete", "550e8400-e29b-41d4-a716-446655440000"])
        assert args.command == "delete"
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"


class TestDeleteTask:
    """Tests for the delete_task function."""

    def test_delete_task_removes_from_list(self):
        """Test that delete_task removes the task from the list."""
        from src.delete_handler import delete_task
        from src.task import Task

        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        tasks = [task1, task2]

        delete_task(tasks, task1)
        assert len(tasks) == 1
        assert task2 in tasks
        assert task1 not in tasks

    def test_delete_last_task(self):
        """Test deleting the last task in the list."""
        from src.delete_handler import delete_task
        from src.task import Task

        task = Task(title="Only task")
        tasks = [task]

        delete_task(tasks, task)
        assert len(tasks) == 0


class TestFormatDeleteSuccess:
    """Tests for the format_delete_success function."""

    def test_format_delete_success(self):
        """Test formatting delete success message."""
        from src.delete_handler import format_delete_success
        from src.task import Task

        task = Task(title="Deleted task", description="Test description")
        result = format_delete_success(task)
        assert "Task deleted successfully" in result
        assert "Deleted task" in result
        assert task.id[:8] in result


class TestDeleteIntegration:
    """Integration tests for the delete command."""

    def test_delete_task_success(self):
        """Test successful task deletion via main."""
        from src.storage import TaskList
        from src.update_handler import find_task_by_id

        # Create a task first
        task_list = TaskList()
        task = task_list.add_task("Task to delete", "Test description")

        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "delete", task.id]):
            with patch("sys.stdout", captured):
                from src.main import main
                exit_code = main()

        output = captured.getvalue()
        assert exit_code == 0
        assert "Task deleted successfully" in output
        assert "Task to delete" in output

        # Verify task is actually deleted
        task_list = TaskList()
        result = find_task_by_id(list(task_list), task.id)
        assert result is None

    def test_delete_invalid_uuid_error(self):
        """Test error for invalid UUID format."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "delete", "invalid-id"]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Invalid task ID format" in error_str

    def test_delete_task_not_found_error(self):
        """Test error when task not found."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "delete", "00000000-0000-0000-0000-000000000000"]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Task not found" in error_str


class TestMarkCLI:
    """Tests for the mark command CLI parsing."""

    def test_parse_mark_args_complete(self):
        """Test parsing mark command with --complete flag."""
        from src.cli import parse_mark_args
        args = parse_mark_args(["550e8400-e29b-41d4-a716-446655440000", "--complete"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.status == "Complete"

    def test_parse_mark_args_incomplete(self):
        """Test parsing mark command with --incomplete flag."""
        from src.cli import parse_mark_args
        args = parse_mark_args(["550e8400-e29b-41d4-a716-446655440000", "--incomplete"])
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.status == "Incomplete"

    def test_create_parser_has_mark_command(self):
        """Test that parser has mark subcommand."""
        from src.cli import create_parser
        parser = create_parser()
        args = parser.parse_args(["mark", "550e8400-e29b-41d4-a716-446655440000", "--complete"])
        assert args.command == "mark"
        assert args.task_id == "550e8400-e29b-41d4-a716-446655440000"
        assert args.status == "Complete"


class TestMarkTask:
    """Tests for the mark_task function."""

    def test_mark_task_to_complete(self):
        """Test marking a task as complete."""
        from src.mark_handler import mark_task
        from src.task import Task

        task = Task(title="Test task", status="Incomplete")
        mark_task(task, "Complete")
        assert task.status == "Complete"

    def test_mark_task_to_incomplete(self):
        """Test marking a task as incomplete."""
        from src.mark_handler import mark_task
        from src.task import Task

        task = Task(title="Test task", status="Complete")
        mark_task(task, "Incomplete")
        assert task.status == "Incomplete"

    def test_mark_task_same_status(self):
        """Test marking a task with the same status."""
        from src.mark_handler import mark_task
        from src.task import Task

        task = Task(title="Test task", status="Incomplete")
        mark_task(task, "Incomplete")
        assert task.status == "Incomplete"


class TestFormatMarkSuccess:
    """Tests for the format_mark_success function."""

    def test_format_mark_success(self):
        """Test formatting mark success message."""
        from src.mark_handler import format_mark_success
        from src.task import Task

        task = Task(title="Test task", status="Complete")
        result = format_mark_success(task, "Incomplete")
        assert "Task status updated successfully" in result
        assert "Test task" in result
        assert "Incomplete -> Complete" in result
        assert task.id[:8] in result


class TestMarkIntegration:
    """Integration tests for the mark command."""

    def test_mark_task_complete_success(self):
        """Test successful task status update to complete."""
        from src.storage import TaskList
        from src.update_handler import find_task_by_id

        # Create a task first
        task_list = TaskList()
        task = task_list.add_task("Task to complete", "Test description")

        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "mark", task.id, "--complete"]):
            with patch("sys.stdout", captured):
                from src.main import main
                exit_code = main()

        output = captured.getvalue()
        assert exit_code == 0
        assert "Task status updated successfully" in output
        assert "Complete" in output

        # Verify status was actually updated
        task_list = TaskList()
        updated_task = find_task_by_id(list(task_list), task.id)
        assert updated_task.status == "Complete"

    def test_mark_task_incomplete_success(self):
        """Test successful task status update to incomplete."""
        from src.storage import TaskList

        task_list = TaskList()
        task = task_list.add_task("Task title", "Test description")
        task.status = "Complete"  # Set to complete first

        captured = StringIO()
        with patch.object(sys, "argv", ["main.py", "mark", task.id, "--incomplete"]):
            with patch("sys.stdout", captured):
                from src.main import main
                exit_code = main()

        output = captured.getvalue()
        assert exit_code == 0
        assert "Task status updated successfully" in output
        assert "Incomplete" in output

    def test_mark_invalid_uuid_error(self):
        """Test error for invalid UUID format."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "mark", "invalid-id", "--complete"]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Invalid task ID format" in error_str

    def test_mark_task_not_found_error(self):
        """Test error when task not found."""
        captured = StringIO()
        error_output = StringIO()
        with patch.object(sys, "argv", ["main.py", "mark", "00000000-0000-0000-0000-000000000000", "--complete"]):
            with patch("sys.stdout", captured):
                with patch("sys.stderr", error_output):
                    from src.main import main
                    exit_code = main()

        assert exit_code == 1
        error_str = error_output.getvalue()
        assert "Task not found" in error_str
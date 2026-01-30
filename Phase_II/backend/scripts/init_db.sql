-- Database initialization script for Task CRUD API
-- This script creates the necessary tables for the application

-- Create task table
CREATE TABLE IF NOT EXISTS task (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'Incomplete',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    INDEX (user_id)
);

-- Create index on user_id for fast filtering
CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);

-- Create index on created_at for sorting by age
CREATE INDEX IF NOT EXISTS idx_task_created_at ON task(created_at DESC);

-- Create composite index for common filtering (user_id + status)
CREATE INDEX IF NOT EXISTS idx_task_user_status ON task(user_id, status);

-- Add comment to table
COMMENT ON TABLE task IS 'User tasks for todo management';
COMMENT ON COLUMN task.user_id IS 'Foreign key to user (owner of the task)';
COMMENT ON COLUMN task.title IS 'Task title (required, non-empty)';
COMMENT ON COLUMN task.description IS 'Task description (optional)';
COMMENT ON COLUMN task.status IS 'Task status: Incomplete or Complete';
COMMENT ON COLUMN task.created_at IS 'Timestamp when task was created';
COMMENT ON COLUMN task.updated_at IS 'Timestamp when task was last modified';

// phase_ii/web/components/TaskList.tsx
'use client';

import { Task } from '@/types/task';
import { useState } from 'react';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';

interface TaskListProps {
  initialTasks: Task[];
}

export default function TaskList({ initialTasks }: TaskListProps) {
  // Note: initialTasks comes from server, but actions call revalidatePath so the page refreshes.
  // We don't need local state for the list unless we want optimistic updates (out of scope for now).
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">My Tasks</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={isCreating || !!editingTask}
        >
          Add Task
        </button>
      </div>

      {/* Modal or Inline Form for Create */}
      {isCreating && (
        <div className="mb-6 p-4 border rounded bg-gray-50">
          <h2 className="text-lg font-semibold mb-3 text-black">New Task</h2>
          <TaskForm
            onSuccess={() => setIsCreating(false)}
            onCancel={() => setIsCreating(false)}
          />
        </div>
      )}

      {/* Modal or Inline Form for Edit */}
      {editingTask && (
        <div className="mb-6 p-4 border rounded bg-gray-50">
          <h2 className="text-lg font-semibold mb-3 text-black">Edit Task</h2>
          <TaskForm
            task={editingTask}
            onSuccess={() => setEditingTask(null)}
            onCancel={() => setEditingTask(null)}
          />
        </div>
      )}

      <div className="space-y-4">
        {initialTasks.length === 0 ? (
          <p className="text-center text-gray-500 py-10">No tasks found. Create one to get started!</p>
        ) : (
          initialTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={setEditingTask}
            />
          ))
        )}
      </div>
    </div>
  );
}

// phase_ii/web/components/TaskItem.tsx
'use client';

import { Task } from '@/types/task';
import { deleteTask, updateTaskStatus } from '@/app/actions';
import { useState } from 'react';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
}

export default function TaskItem({ task, onEdit }: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    setIsDeleting(true);
    try {
      await deleteTask(task.id);
    } catch (err) {
      console.error(err);
      alert('Failed to delete task');
    } finally {
      setIsDeleting(false);
    }
  };

  const toggleStatus = async () => {
    setIsUpdatingStatus(true);
    try {
      const newStatus = task.status === 'Complete' ? 'Incomplete' : 'Complete';
      await updateTaskStatus(task.id, newStatus);
    } catch (err) {
      console.error(err);
      alert('Failed to update status');
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  return (
    <div className={`p-4 border rounded shadow-sm flex items-start justify-between bg-white ${task.status === 'Complete' ? 'opacity-75 bg-gray-50' : ''}`}>
      <div className="flex-1">
        <h3 className={`font-semibold text-lg text-black ${task.status === 'Complete' ? 'line-through text-gray-500' : ''}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className="text-gray-600 mt-1 whitespace-pre-wrap text-sm">{task.description}</p>
        )}
        <div className="mt-2 text-xs text-gray-400">
          Created: {new Date(task.created_at).toLocaleDateString()}
        </div>
      </div>

      <div className="flex flex-col gap-2 ml-4">
         <button
          onClick={toggleStatus}
          disabled={isUpdatingStatus}
          className={`px-3 py-1 text-sm rounded ${
            task.status === 'Complete'
              ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
              : 'bg-green-100 text-green-700 hover:bg-green-200'
          }`}
        >
          {task.status === 'Complete' ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button
          onClick={() => onEdit(task)}
          className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </button>
      </div>
    </div>
  );
}

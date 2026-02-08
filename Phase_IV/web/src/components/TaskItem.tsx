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

  const isComplete = task.status === 'Complete';

  const handleDelete = async () => {
    if (!confirm('De-authorize this task record?')) return;
    setIsDeleting(true);
    try {
      await deleteTask(task.id);
    } catch (err) {
      console.error(err);
    } finally {
      setIsDeleting(false);
    }
  };

  const toggleStatus = async () => {
    setIsUpdatingStatus(true);
    try {
      const newStatus = isComplete ? 'Incomplete' : 'Complete';
      await updateTaskStatus(task.id, newStatus);
    } catch (err) {
      console.error(err);
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  return (
    <div className={`group relative overflow-hidden transition-all duration-500 border rounded-xl p-5 
      ${isComplete 
        ? 'bg-black/20 border-emerald-900/20 opacity-60' 
        : 'bg-emerald-950/5 border-emerald-500/20 hover:border-emerald-500/50 shadow-[0_0_20px_-12px_rgba(16,185,129,0.3)]'
      }`}>
      
      {/* Background Glow for Active Tasks */}
      {!isComplete && (
        <div className="absolute -right-20 -top-20 w-40 h-40 bg-emerald-500/5 blur-[50px] pointer-events-none group-hover:bg-emerald-500/10 transition-colors" />
      )}

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
        
        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-2">
            <div className={`h-2 w-2 rounded-full ${isComplete ? 'bg-slate-700' : 'bg-emerald-500 animate-pulse shadow-[0_0_8px_#10b981]'}`} />
            <span className="text-[10px] font-mono tracking-widest text-emerald-500/50 uppercase">
              ID-{task.id.toString().slice(-4)}
            </span>
          </div>

          <h3 className={`text-lg font-bold tracking-tight transition-all ${isComplete ? 'text-slate-500 line-through' : 'text-white'}`}>
            {task.title}
          </h3>

          {task.description && (
            <p className={`mt-2 text-sm leading-relaxed max-w-2xl transition-colors ${isComplete ? 'text-slate-600' : 'text-slate-400'}`}>
              {task.description}
            </p>
          )}

          <div className="mt-4 flex items-center gap-4 text-[10px] font-mono uppercase tracking-tighter text-slate-500">
            <span>Entry: {new Date(task.created_at).toLocaleDateString()}</span>
            <span className="h-1 w-1 bg-slate-800 rounded-full" />
            <span className={isComplete ? 'text-slate-600' : 'text-emerald-500/70'}>
              Status: {task.status}
            </span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2 bg-black/40 p-2 rounded-lg border border-white/5 backdrop-blur-md">
          <button
            onClick={toggleStatus}
            disabled={isUpdatingStatus}
            className={`px-4 py-1.5 text-[10px] font-bold uppercase tracking-widest rounded transition-all
              ${isComplete 
                ? 'bg-slate-800 text-slate-400 hover:bg-slate-700' 
                : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500 hover:text-black'
              }`}
          >
            {isUpdatingStatus ? 'Syncing...' : isComplete ? 'Restore' : 'Complete'}
          </button>

          <button
            onClick={() => onEdit(task)}
            className="p-2 text-slate-400 hover:text-white transition-colors"
            title="Edit Protocol"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          <div className="w-px h-4 bg-white/10 mx-1" />

          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="p-2 text-slate-500 hover:text-red-500 transition-colors"
            title="Terminate"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
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
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  return (
    <div className="w-full">
      {/* --- HEADER SECTION --- */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8 pb-6 border-b border-emerald-500/10">
        <div>
          <h2 className="text-2xl font-black text-white tracking-tight uppercase italic">
            Task <span className="text-emerald-500">Registry</span>
          </h2>
          <p className="text-xs font-mono text-emerald-500/60 uppercase tracking-widest mt-1">
            Total Records: {initialTasks.length.toString().padStart(2, '0')}
          </p>
        </div>

        <button
          onClick={() => setIsCreating(true)}
          disabled={isCreating || !!editingTask}
          className="group relative px-6 py-2 bg-emerald-500 text-black font-bold uppercase text-xs tracking-tighter transition-all hover:bg-emerald-400 disabled:opacity-30 disabled:cursor-not-allowed overflow-hidden"
        >
          {/* Cyber Button Effect */}
          <span className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-white"></span>
          <span className="relative z-10 flex items-center gap-2">
            <span className="text-lg">+</span> Initialize New Task
          </span>
        </button>
      </div>

      {/* --- FORM MODALS / INLINE --- */}
      {(isCreating || editingTask) && (
        <div className="mb-10 relative group">
          {/* Animated border glow for the form */}
          <div className="absolute -inset-0.5 bg-emerald-500/30 rounded-xl blur opacity-75 animate-pulse"></div>
          
          <div className="relative bg-[#0d1117] border border-emerald-500/30 p-6 rounded-xl shadow-2xl backdrop-blur-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="h-4 w-1 bg-emerald-500"></div>
              <h2 className="text-lg font-bold text-white uppercase tracking-tight">
                {isCreating ? 'Primary Directive Entry' : 'Modify Core Task'}
              </h2>
            </div>
            
            <TaskForm
              task={editingTask || undefined}
              onSuccess={() => {
                setIsCreating(false);
                setEditingTask(null);
              }}
              onCancel={() => {
                setIsCreating(false);
                setEditingTask(null);
              }}
            />
          </div>
        </div>
      )}

      {/* --- TASK FEED --- */}
      <div className="grid gap-4">
        {initialTasks.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 border-2 border-dashed border-emerald-500/10 rounded-3xl bg-emerald-500/2">
            <div className="w-12 h-12 rounded-full border border-emerald-500/30 flex items-center justify-center mb-4 animate-pulse">
              <span className="text-emerald-500 text-xl font-mono">!</span>
            </div>
            <p className="text-emerald-500/40 font-mono text-sm uppercase tracking-widest">
              Zero active tasks detected in local cache.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {initialTasks.map((task) => (
              <div 
                key={task.id} 
                className="transition-all duration-300 hover:translate-x-1"
              >
                <TaskItem
                  task={task}
                  onEdit={setEditingTask}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* --- DECORATIVE SIDEBAR ELEMENT (Internal to list) --- */}
      <div className="mt-8 pt-6 border-t border-emerald-500/5 flex justify-between items-center">
        <div className="flex gap-1">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-1 w-4 bg-emerald-500/20 rounded-full"></div>
          ))}
        </div>
        <span className="text-[10px] font-mono text-slate-600 uppercase">Buffer: Synced</span>
      </div>
    </div>
  );
}
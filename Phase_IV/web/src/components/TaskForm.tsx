// phase_ii/web/components/TaskForm.tsx
'use client';

import { useState } from 'react';
import { Task } from '@/types/task';
import { createTask, updateTask } from '@/app/actions';

interface TaskFormProps {
  task?: Task;
  onSuccess: () => void;
  onCancel: () => void;
}

export default function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      if (task) {
        await updateTask(task.id, { title, description });
      } else {
        await createTask({ title, description });
      }
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Neural uplink failed. Try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg text-xs font-mono animate-shake">
          <span className="font-bold mr-2">[CRITICAL_ERROR]</span> {error}
        </div>
      )}

      <div className="space-y-1">
        <label className="text-[10px] font-mono uppercase tracking-[0.2em] text-emerald-500/70 ml-1">
          Directive_Title
        </label>
        <div className="relative group">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={255}
            placeholder="Enter task designation..."
            className="w-full bg-black/40 border border-emerald-500/20 rounded-lg p-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all font-mono text-sm"
          />
          {/* Decorative corner accent */}
          <div className="absolute top-0 right-0 w-1 h-1 bg-emerald-500 opacity-0 group-focus-within:opacity-100 transition-opacity" />
        </div>
      </div>

      <div className="space-y-1">
        <label className="text-[10px] font-mono uppercase tracking-[0.2em] text-emerald-500/70 ml-1">
          Parameter_Details
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={2000}
          rows={4}
          placeholder="Input additional telemetry data..."
          className="w-full bg-black/40 border border-emerald-500/20 rounded-lg p-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all font-mono text-sm resize-none"
        />
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-emerald-500/10">
        <div className="hidden md:block text-[9px] font-mono text-slate-600 uppercase tracking-widest">
          Secured Protocol: AES-256
        </div>
        
        <div className="flex gap-3 w-full md:w-auto">
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 md:flex-none px-6 py-2 text-[10px] font-bold uppercase tracking-widest text-slate-400 hover:text-white transition-colors border border-transparent hover:border-slate-800 rounded-lg"
          >
            Abort
          </button>
          
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 md:flex-none relative px-8 py-2 bg-emerald-600 text-black font-black uppercase text-[10px] tracking-[0.15em] rounded-lg hover:bg-emerald-400 disabled:opacity-30 disabled:grayscale transition-all shadow-[0_0_20px_rgba(16,185,129,0.2)]"
          >
            {isSubmitting ? (
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 border-2 border-black border-t-transparent rounded-full animate-spin" />
                Processing...
              </span>
            ) : (
              task ? 'Commit Changes' : 'Execute Creation'
            )}
          </button>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-4px); }
          75% { transform: translateX(4px); }
        }
        .animate-shake { animation: shake 0.2s ease-in-out 0s 2; }
      `}} />
    </form>
  );
}
// phase_ii/web/src/app/tasks/page.tsx
import { getTasks } from '@/lib/api';
import TaskList from '@/components/TaskList';
import SignOutButton from '@/components/SignOutButton';
import ChatWidget from '@/components/ChatWidget';
import { Task } from '@/types/task';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

export const dynamic = 'force-dynamic';

export default async function TasksPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  if (!session?.user) {
    redirect('/signin');
  }

  let tasks: Task[] = [];
  try {
    tasks = await getTasks();
  } catch(e) {
    console.error("Failed to fetch tasks", e);
  }

  return (
    <div className="relative min-h-screen bg-[#020617] text-slate-200 selection:bg-emerald-500/40 selection:text-white overflow-hidden">
      
      {/* --- ADVANCED AI BACKGROUND --- */}
      <div className="fixed inset-0 z-0">
        {/* Deep Gradient Radial Base */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,#064e3b20_0%,transparent_50%)]" />
        
        {/* Animated Scanning Line - Using arbitrary values to avoid styled-jsx error */}
        <div className="absolute inset-0 opacity-[0.05] pointer-events-none bg-[linear-gradient(transparent_0%,#10b981_50%,transparent_100%)] bg-[length:100%_200px] animate-[pulse_8s_linear_infinite]" 
             style={{ animation: 'scan 10s linear infinite' }} />
        
        {/* Geometric Grid */}
        <div 
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `linear-gradient(#10b981 1px, transparent 1px), linear-gradient(90deg, #10b981 1px, transparent 1px)`,
            backgroundSize: '45px 45px',
            maskImage: 'radial-gradient(ellipse at center, black, transparent 90%)'
          }}
        />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-8">
        
        {/* --- PROFESSIONAL HEADER --- */}
        <header className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12 border-b border-emerald-500/10 pb-8">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-[10px] uppercase tracking-[0.4em] text-emerald-500 font-bold">Neural Link Active</span>
            </div>
            <h1 className="text-4xl md:text-6xl font-black tracking-tighter italic uppercase text-white">
              Core<span className="text-emerald-500 drop-shadow-[0_0_10px_rgba(16,185,129,0.5)]">Tasks</span>
            </h1>
          </div>

          <div className="flex items-center gap-6 bg-emerald-950/30 border border-emerald-500/20 px-6 py-3 rounded-xl backdrop-blur-xl shadow-2xl">
            <div className="text-right">
              <p className="text-[9px] uppercase text-emerald-500/50 font-bold leading-none mb-1">Authenticated User</p>
              <p className="text-white font-mono text-sm tracking-tighter">{session.user.name || 'Anonymous'}</p>
            </div>
            <div className="h-8 w-[1px] bg-emerald-500/20" />
            
          </div>
        </header>

        {/* --- MAIN INTERFACE --- */}
        <main className="grid grid-cols-1 gap-8">
          <div className="relative group">
            {/* The "AI Glow" backdrop */}
            <div className="absolute -inset-1 bg-gradient-to-r from-emerald-600/20 to-emerald-900/20 rounded-[2rem] blur-2xl opacity-50 group-hover:opacity-100 transition duration-1000"></div>
            
            <div className="relative bg-[#070c18]/90 backdrop-blur-3xl rounded-[1.5rem] border border-emerald-500/10 shadow-[0_0_50px_-12px_rgba(0,0,0,0.5)] overflow-hidden">
              {/* Top Accent Line */}
              <div className="h-[2px] w-full bg-gradient-to-r from-transparent via-emerald-500/50 to-transparent" />
              
              <div className="p-2 md:p-6">
                <TaskList initialTasks={tasks} />
              </div>
            </div>
          </div>
        </main>

        <footer className="mt-20 flex flex-col items-center gap-4 opacity-40">
           <div className="h-[1px] w-24 bg-gradient-to-r from-transparent via-emerald-500 to-transparent" />
           <div className="flex gap-10 text-[9px] font-mono uppercase tracking-[0.2em] text-emerald-500">
             <span className="flex items-center gap-2"><span className="w-1 h-1 bg-emerald-500 rounded-full animate-pulse" /> Encrypted</span>
             <span>Node: v2.2.0-secure</span>
             <span>TX-Ready</span>
           </div>
        </footer>
      </div>

      <ChatWidget />

      {/* Injecting the keyframes via a standard <style> tag to bypass the client-only error */}
      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes scan {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(100vh); }
        }
      `}} />
    </div>
  );
}
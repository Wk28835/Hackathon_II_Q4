// phase_ii/web/src/app/page.tsx
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import Link from "next/link";

export default async function Home() {
  const session = await auth.api.getSession({
    headers: await headers()
  });

  return (
    <div className="relative min-h-screen bg-[#020617] text-white overflow-hidden flex flex-col items-center">
      
      {/* --- BACKGROUND ARCHITECTURE --- */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_-20%,#10b98115_0%,transparent_50%)]" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-50 mix-blend-overlay" />
        <div 
          className="absolute inset-0 opacity-[0.15]"
          style={{
            backgroundImage: `linear-gradient(#10b981 1px, transparent 1px), linear-gradient(90deg, #10b981 1px, transparent 1px)`,
            backgroundSize: '60px 60px',
            maskImage: 'linear-gradient(to bottom, black, transparent)'
          }}
        />
      </div>

      {/* --- HERO SECTION --- */}
      <main className="relative z-10 w-full max-w-6xl px-6 pt-12 pb-20 flex flex-col items-center text-center">
        
        {/* Tech Badges */}
        <div className="flex flex-wrap justify-center gap-3 mb-8 animate-in fade-in slide-in-from-top-4 duration-1000">
          {['Gemini 1.5 Pro', 'MCP Architecture', 'FastAPI', 'BetterAuth'].map((tech) => (
            <span key={tech} className="px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/5 text-[10px] font-mono text-emerald-400 uppercase tracking-widest">
              {tech}
            </span>
          ))}
        </div>

        <h1 className="text-5xl md:text-8xl font-black tracking-tighter italic uppercase mb-6 leading-none">
          Neural<span className="text-emerald-500 drop-shadow-[0_0_15px_rgba(16,185,129,0.4)]">Task</span><br/>Intelligence
        </h1>
        
        <p className="max-w-2xl text-slate-400 text-lg md:text-xl font-light leading-relaxed mb-10">
          The next evolution of productivity. A seamless fusion of <span className="text-white font-semibold">Gemini AI</span> and 
          <span className="text-white font-semibold"> Model Context Protocol</span> designed to manage your directives 
          through natural language and autonomous execution.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link 
            href={session ? "/tasks" : "/signin"}
            className="px-10 py-4 bg-emerald-500 text-black font-black uppercase text-sm tracking-widest rounded-full hover:bg-emerald-400 transition-all hover:scale-105 shadow-[0_0_30px_rgba(16,185,129,0.3)]"
          >
            {session ? "Enter Dashboard" : "Initialize Session"}
          </Link>
          {!session && (
            <Link 
              href="/signup"
              className="px-10 py-4 bg-transparent border border-white/10 text-white font-bold uppercase text-sm tracking-widest rounded-full hover:bg-white/5 transition-all"
            >
              Create Identity
            </Link>
          )}
        </div>
      </main>

      {/* --- FEATURE GRID --- */}
      <section className="relative z-10 w-full max-w-6xl px-6 py-20 border-t border-white/5">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Card 1: Task Management */}
          <div className="group p-8 rounded-3xl bg-white/2 border border-white/5 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-6 text-emerald-500">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            </div>
            <h3 className="text-xl font-bold mb-3 uppercase italic tracking-tight">Advanced Registry</h3>
            <p className="text-slate-500 text-sm leading-relaxed">Structured task management with high-performance FastAPI backends for sub-millisecond persistence.</p>
          </div>

          {/* Card 2: AI Chatbot */}
          <div className="group p-8 rounded-3xl bg-white/2 border border-white/5 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center mb-6 text-blue-400">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
            </div>
            <h3 className="text-xl font-bold mb-3 uppercase italic tracking-tight">Neural Link</h3>
            <p className="text-slate-500 text-sm leading-relaxed">Integrated Gemini 2.5 Pro assistant capable of creating, updating, and querying your tasks through natural dialogue.</p>
          </div>

          {/* Card 3: MCP */}
          <div className="group p-8 rounded-3xl bg-white/2 border border-white/5 hover:border-emerald-500/30 transition-all">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mb-6 text-purple-400">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
            <h3 className="text-xl font-bold mb-3 uppercase italic tracking-tight">MCP Protocol</h3>
            <p className="text-slate-500 text-sm leading-relaxed">Leveraging Model Context Protocol to bridge the gap between AI reasoning and your local application data.</p>
          </div>

        </div>
      </section>

      {/* --- TECH SPECS FOOTER (Visual Only) --- */}
      <div className="relative z-10 w-full py-10 opacity-20 grayscale pointer-events-none overflow-hidden whitespace-nowrap">
        <div className="flex gap-20 animate-marquee text-[10px] font-mono uppercase tracking-[0.5em]">
          <span>FastAPI Endpoint Connected</span>
          <span>BetterAuth Session Active</span>
          <span>Gemini-1.5-Pro Token: Valid</span>
          <span>MCP Server Node: Online</span>
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}} />
    </div>
  );
}
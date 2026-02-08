// src/app/signin/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signIn } from '@/lib/auth-client';

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const result = await signIn.email({
        email,
        password,
      });

      if (result.error) {
        setError(result.error.message || 'Access Denied: Invalid Credentials');
      } else {
        router.push('/tasks');
        router.refresh();
      }
    } catch (err) {
      setError('Uplink Interrupted: System error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-[#020617] py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      
      {/* AI TECH BACKGROUND */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,#064e3b15_0%,transparent_70%)]" />
        <div 
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `linear-gradient(#10b981 1px, transparent 1px), linear-gradient(90deg, #10b981 1px, transparent 1px)`,
            backgroundSize: '40px 40px',
            maskImage: 'radial-gradient(ellipse at center, black, transparent 80%)'
          }}
        />
      </div>

      {/* LOGIN CARD */}
      <div className="relative z-10 max-w-md w-full">
        <div className="bg-black/60 backdrop-blur-3xl p-8 rounded-3xl border border-emerald-500/20 shadow-[0_0_50px_-12px_rgba(16,185,129,0.3)]">
          
          <div className="text-center mb-10">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 mb-4">
              <div className="w-6 h-6 border-2 border-emerald-500 rounded-sm animate-pulse" />
            </div>
            <h2 className="text-3xl font-black tracking-tighter text-white uppercase italic">
              Task<span className="text-emerald-500">Manager</span>
            </h2>
            <p className="mt-2 text-sm font-mono text-emerald-500/60 tracking-widest uppercase">
              Identify yourself, Operator
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-3 rounded-lg text-[10px] font-mono uppercase tracking-tight animate-shake">
                <span className="font-bold">[!] ERROR:</span> {error}
              </div>
            )}

            <div className="space-y-4">
              <div className="group">
                <label htmlFor="email" className="block text-[10px] font-mono text-emerald-500/50 uppercase tracking-widest mb-1 ml-1">
                  Neural_Identity (Email)
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-800 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="name@nexus.com"
                />
              </div>

              <div className="group">
                <label htmlFor="password" className="block text-[10px] font-mono text-emerald-500/50 uppercase tracking-widest mb-1 ml-1">
                  Access_Key (Password)
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-800 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-3 px-4 bg-emerald-600 text-black text-xs font-black uppercase tracking-[0.2em] rounded-xl hover:bg-emerald-400 disabled:opacity-30 transition-all shadow-[0_0_20px_rgba(16,185,129,0.2)]"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="w-3 h-3 border-2 border-black border-t-transparent rounded-full animate-spin" />
                    Authenticating...
                  </span>
                ) : 'Establish Link'}
              </button>
            </div>
          </form>

          <div className="mt-8 text-center">
            <p className="text-xs font-mono text-slate-500 uppercase tracking-tighter">
              New to the Nexus?{' '}
              <Link href="/signup" className="text-emerald-500 hover:text-emerald-400 font-bold transition-colors">
                Initialize Account
              </Link>
            </p>
          </div>
        </div>
        
        {/* Footer info for that extra "Pro" feel */}
        <div className="mt-8 flex justify-between px-4 opacity-20 text-[9px] font-mono uppercase tracking-[0.2em] text-emerald-500">
          <span>Encrypted_Uplink</span>
          <span>v2.2.0</span>
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
    </div>
  );
}
// src/app/signup/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signUp } from '@/lib/auth-client';

export default function SignUpPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Neural Key Mismatch: Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Insecure Key: Minimum 6 characters required');
      return;
    }

    setIsLoading(true);

    try {
      const result = await signUp.email({
        email,
        password,
        name,
      });

      if (result.error) {
        setError(result.error.message || 'Initialization Failed');
      } else {
        router.push('/tasks');
        router.refresh();
      }
    } catch (err) {
      setError('Uplink Error: Connection timed out');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-[#020617] py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      
      {/* BACKGROUND ELEMENTS */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,#064e3b15_0%,transparent_70%)]" />
        <div 
          className="absolute inset-0 opacity-5"
          style={{
            backgroundImage: `repeating-linear-gradient(0deg, #10b981 0px, transparent 1px, transparent 40px)`,
            backgroundSize: '100% 40px',
          }}
        />
      </div>

      <div className="relative z-10 max-w-md w-full">
        <div className="bg-black/60 backdrop-blur-3xl p-8 rounded-3xl border border-emerald-500/20 shadow-[0_0_50px_-12px_rgba(16,185,129,0.3)]">
          
          <div className="text-center mb-8">
            <h2 className="text-3xl font-black tracking-tighter text-white uppercase italic">
              New<span className="text-emerald-500">Identity</span>
            </h2>
            <p className="mt-2 text-[10px] font-mono text-emerald-500/60 tracking-[0.3em] uppercase">
              Register Neural Signature
            </p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-500/10 border border-red-500/40 text-red-400 p-3 rounded-xl text-[10px] font-mono uppercase animate-pulse">
                [!] CRITICAL_ERROR: {error}
              </div>
            )}

            <div className="space-y-3">
              <div className="group">
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="FULL_NAME"
                />
              </div>

              <div className="group">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="EMAIL_ADDRESS"
                />
              </div>

              <div className="group">
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="ACCESS_KEY"
                />
              </div>

              <div className="group">
                <input
                  type="password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full bg-black/40 border border-emerald-500/20 rounded-xl px-4 py-3 text-white placeholder:text-slate-700 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20 transition-all font-mono text-sm"
                  placeholder="CONFIRM_KEY"
                />
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-4 bg-emerald-600 text-black text-xs font-black uppercase tracking-[0.2em] rounded-xl hover:bg-emerald-400 disabled:opacity-30 transition-all shadow-[0_0_20px_rgba(16,185,129,0.2)]"
              >
                {isLoading ? 'Creating Index...' : 'Initialize Identity'}
              </button>
            </div>
          </form>

          <div className="mt-8 text-center">
            <p className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">
              Existing Operator?{' '}
              <Link href="/signin" className="text-emerald-500 hover:text-emerald-400 font-bold transition-colors">
                Return to Login
              </Link>
            </p>
          </div>
        </div>
        
        <div className="mt-6 text-center opacity-20">
          <p className="text-[9px] font-mono text-emerald-500 uppercase tracking-[0.4em]">
            Security_Protocol_Active // RSA_4096
          </p>
        </div>
      </div>
    </div>
  );
}
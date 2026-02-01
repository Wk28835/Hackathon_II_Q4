// phase_ii/web/components/Navbar.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import SignOutButton from './SignOutButton';
import { useSession } from '@/lib/auth-client'; // Import the session hook

export default function Navbar() {
  const pathname = usePathname();
  const { data: session, isPending } = useSession(); // Access user data

  const navLinks = [
    { name: 'Home', href: '/' },
    { name: 'Tasks', href: '/tasks' },
    { name: 'Neural_Chat', href: '/chat' },
  ];

  return (
    <nav className="sticky top-0 z-100 w-full border-b border-emerald-500/10 bg-[#020617]/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          
          {/* Logo Section */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-6 h-6 bg-emerald-500 rounded-sm rotate-45 flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.4)] transition-transform group-hover:scale-110">
              <div className="w-2 h-2 bg-black rounded-full animate-pulse" />
            </div>
            <span className="text-white font-black tracking-tighter uppercase italic hidden sm:block">
              Nexus<span className="text-emerald-500">OS</span>
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center gap-1 sm:gap-6">
            {navLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-3 py-1.5 text-[10px] sm:text-xs font-mono uppercase tracking-widest transition-all rounded-md border ${
                    isActive 
                      ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.1)]' 
                      : 'border-transparent text-slate-500 hover:text-emerald-400 hover:border-emerald-500/20'
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </div>

          {/* Action Section: Conditional Auth UI */}
          <div className="flex items-center gap-4 pl-4 border-l border-emerald-500/10">
            {isPending ? (
              // Loading State (Prevents layout shift)
              <div className="w-20 h-4 bg-emerald-500/10 animate-pulse rounded" />
            ) : session?.user ? (
              // Logged In State
              <div className="flex items-center gap-4">
                <div className="hidden md:flex flex-col items-end">
                  <span className="text-[9px] font-mono text-emerald-500/50 uppercase tracking-tighter">Operator_Active</span>
                  <span className="text-[11px] font-mono text-white tracking-tight">{session.user.name}</span>
                </div>
                <SignOutButton />
              </div>
            ) : (
              // Logged Out State
              <Link 
                href="/signin" 
                className="px-4 py-1.5 bg-emerald-500 text-black text-[10px] font-black uppercase tracking-widest rounded hover:bg-emerald-400 transition-all shadow-[0_0_15px_rgba(16,185,129,0.2)]"
              >
                Sign_In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
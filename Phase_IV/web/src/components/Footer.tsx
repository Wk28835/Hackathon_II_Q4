// phase_ii/web/components/Footer.tsx
export default function Footer() {
  const year = new Date().getFullYear();
  
  return (
    <footer className="w-full py-10 border-t border-emerald-500/5 bg-[#020617] mt-auto">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          
          {/* Status Indicators */}
          <div className="flex gap-6 justify-center md:justify-start">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[9px] font-mono uppercase text-slate-500 tracking-[0.2em]">Node_Active</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
              <span className="text-[9px] font-mono uppercase text-slate-500 tracking-[0.2em]">DB_Synced</span>
            </div>
          </div>

          {/* Copyright Section */}
          <div className="text-center">
            <p className="text-[10px] font-mono text-slate-600 uppercase tracking-widest">
              &copy; {year} Nexus Intelligence Systems // All Rights Reserved
            </p>
          </div>

          {/* Version / Metadata */}
          <div className="flex justify-center md:justify-end gap-4 text-[9px] font-mono text-emerald-500/30">
            <span>SECURE_LAYER: v4.2</span>
            <span className="text-slate-800">|</span>
            <span>UPLINK: STABLE</span>
          </div>
        </div>
        
        {/* Decorative Bottom Bar */}
        <div className="mt-8 h-0.5 w-full bg-liner-to-r from-transparent via-emerald-500/20 to-transparent" />
      </div>
    </footer>
  );
}
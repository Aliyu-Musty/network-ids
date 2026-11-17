import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { ShieldAlert, LogOut, User } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 sticky top-0 z-40">
      <div className="flex items-center space-x-3">
        <ShieldAlert className="h-7 w-7 text-indigo-500 animate-pulse" />
        <span className="font-bold text-lg tracking-wide text-slate-100">
          NIDS <span className="text-indigo-400 font-medium text-sm">Real-Time Monitor</span>
        </span>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-sm text-slate-300 bg-slate-800/80 py-1.5 px-3 rounded-full border border-slate-700">
          <User className="h-4 w-4 text-indigo-400" />
          <span>{user?.full_name || 'Security Analyst'}</span>
        </div>

        <button
          onClick={logout}
          className="flex items-center space-x-1 text-sm text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 px-3 py-1.5 rounded-md transition"
        >
          <LogOut className="h-4 w-4" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
};

export default Navbar;

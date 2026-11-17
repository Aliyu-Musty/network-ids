import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, AlertTriangle, Activity, Settings } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Alerts History', path: '/alerts', icon: AlertTriangle },
    { name: 'Traffic Analytics', path: '/analytics', icon: Activity },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between">
      <nav className="space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>

      <div className="bg-slate-800/60 border border-slate-700/60 p-3 rounded-lg text-xs text-slate-400 space-y-1">
        <div className="flex items-center justify-between">
          <span>Engine:</span>
          <span className="text-emerald-400 font-medium">XGBoost Active</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Sniffer:</span>
          <span className="text-emerald-400 font-medium">Scapy Live</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;

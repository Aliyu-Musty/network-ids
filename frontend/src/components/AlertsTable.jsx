import React from 'react';

const AlertsTable = ({ alerts = [] }) => {
  const getSeverityBadge = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">MEDIUM</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">LOW</span>;
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm text-slate-300">
        <thead className="bg-slate-800/60 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-700">
          <tr>
            <th className="px-4 py-3">Time</th>
            <th className="px-4 py-3">Attack Type</th>
            <th className="px-4 py-3">Severity</th>
            <th className="px-4 py-3">Source IP</th>
            <th className="px-4 py-3">Destination IP</th>
            <th className="px-4 py-3">Protocol</th>
            <th className="px-4 py-3">Confidence</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {alerts.length === 0 ? (
            <tr>
              <td colSpan="7" className="text-center py-8 text-slate-500 italic">
                No active attack alerts detected. Network traffic is normal.
              </td>
            </tr>
          ) : (
            alerts.map((alert, idx) => (
              <tr key={alert.id || idx} className="hover:bg-slate-800/40 transition">
                <td className="px-4 py-3 text-xs text-slate-400">
                  {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString() : 'Just now'}
                </td>
                <td className="px-4 py-3 font-medium text-slate-200">
                  {alert.attack_type}
                </td>
                <td className="px-4 py-3">{getSeverityBadge(alert.severity)}</td>
                <td className="px-4 py-3 font-mono text-xs text-indigo-300">{alert.src_ip}</td>
                <td className="px-4 py-3 font-mono text-xs text-slate-300">{alert.dst_ip}</td>
                <td className="px-4 py-3 text-xs">{alert.protocol}</td>
                <td className="px-4 py-3 text-xs font-semibold text-slate-300">
                  {(alert.confidence * 100).toFixed(1)}%
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default AlertsTable;

import React, { useState, useEffect } from 'react';
import StatCard from '../components/StatCard';
import LiveTrafficChart from '../components/LiveTrafficChart';
import AlertsTable from '../components/AlertsTable';
import { LiveAlertSocket } from '../services/websocket';
import api from '../services/api';
import { ShieldCheck, AlertOctagon, Activity, Radio } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_packets: 0,
    total_attacks: 0,
    critical_alerts: 0,
    active_threats: 0,
  });

  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState([
    { time: '12:00', packets: 400, attacks: 2 },
    { time: '12:05', packets: 520, attacks: 5 },
    { time: '12:10', packets: 600, attacks: 1 },
    { time: '12:15', packets: 750, attacks: 8 },
    { time: '12:20', packets: 820, attacks: 3 },
  ]);

  useEffect(() => {
    // Fetch initial stats and recent alerts
    const fetchData = async () => {
      try {
        const statsRes = await api.get('/traffic/stats');
        setStats(statsRes.data);

        const alertsRes = await api.get('/alerts/?limit=10');
        setAlerts(alertsRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      }
    };
    fetchData();

    // Connect to WebSocket for live incoming alerts
    const socket = new LiveAlertSocket((newAlert) => {
      setAlerts((prev) => [newAlert, ...prev.slice(0, 19)]);
      if (newAlert.is_attack) {
        setStats((prev) => ({
          ...prev,
          total_attacks: prev.total_attacks + 1,
          critical_alerts: newAlert.severity === 'CRITICAL' ? prev.critical_alerts + 1 : prev.critical_alerts,
        }));
      }
    });

    socket.connect();
    return () => socket.disconnect();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <span>Real-Time Security Operations</span>
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
          </h1>
          <p className="text-sm text-slate-400">Scapy packet sniffer and XGBoost classification active.</p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700 text-slate-300">
          <Radio className="h-4 w-4 text-emerald-400 animate-pulse" />
          <span>LISTENING ON ALL INTERFACES</span>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard title="Total Packets Monitored" value={stats.total_packets.toLocaleString()} icon={Activity} color="indigo" />
        <StatCard title="Total Attacks Flagged" value={stats.total_attacks.toLocaleString()} icon={AlertOctagon} color="rose" />
        <StatCard title="Critical Severity Alerts" value={stats.critical_alerts.toLocaleString()} icon={ShieldCheck} color="amber" />
        <StatCard title="Active Live Threats" value={stats.active_threats.toLocaleString()} icon={Radio} color="emerald" />
      </div>

      {/* Real-time Traffic Graph */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-slate-200">Live Traffic & Threat Volume</h2>
          <span className="text-xs text-slate-500">Flow window: 5s intervals</span>
        </div>
        <LiveTrafficChart data={chartData} />
      </div>

      {/* Live Alerts Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-slate-200">Recent Detected Threats</h2>
          <span className="text-xs text-indigo-400 font-medium">Real-Time Stream Active</span>
        </div>
        <AlertsTable alerts={alerts} />
      </div>
    </div>
  );
};

export default Dashboard;

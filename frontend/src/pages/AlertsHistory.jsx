import React, { useState, useEffect } from 'react';
import AlertsTable from '../components/AlertsTable';
import api from '../services/api';
import { Search, Filter, Download } from 'lucide-react';

const AlertsHistory = () => {
  const [alerts, setAlerts] = useState([]);
  const [severityFilter, setSeverityFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        let endpoint = '/alerts/?limit=100';
        if (severityFilter) endpoint += `&severity=${severityFilter}`;
        const res = await api.get(endpoint);
        setAlerts(res.data);
      } catch (err) {
        console.error('Failed to load alert history:', err);
      }
    };
    fetchAlerts();
  }, [severityFilter]);

  const filteredAlerts = alerts.filter(
    (a) =>
      a.attack_type?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.src_ip?.includes(searchQuery) ||
      a.dst_ip?.includes(searchQuery)
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <div>
          <h1 className="text-xl font-bold text-slate-100">Historical Attack Logs</h1>
          <p className="text-sm text-slate-400">Search, filter, and review all previous intrusion detections.</p>
        </div>

        <button className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2 rounded-lg text-sm border border-slate-700 transition">
          <Download className="h-4 w-4" />
          <span>Export CSV</span>
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 justify-between">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search by IP or attack type..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex items-center space-x-3">
            <Filter className="h-4 w-4 text-slate-400" />
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-indigo-500"
            >
              <option value="">All Severities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
        </div>

        {/* Table */}
        <AlertsTable alerts={filteredAlerts} />
      </div>
    </div>
  );
};

export default AlertsHistory;

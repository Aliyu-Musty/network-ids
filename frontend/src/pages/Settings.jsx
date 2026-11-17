import React, { useState } from 'react';
import { Sliders, Save, Cpu, HardDrive } from 'lucide-react';

const Settings = () => {
  const [interfaceName, setInterfaceName] = useState('Wi-Fi (Default)');
  const [threshold, setThreshold] = useState(0.75);
  const [autoBlock, setAutoBlock] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
        <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
          <Sliders className="h-5 w-5 text-indigo-400" />
          <span>System & Detection Configuration</span>
        </h1>
        <p className="text-sm text-slate-400 mt-1">Configure packet sniffer thresholds and ML classification limits.</p>
      </div>

      <form onSubmit={handleSave} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Network Sniffer Interface
          </label>
          <input
            type="text"
            value={interfaceName}
            onChange={(e) => setInterfaceName(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
          <p className="text-xs text-slate-500 mt-1">Leave empty to allow Scapy to listen on default active network adapter.</p>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-sm font-medium text-slate-300">
              XGBoost Threat Confidence Threshold: {(threshold * 100).toFixed(0)}%
            </label>
          </div>
          <input
            type="range"
            min="0.5"
            max="0.99"
            step="0.01"
            value={threshold}
            onChange={(e) => setThreshold(parseFloat(e.target.value))}
            className="w-full accent-indigo-500"
          />
          <p className="text-xs text-slate-500 mt-1">Only predictions with confidence above this value trigger security alerts.</p>
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <input
            type="checkbox"
            id="autoblock"
            checked={autoBlock}
            onChange={(e) => setAutoBlock(e.target.checked)}
            className="rounded bg-slate-950 border-slate-800 text-indigo-600 focus:ring-indigo-500 h-4 w-4"
          />
          <label htmlFor="autoblock" className="text-sm text-slate-300">
            Enable Experimental Automated IP Firewall Blocking for Critical Severity
          </label>
        </div>

        {saved && (
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 text-sm">
            Configuration successfully updated.
          </div>
        )}

        <div className="pt-4 border-t border-slate-800">
          <button
            type="submit"
            className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-5 py-2.5 rounded-lg text-sm transition shadow-lg shadow-indigo-600/30"
          >
            <Save className="h-4 w-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default Settings;

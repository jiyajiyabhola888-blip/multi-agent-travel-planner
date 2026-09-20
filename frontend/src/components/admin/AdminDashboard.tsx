import React from 'react';
import { ShieldCheck, Activity, Users, MapPin, Sparkles, Database, CheckCircle2, ArrowLeft } from 'lucide-react';

interface AdminDashboardProps {
  onBack?: () => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ onBack }) => {
  return (
    <div className="max-w-6xl mx-auto my-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="badge-pink text-xs font-bold">Platform Governance</span>
            <span className="badge-green text-xs font-bold">Systems Operational</span>
          </div>
          <h1 className="text-3xl font-extrabold text-navy-900 mt-2">Admin Control & Agent Telemetry</h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time monitoring of multi-agent debate consensus, global destination catalogs, and guide verifications.
          </p>
        </div>
        {onBack && (
          <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
        )}
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="card-clean p-5 bg-white border border-slate-100">
          <span className="text-xs font-bold text-slate-400 block uppercase">Active AI Agents</span>
          <span className="text-2xl font-extrabold text-brand-600 mt-1 block">15/15</span>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">100% Online</span>
        </div>

        <div className="card-clean p-5 bg-white border border-slate-100">
          <span className="text-xs font-bold text-slate-400 block uppercase">Debate Consensus</span>
          <span className="text-2xl font-extrabold text-navy-900 mt-1 block">98.4%</span>
          <span className="text-[11px] text-slate-500 mt-1 block">Judge Agent Arbiter</span>
        </div>

        <div className="card-clean p-5 bg-white border border-slate-100">
          <span className="text-xs font-bold text-slate-400 block uppercase">India States & UTs</span>
          <span className="text-2xl font-extrabold text-navy-900 mt-1 block">36/36</span>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">Full National Scale</span>
        </div>

        <div className="card-clean p-5 bg-white border border-slate-100">
          <span className="text-xs font-bold text-slate-400 block uppercase">Verified Local Guides</span>
          <span className="text-2xl font-extrabold text-pink-600 mt-1 block">24 Vetted</span>
          <span className="text-[11px] text-slate-500 mt-1 block">0 Pending Review</span>
        </div>
      </div>

      {/* 15 Agent Health & Status Overview */}
      <div className="card-clean p-6 bg-white border border-slate-100 shadow-soft space-y-4">
        <h3 className="font-bold text-base text-navy-900">15 Specialized Agents Health Check</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          {[
            '1. Preference Agent (Active)',
            '2. Destination Agent (Active)',
            '3. Route Agent (Active)',
            '4. Budget Agent (Active)',
            '5. Stay Agent (Active)',
            '6. Food Agent (Active)',
            '7. Weather Agent (Active)',
            '8. Experience Agent (Active)',
            '9. Risk Agent (Active)',
            '10. Group Conflict Agent (Active)',
            '11. Booking Agent (Active)',
            '12. Simulation Agent (Active)',
            '13. Recovery Agent (Active)',
            '14. Explainability Agent (Active)',
            '15. Judge Agent Arbiter (Active)',
          ].map((agent, i) => (
            <div key={i} className="p-3 bg-surface-50 rounded-xl flex items-center justify-between">
              <span className="font-semibold text-slate-700">{agent}</span>
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

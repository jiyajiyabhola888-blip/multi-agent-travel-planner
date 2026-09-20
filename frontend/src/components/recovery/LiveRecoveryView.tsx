import React, { useState } from 'react';
import { RotateCcw, AlertTriangle, CheckCircle2, ArrowLeft, ArrowRight, Sparkles, ShieldCheck } from 'lucide-react';
import { TripResponse } from '../../types';

interface LiveRecoveryViewProps {
  trip: TripResponse;
  onApplyRecovery: () => void;
  onBack: () => void;
}

export const LiveRecoveryView: React.FC<LiveRecoveryViewProps> = ({ trip, onApplyRecovery, onBack }) => {
  const [incident, setIncident] = useState<string>('train_cancelled');
  const [isReplanning, setIsReplanning] = useState<boolean>(false);
  const [replanDone, setReplanDone] = useState<boolean>(true);

  const incidents = [
    { id: 'train_cancelled', label: 'Train / Transit Cancelled', desc: 'Auto-swaps rail with on-demand express cab and preserves dining reservations.' },
    { id: 'severe_rain', label: 'Sudden Heavy Rainstorm', desc: 'Diverts outdoor sights to covered royal galleries and palace courtyards.' },
    { id: 'flight_delay', label: 'Flight Landing Delayed 2+ Hrs', desc: 'Fast-tracks check-in and shifts morning sightseeing to golden hour sunset.' },
    { id: 'venue_shut', label: 'Monument Unexpectedly Closed', desc: 'Substitutes with top-tier neighboring heritage museum within 1.5km.' }
  ];

  const handleSimulateIncident = (incId: string) => {
    setIncident(incId);
    setIsReplanning(true);
    setTimeout(() => {
      setIsReplanning(false);
      setReplanDone(true);
    }, 600);
  };

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 sm:px-6 space-y-6">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="badge-pink text-xs font-bold">Autonomous Recovery</span>
              <span className="badge-green text-xs font-bold">Surgical Re-planning</span>
            </div>
            <h1 className="text-3xl font-extrabold text-navy-900 mt-2">Live Trip Recovery Engine</h1>
            <p className="text-sm text-slate-500 mt-1">
              Select an in-trip incident below. Recovery Agent will recalculate only affected legs while preserving the rest of your vacation.
            </p>
          </div>
          <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
        </div>

        {/* Incident Trigger Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-6 pt-6 border-t border-slate-100">
          {incidents.map(inc => (
            <div
              key={inc.id}
              onClick={() => handleSimulateIncident(inc.id)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${
                incident === inc.id
                  ? 'border-rose-500 bg-rose-50/50 shadow-soft ring-2 ring-rose-200'
                  : 'border-slate-200 hover:bg-surface-50'
              }`}
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className={`w-4 h-4 ${incident === inc.id ? 'text-rose-600' : 'text-slate-400'}`} />
                <h4 className="font-bold text-xs text-navy-900">{inc.label}</h4>
              </div>
              <p className="text-[11px] text-slate-500 mt-1 leading-snug">{inc.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Recovery Plan Diff */}
      {replanDone && (
        <div className="card-clean p-6 bg-gradient-to-br from-white via-brand-50/30 to-blush-50/30 border border-brand-200 shadow-soft-lg space-y-6">
          <div className="flex items-center justify-between pb-4 border-b border-brand-100">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-brand-600" />
              <h3 className="font-bold text-lg text-navy-900">Surgical Recovery Solution</h3>
            </div>
            <span className="badge-green text-xs font-bold">85% Plan Preserved</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Original Broken Leg */}
            <div className="p-4 bg-white rounded-xl border border-rose-200 space-y-2">
              <span className="text-rose-700 font-bold uppercase text-[10px] block">Disrupted Original Leg</span>
              <p className="text-slate-600 line-through">09:15 AM: Intercity Express Train Departure</p>
              <p className="text-slate-600 line-through">12:30 PM: Midday Station Buffet Lunch</p>
              <span className="text-[11px] text-rose-600 font-semibold block">Status: Cancelled by operator</span>
            </div>

            {/* Recalculated Recovery Leg */}
            <div className="p-4 bg-white rounded-xl border border-emerald-300 shadow-soft space-y-2">
              <span className="text-emerald-700 font-bold uppercase text-[10px] block">Surgical Recovery Leg</span>
              <p className="text-navy-900 font-bold">09:30 AM: On-Demand Highway Express Cab (Arranged)</p>
              <p className="text-navy-900 font-bold">13:00 PM: Scenic Roadside Heritage Lunch</p>
              <span className="text-[11px] text-emerald-600 font-semibold block">Evening sunset dinner preserved with zero delay!</span>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-brand-100 flex-wrap gap-4">
            <div className="text-xs text-slate-600">
              <span>Budget impact: <strong>+{trip.currency} 850</strong> (Cab differential)</span>
            </div>
            <button
              onClick={onApplyRecovery}
              className="btn-primary text-xs py-2.5 px-6 shadow-glow-blue"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Apply Recovery Plan to Active Itinerary</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState } from 'react';
import { Sparkles, CloudRain, Clock, BadgeDollarSign, ShieldAlert, ArrowLeft, ArrowRight, CheckCircle2, Layers } from 'lucide-react';
import { TripResponse } from '../../types';

interface TripTwinSimulatorProps {
  trip: TripResponse;
  onBack: () => void;
}

const SCENARIOS = [
  { id: 'rain', name: 'What if it rains heavily?', icon: CloudRain, color: 'text-blue-600', bg: 'bg-blue-50', desc: 'Swaps outdoor monuments & boats with museums & royal indoor palaces.' },
  { id: 'delay', name: 'What if flight is delayed 3 hrs?', icon: Clock, color: 'text-amber-600', bg: 'bg-amber-50', desc: 'Expedites check-in and shifts morning sights into sunset evening stroll.' },
  { id: 'budget', name: 'What if budget is cut by 20%?', icon: BadgeDollarSign, color: 'text-emerald-600', bg: 'bg-emerald-50', desc: 'Optimizes stay to boutique heritage homestays & free walking tours.' },
  { id: 'closed', name: 'What if primary POI is closed?', icon: ShieldAlert, color: 'text-rose-600', bg: 'bg-rose-50', desc: 'Auto-substitutes nearest top-tier landmark in 1.5km radius.' },
];

export const TripTwinSimulator: React.FC<TripTwinSimulatorProps> = ({ trip, onBack }) => {
  const [selectedScenario, setSelectedScenario] = useState<string>('rain');
  const [simulatedTwin, setSimulatedTwin] = useState<any>({
    scenarioName: 'What if it rains heavily?',
    impact: 'Outdoor heritage monuments & lake boat rides replaced with world-class indoor museums, palace interiors, and cozy artisanal cafes.',
    budgetDelta: 0,
    timeDelta: -30,
    modifications: [
      { original: 'Outdoor Heritage Walking Tour & Sunset Ghats', modified: 'National Heritage Museum & Palace Gallery Tour', reason: 'Heavy rain protection' },
      { original: 'Lake Pichola Open Boat Cruise', modified: 'Rescheduled to clear morning; added Covered Royal Tea Workshop', reason: 'High comfort indoor safety' },
      { original: 'Open Air Street Food Lane', modified: 'Indoor Heritage Haveli Courtyard Dining', reason: 'Sanitary indoor setting' }
    ]
  });

  const handleSelectScenario = (scId: string) => {
    setSelectedScenario(scId);
    if (scId === 'rain') {
      setSimulatedTwin({
        scenarioName: 'What if it rains heavily?',
        impact: 'Outdoor heritage monuments & lake boat rides replaced with world-class indoor museums, palace interiors, and cozy artisanal cafes.',
        budgetDelta: 0,
        timeDelta: -30,
        modifications: [
          { original: 'Outdoor Heritage Walking Tour & Sunset Ghats', modified: 'National Heritage Museum & Palace Gallery Tour', reason: 'Heavy rain protection' },
          { original: 'Lake Pichola Open Boat Cruise', modified: 'Rescheduled to clear morning; added Covered Royal Tea Workshop', reason: 'High comfort indoor safety' },
          { original: 'Open Air Street Food Lane', modified: 'Indoor Heritage Haveli Courtyard Dining', reason: 'Sanitary indoor setting' }
        ]
      });
    } else if (scId === 'delay') {
      setSimulatedTwin({
        scenarioName: 'What if transit/flight is delayed 3 hours?',
        impact: 'Surgically shifted morning sightseeing to evening sunset promenade; check-in expedited with direct hotel transfer.',
        budgetDelta: 0,
        timeDelta: 180,
        modifications: [
          { original: 'Morning 09:30 AM Fort Visit', modified: 'Compressed into Evening Sunset Photo Promenade at 17:45', reason: '3-hour flight landing delay' },
          { original: 'Standard Hotel Check-In Queue', modified: 'Pre-notified Hotel & Fast-Track Key Pick-Up', reason: 'Automated logistics synchronization' }
        ]
      });
    } else if (scId === 'budget') {
      const saved = Math.round(trip.total_budget * 0.20);
      setSimulatedTwin({
        scenarioName: 'What if total budget is reduced by 20%?',
        impact: `Optimized accommodation to boutique 4-star heritage homestay and swapped private cab with high-speed express metro. Saved ${trip.currency} ${saved.toLocaleString()}.`,
        budgetDelta: -saved,
        timeDelta: 0,
        modifications: [
          { original: '5-Star Luxury Resort Stay', modified: 'Verified Boutique Heritage Homestay (Saved 15%)', reason: 'Zero comfort loss budget optimization' },
          { original: 'Private Chauffeur Sedan', modified: 'High-Speed Express Transit & Scheduled Auto Passes', reason: 'Direct transit savings' }
        ]
      });
    } else {
      setSimulatedTwin({
        scenarioName: 'What if primary attraction is closed?',
        impact: 'Auto-swapped with top-rated neighboring royal palace within 1.5 km radius; preserved meal and transit schedule.',
        budgetDelta: 50,
        timeDelta: -15,
        modifications: [
          { original: 'Closed Monument Entry', modified: 'Adjacent Historic Gallery & Garden Complex', reason: 'Neighboring cultural landmark swap' }
        ]
      });
    }
  };

  return (
    <div className="max-w-6xl mx-auto my-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="badge-pink text-xs px-2.5 py-0.5">Trip Twin Simulator</span>
              <span className="badge-blue text-xs px-2.5 py-0.5">Golden Plan Protected</span>
            </div>
            <h1 className="text-3xl font-extrabold text-navy-900 mt-2">What-If Scenario Simulation</h1>
            <p className="text-sm text-slate-500 mt-1">
              Simulate disruptions, weather shifts, and budget shocks side-by-side without altering your original plan.
            </p>
          </div>
          <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Itinerary</span>
          </button>
        </div>

        {/* Scenario Selector Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-100">
          {SCENARIOS.map(sc => {
            const Icon = sc.icon;
            const isSelected = selectedScenario === sc.id;
            return (
              <div
                key={sc.id}
                onClick={() => handleSelectScenario(sc.id)}
                className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                  isSelected
                    ? 'border-brand-500 bg-brand-50/70 shadow-soft ring-2 ring-brand-200'
                    : 'border-slate-200 hover:bg-surface-50'
                }`}
              >
                <div className={`w-8 h-8 rounded-xl ${sc.bg} ${sc.color} flex items-center justify-center mb-2`}>
                  <Icon className="w-4 h-4" />
                </div>
                <h4 className="font-bold text-xs text-navy-900">{sc.name}</h4>
                <p className="text-[11px] text-slate-500 mt-1 leading-snug">{sc.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Side-by-Side Trip Twin Comparator */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Original Golden Plan Card */}
        <div className="card-clean p-6 bg-white border border-slate-200 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <span className="badge-blue text-xs font-bold">Original Golden Plan</span>
            <span className="text-xs font-bold text-navy-900">{trip.currency} {trip.total_budget.toLocaleString()}</span>
          </div>

          <div className="space-y-3 text-xs">
            <h4 className="font-bold text-sm text-navy-900">{trip.title}</h4>
            <p className="text-slate-500">Scheduled standard timeline with planned outdoor highlights and full reservations.</p>

            <div className="p-3 bg-surface-50 rounded-xl space-y-2">
              <span className="font-bold text-slate-400 text-[10px] uppercase block">Key Baseline Activities:</span>
              <ul className="space-y-1.5 text-slate-700">
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-brand-600 shrink-0" />
                  <span>Full Outdoor Sightseeing & Heritage Fort Trails</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-brand-600 shrink-0" />
                  <span>Sunset Promenade & Open Boat Cruise</span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-brand-600 shrink-0" />
                  <span>Standard 4-Star / 5-Star Boutique Stay</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Simulated Trip Twin Card */}
        <div className="card-clean p-6 bg-gradient-to-br from-white via-brand-50/20 to-blush-50/30 border border-brand-300 shadow-soft-lg space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-brand-100">
            <span className="badge-pink text-xs font-bold">Simulated Trip Twin</span>
            <span className="text-xs font-bold text-emerald-700">
              {trip.currency} {(trip.total_budget + simulatedTwin.budgetDelta).toLocaleString()} 
              {simulatedTwin.budgetDelta !== 0 && ` (${simulatedTwin.budgetDelta > 0 ? '+' : ''}${simulatedTwin.budgetDelta})`}
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <h4 className="font-bold text-sm text-navy-900">{simulatedTwin.scenarioName}</h4>
            <p className="text-slate-700 font-medium bg-white/80 p-3 rounded-xl border border-brand-100 leading-relaxed">
              {simulatedTwin.impact}
            </p>

            <div className="space-y-2 pt-1">
              <span className="font-bold text-slate-400 text-[10px] uppercase block">Surgical Adaptations Applied:</span>
              {simulatedTwin.modifications.map((mod: any, idx: number) => (
                <div key={idx} className="p-3 bg-white rounded-xl border border-slate-100 text-[11px] space-y-1">
                  <div className="line-through text-slate-400">{mod.original}</div>
                  <div className="text-brand-700 font-bold flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-pink-500 shrink-0" />
                    <span>{mod.modified}</span>
                  </div>
                  <div className="text-[10px] text-slate-400 italic">Reason: {mod.reason}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { 
  Compass, 
  MapPin, 
  Clock, 
  Car, 
  CloudSun, 
  BadgeDollarSign, 
  ShieldCheck, 
  RotateCcw, 
  PhoneCall, 
  ArrowLeft,
  Sparkles,
  AlertCircle
} from 'lucide-react';
import { TripResponse } from '../../types';

interface LiveTripCompanionProps {
  trip: TripResponse;
  onTriggerRecovery: () => void;
  onBack: () => void;
}

export const LiveTripCompanion: React.FC<LiveTripCompanionProps> = ({ trip, onTriggerRecovery, onBack }) => {
  const currentDay = trip.itinerary_days[0] || { day_number: 1, theme: 'Arrival & Sightseeing', activities: [] };
  const currentAct = currentDay.activities[0] || {
    start_time: '09:00', end_time: '11:30', activity_name: 'Royal Heritage Fortress Tour',
    location_name: 'City Landmark', category: 'Heritage', estimated_cost: 200, is_indoor: false
  };
  const nextAct = currentDay.activities[1] || {
    start_time: '12:00', end_time: '13:45', activity_name: 'Authentic Local Lunch & Artisan Cafe',
    location_name: 'City Bistro', category: 'Culinary', estimated_cost: 600, is_indoor: true
  };

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 sm:px-6 space-y-6">
      {/* Header */}
      <div className="card-clean p-6 bg-gradient-to-r from-navy-900 to-brand-900 text-white shadow-soft-xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-xs text-emerald-300 font-bold uppercase tracking-wider">Live Trip Companion Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold mt-1">{trip.destination}</h1>
          <p className="text-xs text-brand-200 mt-0.5">Day {currentDay.day_number} of {trip.num_days} • {currentDay.theme}</p>
        </div>

        <div className="flex items-center gap-2.5">
          <button 
            onClick={onTriggerRecovery}
            className="btn-accent text-xs py-2.5 px-4 shadow-glow-pink"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Report Disruption</span>
          </button>
          <button onClick={onBack} className="text-xs text-brand-200 hover:text-white px-3 py-2">
            Exit Live Mode
          </button>
        </div>
      </div>

      {/* Live Status Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Weather & Local Time */}
        <div className="card-clean p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <CloudSun className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Local Weather</span>
            <span className="text-xs font-bold text-navy-900">26°C Sunny • Low Humidity</span>
          </div>
        </div>

        {/* Today's Spending */}
        <div className="card-clean p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <BadgeDollarSign className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Today's Budget</span>
            <span className="text-xs font-bold text-emerald-700">{trip.currency} {currentDay.daily_cost_estimated.toLocaleString()} / {currentDay.daily_budget_allocated.toLocaleString()}</span>
          </div>
        </div>

        {/* Local Emergency & Guide Hotline */}
        <div className="card-clean p-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-pink-50 text-pink-600 flex items-center justify-center">
            <PhoneCall className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 font-bold uppercase block">Guide Hotline</span>
            <span className="text-xs font-bold text-navy-900">+91 98765 43210 (Aarav)</span>
          </div>
        </div>
      </div>

      {/* Current Active Plan Segment */}
      <div className="card-clean p-6 bg-white border-2 border-brand-500 shadow-soft-lg space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <span className="badge-pink text-xs font-bold">CURRENT ACTIVITY</span>
            <span className="text-xs text-brand-600 font-bold">{currentAct.start_time} - {currentAct.end_time}</span>
          </div>
          <span className="badge-green text-xs font-bold">On Schedule</span>
        </div>

        <div>
          <h2 className="text-xl font-extrabold text-navy-900">{currentAct.activity_name}</h2>
          <p className="text-xs text-slate-500 flex items-center gap-1.5 mt-1">
            <MapPin className="w-3.5 h-3.5 text-brand-500" />
            <span>{currentAct.location_name}</span>
          </p>
        </div>

        <div className="p-3 bg-brand-50/70 rounded-xl text-xs text-slate-700 flex items-center justify-between">
          <span className="flex items-center gap-1.5 font-semibold text-brand-800">
            <Sparkles className="w-4 h-4 text-brand-600" />
            <span>Recommended: Check in at ticket counter 15 mins prior.</span>
          </span>
          <span className="font-bold text-navy-900">{trip.currency} {currentAct.estimated_cost.toLocaleString()}</span>
        </div>
      </div>

      {/* Upcoming Next Activity */}
      <div className="card-clean p-5 bg-surface-50 space-y-3">
        <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400">UP NEXT AT {nextAct.start_time}</span>
        <div className="flex items-center justify-between">
          <div>
            <h4 className="font-bold text-sm text-navy-900">{nextAct.activity_name}</h4>
            <p className="text-xs text-slate-500 mt-0.5">{nextAct.location_name} • {nextAct.category}</p>
          </div>
          <div className="text-right">
            <span className="text-xs font-bold text-navy-900 block">{trip.currency} {nextAct.estimated_cost.toLocaleString()}</span>
            <span className="text-[10px] text-slate-400">10 min walk</span>
          </div>
        </div>
      </div>
    </div>
  );
};

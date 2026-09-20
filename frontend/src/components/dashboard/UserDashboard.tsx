import React, { useState } from 'react';
import { User, Heart, MapPin, Calendar, Clock, Sparkles, Settings, Trash2, CheckCircle2, ArrowRight } from 'lucide-react';
import { TripResponse } from '../../types';

interface UserDashboardProps {
  recentTrip?: TripResponse | null;
  onOpenTrip?: (trip: TripResponse) => void;
  onPlanNew: () => void;
}

export const UserDashboard: React.FC<UserDashboardProps> = ({ recentTrip, onOpenTrip, onPlanNew }) => {
  const [activeTab, setActiveTab] = useState<'trips' | 'memory' | 'saved'>('trips');
  const [preferences, setPreferences] = useState<{
    travelStyle: string;
    travelPace: string;
    dietary: string[];
    interests: string[];
  }>({
    travelStyle: 'Balanced',
    travelPace: 'Balanced',
    dietary: ['Vegetarian', 'Authentic Local Street Food'],
    interests: ['Heritage Fortresses', 'Photography Trails', 'Scenic Lakes']
  });

  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);

  const handleSaveMemory = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  return (
    <div className="max-w-6xl mx-auto my-8 px-4 sm:px-6 space-y-8">
      {/* User Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 to-brand-500 text-white flex items-center justify-center font-extrabold text-xl shadow-soft">
            RV
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-extrabold text-navy-900">Rohit Verma</h1>
              <span className="badge-blue text-[10px] px-2 py-0.5">Global Explorer</span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">Home Base: Delhi, India • Active Trips: 1</p>
          </div>
        </div>

        <button onClick={onPlanNew} className="btn-primary text-xs py-2.5 px-5 self-start sm:self-auto">
          <Sparkles className="w-4 h-4" />
          <span>Plan New Trip</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('trips')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'trips' ? 'bg-brand-600 text-white shadow-soft' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          My Trips (Upcoming & Past)
        </button>
        <button
          onClick={() => setActiveTab('memory')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'memory' ? 'bg-brand-600 text-white shadow-soft' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          AI Preference Memory
        </button>
        <button
          onClick={() => setActiveTab('saved')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'saved' ? 'bg-brand-600 text-white shadow-soft' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Saved Guides & Places
        </button>
      </div>

      {/* Tab 1: Trips */}
      {activeTab === 'trips' && (
        <div className="space-y-4">
          {recentTrip ? (
            <div className="card-clean p-6 bg-white border border-slate-100 shadow-soft flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="badge-pink text-[10px] px-2 py-0.5">{recentTrip.trip_type}</span>
                  <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Active Plan</span>
                </div>
                <h3 className="font-bold text-lg text-navy-900">{recentTrip.title}</h3>
                <p className="text-xs text-slate-500 flex items-center gap-3">
                  <span>{recentTrip.start_date} to {recentTrip.end_date}</span>
                  <span>•</span>
                  <span>{recentTrip.num_days} Days</span>
                  <span>•</span>
                  <span className="font-bold text-navy-900">{recentTrip.currency} {recentTrip.total_budget.toLocaleString()}</span>
                </p>
              </div>

              <button
                onClick={() => onOpenTrip?.(recentTrip)}
                className="btn-primary text-xs py-2.5 px-5 shadow-soft shrink-0"
              >
                <span>View Itinerary</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="p-12 text-center card-clean bg-white space-y-3">
              <Calendar className="w-10 h-10 text-slate-300 mx-auto" />
              <h4 className="font-bold text-base text-navy-900">No trips generated yet</h4>
              <p className="text-xs text-slate-400">Launch the 15-step wizard to create your first multi-agent travel plan.</p>
              <button onClick={onPlanNew} className="btn-primary text-xs py-2 px-4 mt-2">
                Plan a Trip Now
              </button>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Preference Memory */}
      {activeTab === 'memory' && (
        <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft space-y-6">
          <div>
            <span className="badge-pink text-xs font-bold">Autonomous Habit Learning</span>
            <h3 className="text-lg font-bold text-navy-900 mt-1">Stored Travel Preference Memory</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              The multi-agent system uses these persistent preferences across all your future itineraries unless overridden.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Default Travel Style</label>
              <select 
                value={preferences.travelStyle}
                onChange={(e) => setPreferences({ ...preferences, travelStyle: e.target.value })}
                className="w-full p-2.5 rounded-xl border border-slate-200 bg-white"
              >
                <option>Budget</option>
                <option>Balanced</option>
                <option>Luxury</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Default Travel Pace</label>
              <select 
                value={preferences.travelPace}
                onChange={(e) => setPreferences({ ...preferences, travelPace: e.target.value })}
                className="w-full p-2.5 rounded-xl border border-slate-200 bg-white"
              >
                <option>Relaxed (+45m buffers)</option>
                <option>Balanced (+20m buffers)</option>
                <option>Packed (High Density)</option>
                <option>Adventure</option>
              </select>
            </div>
          </div>

          <div className="space-y-2 text-xs">
            <label className="block font-semibold text-slate-700">Permanent Dietary Preferences</label>
            <div className="flex flex-wrap gap-2">
              {preferences.dietary.map(d => (
                <span key={d} className="badge-green text-xs px-3 py-1 flex items-center gap-1.5">
                  <span>{d}</span>
                </span>
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            {savedSuccess ? (
              <span className="text-xs text-emerald-600 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4" /> Preference Memory Updated!
              </span>
            ) : <div />}

            <button onClick={handleSaveMemory} className="btn-primary text-xs py-2.5 px-6">
              Save Preference Memory
            </button>
          </div>
        </div>
      )}

      {/* Tab 3: Saved Guides */}
      {activeTab === 'saved' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="card-clean p-5 bg-white border border-slate-100 space-y-2">
            <h4 className="font-bold text-sm text-navy-900">Aarav Sharma (Delhi)</h4>
            <p className="text-xs text-slate-500">Mughal Architecture & Street Food specialist • ★ 4.96</p>
            <span className="badge-blue text-[10px] px-2 py-0.5 inline-block">Saved Guide</span>
          </div>
          <div className="card-clean p-5 bg-white border border-slate-100 space-y-2">
            <h4 className="font-bold text-sm text-navy-900">Mahipal Singh Rathore (Jaipur)</h4>
            <p className="text-xs text-slate-500">Royal Rajput history & storytelling • ★ 4.98</p>
            <span className="badge-blue text-[10px] px-2 py-0.5 inline-block">Saved Guide</span>
          </div>
        </div>
      )}
    </div>
  );
};

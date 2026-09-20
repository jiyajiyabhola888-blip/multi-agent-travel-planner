import React, { useState } from 'react';
import { ShieldCheck, CheckSquare, Square, FileText, AlertCircle, ArrowLeft, Sun, Luggage, Heart } from 'lucide-react';
import { TripResponse } from '../../types';

interface PreTripReadinessViewProps {
  trip: TripResponse;
  onBack: () => void;
}

export const PreTripReadinessView: React.FC<PreTripReadinessViewProps> = ({ trip, onBack }) => {
  const [checklist, setChecklist] = useState<Array<{ id: number; task: string; done: boolean; category: string }>>([
    { id: 1, task: 'Verify Passport validity (Min 6 months) or Domestic Aadhaar ID', done: true, category: 'Documents' },
    { id: 2, task: 'Download flight boarding passes & hotel vouchers offline', done: true, category: 'Documents' },
    { id: 3, task: 'Review monument advance reservation slots (Palace & Museums)', done: true, category: 'Tickets' },
    { id: 4, task: 'Pack comfortable walking shoes for cobblestone heritage trails', done: false, category: 'Packing' },
    { id: 5, task: 'Carry universal power adapter & 10000mAh portable powerbank', done: true, category: 'Packing' },
    { id: 6, task: 'Activate international roaming / local eSIM data pack', done: false, category: 'Connectivity' },
    { id: 7, task: 'Check weather forecast and carry light cardigan / umbrella', done: true, category: 'Weather' },
    { id: 8, task: 'Notify local bank of foreign multi-currency card travel usage', done: false, category: 'Finance' },
  ]);

  const toggleTask = (id: number) => {
    setChecklist(prev => prev.map(item => item.id === id ? { ...item, done: !item.done } : item));
  };

  const completedCount = checklist.filter(c => c.done).length;
  const readinessPercent = Math.round((completedCount / checklist.length) * 100);

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 sm:px-6 space-y-6">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="badge-green text-xs font-bold">Readiness Score: {completedCount}/{checklist.length} Completed</span>
            </div>
            <h1 className="text-3xl font-extrabold text-navy-900 mt-2">Pre-Trip Readiness & Checklist</h1>
            <p className="text-sm text-slate-500 mt-1">
              Ensure you have all documents, reservations, and essentials verified before departure to {trip.destination}.
            </p>
          </div>
          <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Itinerary</span>
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mt-6 pt-4 border-t border-slate-100 space-y-2">
          <div className="flex justify-between text-xs font-bold">
            <span className="text-navy-900">Trip Readiness Progress</span>
            <span className="text-brand-600">{readinessPercent}%</span>
          </div>
          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
            <div 
              className="bg-gradient-to-r from-brand-500 to-emerald-500 h-full rounded-full transition-all duration-300"
              style={{ width: `${readinessPercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Official Visa Disclaimer Alert */}
      <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-900 space-y-1">
          <h5 className="font-bold">Important Travel & Visa Reminder</h5>
          <p className="leading-relaxed">
            Government entry policies, visa durations, and customs requirements can change at any time. Always verify current rules directly with the official embassy, consulate, or government visa portal before flying.
          </p>
        </div>
      </div>

      {/* Checklist Items */}
      <div className="card-clean p-6 bg-white border border-slate-100 shadow-soft space-y-3">
        <h3 className="font-bold text-sm text-navy-900 pb-2 border-b border-slate-100">Action Items</h3>
        <div className="space-y-2">
          {checklist.map(item => (
            <div
              key={item.id}
              onClick={() => toggleTask(item.id)}
              className={`p-3.5 rounded-xl border flex items-center justify-between cursor-pointer transition-all ${
                item.done ? 'bg-emerald-50/40 border-emerald-200' : 'bg-surface-50 border-slate-200 hover:bg-slate-100'
              }`}
            >
              <div className="flex items-center gap-3">
                {item.done ? (
                  <CheckSquare className="w-4 h-4 text-emerald-600 shrink-0" />
                ) : (
                  <Square className="w-4 h-4 text-slate-400 shrink-0" />
                )}
                <span className={`text-xs font-medium ${item.done ? 'line-through text-slate-400' : 'text-navy-900'}`}>
                  {item.task}
                </span>
              </div>
              <span className="text-[10px] uppercase font-bold text-slate-400 bg-white px-2 py-0.5 rounded border border-slate-200">
                {item.category}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

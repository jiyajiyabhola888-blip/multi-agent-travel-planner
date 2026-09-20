import React, { useState } from 'react';
import { 
  Calendar, 
  Clock, 
  MapPin, 
  Car, 
  BadgeDollarSign, 
  Info, 
  Sparkles, 
  CloudSun, 
  ShieldCheck, 
  Utensils, 
  Hotel, 
  Compass, 
  RotateCcw,
  CheckCircle2,
  ChevronRight,
  HelpCircle,
  X,
  CreditCard,
  Heart
} from 'lucide-react';
import { TripResponse, ItineraryDaySchema, ActivityItemSchema } from '../../types';

interface SmartItineraryViewProps {
  trip: TripResponse;
  onSimulate: () => void;
  onLiveTrip: () => void;
  onLiveRecovery: () => void;
  onFindGuide: () => void;
  onCheckReadiness: () => void;
  onBookActivity?: (act: ActivityItemSchema) => void;
}

export const SmartItineraryView: React.FC<SmartItineraryViewProps> = ({
  trip,
  onSimulate,
  onLiveTrip,
  onLiveRecovery,
  onFindGuide,
  onCheckReadiness,
  onBookActivity
}) => {
  const [activeDayIndex, setActiveDayIndex] = useState<number>(0);
  const [selectedExplainActivity, setSelectedExplainActivity] = useState<ActivityItemSchema | null>(null);

  const currentDay = trip.itinerary_days[activeDayIndex] || trip.itinerary_days[0];

  return (
    <div className="max-w-7xl mx-auto my-8 px-4 sm:px-6 lg:px-8 space-y-8 animate-fade-in">
      {/* Top Banner & Quick Controls */}
      <div className="card-luxury p-6 sm:p-8 bg-white border border-blush-200 shadow-xl">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 flex-wrap mb-2">
              <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-200">
                {trip.trip_type} Mode
              </span>
              <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-blush-100 text-charcoal-800 border border-blush-200">
                {trip.travel_style} Style
              </span>
              <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-cream text-emerald-700 border border-emerald-200">
                {trip.travel_pace} Pace
              </span>
              <span className="text-xs text-charcoal-400 font-medium">
                Readiness Score: <strong className="text-emerald-600">{trip.readiness_score}/10</strong>
              </span>
            </div>
            <h1 className="font-serif text-2xl sm:text-3xl lg:text-4xl font-bold text-charcoal-900">
              {trip.title}
            </h1>
            <p className="text-xs sm:text-sm text-charcoal-500 mt-2 flex items-center gap-2 flex-wrap">
              <span className="flex items-center gap-1 font-semibold text-rose-600">
                <MapPin className="w-3.5 h-3.5" />
                {trip.start_location} → {trip.destination}
              </span>
              <span className="text-blush-300">•</span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-rose-500" />
                {trip.start_date} to {trip.end_date} ({trip.num_days} Days, {trip.num_travelers} Travelers)
              </span>
            </p>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-2">
            <button 
              onClick={onSimulate}
              className="btn-secondary text-xs py-2.5 px-4 flex items-center gap-1.5"
              title="What-If Trip Simulator"
            >
              <Sparkles className="w-3.5 h-3.5 text-rose-500" />
              <span>Trip Simulator</span>
            </button>

            <button 
              onClick={onLiveTrip}
              className="btn-primary text-xs py-2.5 px-4 flex items-center gap-1.5 shadow-md shadow-rose-200"
              title="Live Trip Companion"
            >
              <Compass className="w-3.5 h-3.5" />
              <span>Live Trip Mode</span>
            </button>

            <button 
              onClick={onLiveRecovery}
              className="px-3.5 py-2.5 rounded-full border border-rose-200 text-rose-700 bg-rose-50 hover:bg-rose-100 text-xs font-semibold flex items-center gap-1.5 transition-colors"
              title="Live Recovery Replanner"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>1-Click Recovery</span>
            </button>

            <button 
              onClick={onCheckReadiness}
              className="btn-secondary text-xs py-2.5 px-3.5 flex items-center gap-1.5"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Readiness</span>
            </button>
          </div>
        </div>

        {/* Budget Summary Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 mt-6 pt-6 border-t border-blush-100 text-xs">
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Total Budget</span>
            <span className="text-sm font-serif font-bold text-charcoal-900 mt-0.5 block">{trip.currency} {trip.total_budget.toLocaleString()}</span>
          </div>
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Stay Bucket</span>
            <span className="text-sm font-bold text-rose-600 mt-0.5 block">{trip.currency} {(trip.budget_breakdown.stay || 0).toLocaleString()}</span>
          </div>
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Transport</span>
            <span className="text-sm font-bold text-charcoal-800 mt-0.5 block">{trip.currency} {(trip.budget_breakdown.transport || 0).toLocaleString()}</span>
          </div>
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Food & Dining</span>
            <span className="text-sm font-bold text-charcoal-800 mt-0.5 block">{trip.currency} {(trip.budget_breakdown.food || 0).toLocaleString()}</span>
          </div>
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Activities</span>
            <span className="text-sm font-bold text-charcoal-800 mt-0.5 block">{trip.currency} {(trip.budget_breakdown.activities || 0).toLocaleString()}</span>
          </div>
          <div className="p-3 bg-cream rounded-2xl border border-blush-100">
            <span className="text-charcoal-400 font-medium block text-[11px]">Guide / Host</span>
            <span className="text-sm font-bold text-rose-700 mt-0.5 block">{trip.currency} {(trip.budget_breakdown.guide || 0).toLocaleString()}</span>
          </div>
        </div>
      </div>

      {/* Main Day View & Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Day Selector Sidebar */}
        <div className="lg:col-span-1 space-y-2">
          <h3 className="font-serif font-bold text-xs uppercase tracking-wider text-charcoal-400 px-1 mb-3">
            Day Schedule & Themes
          </h3>
          {trip.itinerary_days.map((day, idx) => (
            <div
              key={day.day_number}
              onClick={() => setActiveDayIndex(idx)}
              className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                activeDayIndex === idx
                  ? 'bg-rose-600 text-white border-rose-600 shadow-md shadow-rose-200'
                  : 'bg-white text-charcoal-900 border-blush-200 hover:border-blush-300 hover:bg-cream'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-serif font-bold text-sm">Day {day.day_number}</span>
                <span className={`text-[11px] font-semibold ${activeDayIndex === idx ? 'text-blush-100' : 'text-charcoal-400'}`}>
                  {day.date}
                </span>
              </div>
              <p className={`text-xs mt-1 truncate ${activeDayIndex === idx ? 'text-blush-100' : 'text-charcoal-500'}`}>
                {day.theme.replace(/^Day \d+:\s*/, '')}
              </p>
            </div>
          ))}

          {/* Local Guide Connection Card */}
          <div className="p-5 rounded-3xl bg-gradient-to-br from-blush-50 via-cream to-rose-50 border border-blush-200 mt-6 space-y-3">
            <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-600 flex items-center justify-center font-bold">
              🧭
            </div>
            <div>
              <h4 className="font-serif font-bold text-xs text-charcoal-900">Need a Verified Local Guide?</h4>
              <p className="text-[11px] text-charcoal-600 leading-snug mt-0.5">
                Connect with background-checked certified guides in {trip.destination.split(',')[0]}.
              </p>
            </div>
            <button 
              onClick={onFindGuide}
              className="btn-secondary text-xs py-2 px-3.5 w-full text-center"
            >
              Browse Verified Guides
            </button>
          </div>
        </div>

        {/* Day Activity Timeline */}
        <div className="lg:col-span-3 space-y-4">
          {/* Day Header */}
          <div className="card-luxury p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-cream border border-blush-200">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">
                Day {currentDay.day_number} Focus
              </span>
              <h3 className="font-serif font-bold text-lg text-charcoal-900 mt-1">{currentDay.theme}</h3>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <div className="flex items-center gap-1.5 text-charcoal-700 bg-white px-3 py-1.5 rounded-full border border-blush-200">
                <CloudSun className="w-4 h-4 text-amber-500" />
                <span>{currentDay.weather_summary}</span>
              </div>
              <div className="flex items-center gap-1 text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-full font-bold border border-emerald-200">
                <span>{trip.currency} {currentDay.daily_cost_estimated.toLocaleString()} spent</span>
              </div>
            </div>
          </div>

          {/* Timeline Activity Cards */}
          <div className="space-y-4">
            {currentDay.activities.map((act, aIdx) => (
              <div key={act.id || aIdx} className="card-luxury p-5 relative overflow-hidden group bg-white border border-blush-200">
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                  <div className="flex items-start gap-4">
                    {/* Time Slot Pill */}
                    <div className="text-center shrink-0 w-16">
                      <span className="text-xs font-bold text-rose-600 block">{act.start_time}</span>
                      <span className="text-[11px] text-charcoal-400 font-medium block">{act.end_time}</span>
                      <span className="px-2 py-0.5 mt-1 block font-semibold text-[10px] rounded-full bg-blush-50 text-charcoal-700 border border-blush-100">
                        {act.time_slot}
                      </span>
                    </div>

                    {/* Activity Content */}
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h4 className="font-serif font-bold text-base text-charcoal-900">{act.activity_name}</h4>
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-50 text-rose-700 border border-rose-100">
                          {act.category}
                        </span>
                        {act.booking_required && (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                            Booking Recommended
                          </span>
                        )}
                        {act.is_indoor ? (
                          <span className="text-[10px] text-charcoal-600 bg-cream px-2 py-0.5 rounded-full border border-blush-100">
                            Indoor
                          </span>
                        ) : (
                          <span className="text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-100">
                            Outdoor Scenic
                          </span>
                        )}
                      </div>

                      <p className="text-xs text-charcoal-500 flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5 text-rose-500" />
                        <span>{act.location_name}</span>
                      </p>

                      {/* Realistic Time & Buffer Badges */}
                      <div className="flex items-center gap-3 pt-2 flex-wrap text-[11px]">
                        <span className="flex items-center gap-1 text-charcoal-600 bg-cream px-2.5 py-1 rounded-xl border border-blush-100">
                          <Car className="w-3.5 h-3.5 text-rose-500" />
                          <span>Transit: <strong>{act.transit_time_from_prev_mins}m</strong> ({act.transit_mode})</span>
                        </span>

                        <span className="flex items-center gap-1 text-amber-800 bg-amber-50/70 px-2.5 py-1 rounded-xl border border-amber-200">
                          <Clock className="w-3.5 h-3.5 text-amber-600" />
                          <span>Buffer/Queue: <strong>+{act.buffer_security_mins}m</strong></span>
                        </span>

                        <span className="flex items-center gap-1 text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-xl border border-emerald-200 font-bold">
                          <BadgeDollarSign className="w-3.5 h-3.5 text-emerald-600" />
                          <span>{trip.currency} {act.estimated_cost.toLocaleString()}</span>
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Actions Right */}
                  <div className="flex items-center gap-2 self-end sm:self-start">
                    {onBookActivity && (
                      <button
                        onClick={() => onBookActivity(act)}
                        className="px-3 py-1.5 rounded-full border border-blush-200 text-charcoal-700 hover:text-rose-600 hover:bg-blush-50 text-xs font-semibold flex items-center gap-1 transition-colors"
                        title="Book activity ticket in Sandbox"
                      >
                        <CreditCard className="w-3.5 h-3.5 text-rose-500" />
                        <span className="hidden sm:inline">Reserve</span>
                      </button>
                    )}

                    {/* Explainable AI Button */}
                    <button
                      onClick={() => setSelectedExplainActivity(act)}
                      className="p-2 text-charcoal-400 hover:text-rose-600 hover:bg-blush-50 rounded-xl transition-colors shrink-0 flex items-center gap-1 text-xs font-semibold"
                      title="Why was this activity selected?"
                    >
                      <Info className="w-4 h-4 text-rose-600" />
                      <span className="hidden sm:inline">Why this?</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Explainable AI Modal */}
      {selectedExplainActivity && (
        <div className="fixed inset-0 z-50 bg-charcoal-900/50 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
          <div className="card-luxury max-w-md w-full p-6 bg-white shadow-2xl border border-blush-200 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-blush-100">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-200">
                  <Sparkles className="w-4 h-4 text-rose-600" />
                </div>
                <h4 className="font-serif font-bold text-sm text-charcoal-900">Explainable AI Reasoning</h4>
              </div>
              <button onClick={() => setSelectedExplainActivity(null)} className="text-charcoal-400 hover:text-charcoal-700">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <h5 className="font-serif font-bold text-base text-charcoal-900">{selectedExplainActivity.activity_name}</h5>
              <p className="text-xs text-rose-600 font-semibold mt-0.5">{selectedExplainActivity.time_slot} Slot • {selectedExplainActivity.category}</p>
            </div>

            <div className="p-4 rounded-2xl bg-blush-50/70 border border-blush-200 text-xs text-charcoal-700 leading-relaxed space-y-2">
              <p><strong>Rationale:</strong> {selectedExplainActivity.why_explanation}</p>
              <p><strong>Route Optimization:</strong> Clustered within {selectedExplainActivity.transit_time_from_prev_mins} mins transit from previous stop to prevent traveler fatigue.</p>
              <p><strong>Buffer Injection:</strong> +{selectedExplainActivity.buffer_security_mins} mins added for ticketing, security checks, and photography pauses.</p>
            </div>

            <button 
              onClick={() => setSelectedExplainActivity(null)}
              className="btn-primary w-full text-xs py-2.5"
            >
              Understood
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

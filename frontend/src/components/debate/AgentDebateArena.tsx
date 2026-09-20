import React, { useState, useEffect } from 'react';
import { Bot, CheckCircle2, ShieldAlert, Sparkles, Scale, ArrowRight, Activity, Award } from 'lucide-react';
import { AgentDebateMessage } from '../../types';

interface AgentDebateArenaProps {
  debateLog: AgentDebateMessage[];
  onProceedToItinerary: () => void;
  destination: string;
}

export const AgentDebateArena: React.FC<AgentDebateArenaProps> = ({ debateLog, onProceedToItinerary, destination }) => {
  const [visibleCount, setVisibleCount] = useState<number>(1);
  const [isDebating, setIsDebating] = useState<boolean>(true);

  useEffect(() => {
    if (visibleCount < debateLog.length) {
      const timer = setTimeout(() => {
        setVisibleCount(prev => prev + 1);
      }, 350); // fast dynamic stream
      return () => clearTimeout(timer);
    } else {
      setIsDebating(false);
    }
  }, [visibleCount, debateLog.length]);

  return (
    <div className="max-w-4xl mx-auto my-8 px-4 sm:px-6 space-y-6 animate-fade-in">
      {/* Header */}
      <div className="card-luxury p-6 bg-gradient-to-r from-white via-blush-50 to-cream border border-blush-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-50 text-rose-700 border border-rose-200">
              Autonomous Agent Arena
            </span>
            {isDebating ? (
              <span className="flex items-center gap-1.5 text-xs text-rose-600 font-semibold animate-pulse">
                <Activity className="w-3.5 h-3.5" />
                Agents Debating ({visibleCount}/{debateLog.length})...
              </span>
            ) : (
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200">
                Consensus & Arbitration Reached
              </span>
            )}
          </div>
          <h2 className="font-serif text-2xl sm:text-3xl font-bold text-charcoal-900 mt-2">
            15-Agent Live Debate for {destination}
          </h2>
          <p className="text-xs text-charcoal-500 mt-1">
            Evaluating travel pacing, non-repeating POI clusters, budget caps, and realistic transit buffers.
          </p>
        </div>

        {!isDebating && (
          <button
            onClick={onProceedToItinerary}
            className="btn-primary text-xs py-3 px-6 shadow-lg shadow-rose-200 animate-bounce"
          >
            <span>View Smart Itinerary</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Live Debate Message Feed */}
      <div className="space-y-3">
        {debateLog.slice(0, visibleCount).map((msg, idx) => {
          const isJudge = msg.stance === 'verdict';
          const isCritique = msg.stance === 'critique';

          return (
            <div 
              key={idx}
              className={`p-5 rounded-3xl border transition-all animate-slide-up ${
                isJudge 
                  ? 'bg-gradient-to-br from-charcoal-900 via-charcoal-800 to-rose-950 text-white border-rose-500/40 shadow-2xl ring-2 ring-rose-500/20' 
                  : isCritique 
                  ? 'bg-amber-50/80 border-amber-200 shadow-sm' 
                  : 'bg-white border-blush-200 shadow-sm'
              }`}
            >
              <div className="flex items-start gap-3.5">
                {/* Agent Avatar */}
                <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 font-bold text-sm shadow-sm ${
                  isJudge 
                    ? 'bg-gradient-to-tr from-amber-400 to-amber-600 text-charcoal-950' 
                    : isCritique 
                    ? 'bg-amber-500 text-white' 
                    : 'bg-rose-500/10 text-rose-600 border border-rose-200'
                }`}>
                  {isJudge ? <Scale className="w-5 h-5 text-charcoal-900" /> : isCritique ? <ShieldAlert className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between flex-wrap gap-1">
                    <div className="flex items-center gap-2">
                      <h4 className={`font-serif font-bold text-sm ${isJudge ? 'text-amber-300' : 'text-charcoal-900'}`}>
                        {msg.agent_name}
                      </h4>
                      <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${
                        isJudge ? 'bg-white/10 text-blush-200' : 'bg-cream text-charcoal-600 border border-blush-100'
                      }`}>
                        {msg.agent_role}
                      </span>
                    </div>
                    <span className={`text-[10px] uppercase tracking-wider font-extrabold px-2.5 py-0.5 rounded-full ${
                      isJudge 
                        ? 'bg-amber-400 text-charcoal-950 shadow-sm' 
                        : isCritique 
                        ? 'bg-amber-100 text-amber-900' 
                        : 'bg-rose-50 text-rose-700'
                    }`}>
                      {msg.stance}
                    </span>
                  </div>

                  <p className={`text-xs mt-2 leading-relaxed ${isJudge ? 'text-blush-100' : 'text-charcoal-700'}`}>
                    {msg.message}
                  </p>

                  {msg.proposed_adjustments && msg.proposed_adjustments.length > 0 && (
                    <div className={`mt-3 pt-2.5 border-t text-[11px] space-y-1.5 ${isJudge ? 'border-white/10' : 'border-blush-100'}`}>
                      {msg.proposed_adjustments.map((adj, aIdx) => (
                        <div key={aIdx} className={`flex items-center gap-1.5 ${isJudge ? 'text-emerald-300 font-medium' : 'text-rose-600 font-semibold'}`}>
                          <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                          <span>{adj}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

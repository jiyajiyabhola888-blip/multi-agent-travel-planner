import React from 'react';
import { Globe, Shield, Heart, Sparkles, MapPin, Compass, CheckCircle2, Lock } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-blush-200 pt-16 pb-12 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-blush-200">
          {/* Brand Info */}
          <div className="md:col-span-1 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-rose-600 via-rose-500 to-warm-pink flex items-center justify-center text-white shadow-md shadow-rose-200">
                <Globe className="w-5 h-5" />
              </div>
              <div>
                <span className="font-serif font-extrabold text-lg text-charcoal-900 tracking-tight">
                  WORLD <span className="text-rose-600">TRAVELHOLIC</span>
                </span>
                <span className="ml-1 text-sm">🌍</span>
              </div>
            </div>
            <p className="text-xs text-charcoal-500 leading-relaxed">
              The premier autonomous 15-agent travel ecosystem. Delivering discrete canonical destination planning, interactive city hubs, sandbox bookings, and live AI recovery.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-rose-700 font-semibold bg-blush-50 py-1.5 px-3 rounded-full w-fit border border-blush-200">
              <Sparkles className="w-3.5 h-3.5 text-rose-500" />
              <span>Explore More. Travel Smarter.</span>
            </div>
          </div>

          {/* Multi-Agent Architecture */}
          <div>
            <h4 className="font-serif font-bold text-xs text-charcoal-900 mb-4 uppercase tracking-wider">
              15 AI Agent Core
            </h4>
            <ul className="space-y-2 text-xs text-charcoal-500">
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Preference & Destination Engine</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Realistic Route & Transit Buffer</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Stay & Food Venue Curator</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Judge Arbitration & Debate Arena</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Trip Twin Disruption Simulator</li>
            </ul>
          </div>

          {/* Global Destinations */}
          <div>
            <h4 className="font-serif font-bold text-xs text-charcoal-900 mb-4 uppercase tracking-wider">
              Curated City Hubs
            </h4>
            <ul className="space-y-2 text-xs text-charcoal-500">
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Jaipur (Pink City Heritage)</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Udaipur (City of Lakes)</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Tokyo & Kyoto, Japan</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Paris & Interlaken, Europe</li>
              <li className="hover:text-rose-600 cursor-pointer transition-colors">Dubai & Bali, Southeast Asia</li>
            </ul>
          </div>

          {/* Platform Trust & Safety */}
          <div>
            <h4 className="font-serif font-bold text-xs text-charcoal-900 mb-4 uppercase tracking-wider">
              Trust & Sandbox Info
            </h4>
            <ul className="space-y-2.5 text-xs text-charcoal-600">
              <li className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-600" />
                <span>Verified Local Guides & Stays</span>
              </li>
              <li className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-rose-600" />
                <span>Simulated Sandbox Payments (No Real Charges)</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-rose-500" />
                <span>Explainable AI Decisions on Every Choice</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-charcoal-400 gap-4">
          <p>© 2026 WORLD TRAVELHOLIC 🌍. All rights reserved.</p>
          <div className="flex items-center gap-1">
            <span>Crafted with</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500 inline mx-0.5" />
            <span>for the world's most discerning travelers</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

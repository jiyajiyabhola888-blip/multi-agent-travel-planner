import React, { useState } from 'react';
import { ShieldCheck, Star, MapPin, Globe, CheckCircle2, MessageSquare, X, ArrowRight } from 'lucide-react';
import { MOCK_GUIDES } from '../../services/mockData';
import { LocalGuideProfile } from '../../types';

interface GuidesMarketplaceProps {
  onBack?: () => void;
}

export const GuidesMarketplace: React.FC<GuidesMarketplaceProps> = ({ onBack }) => {
  const [selectedCity, setSelectedCity] = useState<string>('All');
  const [selectedGuideForService, setSelectedGuideForService] = useState<LocalGuideProfile | null>(null);
  const [serviceSubmitted, setServiceSubmitted] = useState<boolean>(false);
  const [travelerName, setTravelerName] = useState<string>('Rohit Verma');
  const [travelDate, setTravelDate] = useState<string>('2026-10-16');

  const filteredGuides = MOCK_GUIDES.filter(g => {
    if (selectedCity === 'All') return true;
    return g.city.toLowerCase().includes(selectedCity.toLowerCase());
  });

  const handleSubmitRequest = (e: React.FormEvent) => {
    e.preventDefault();
    setServiceSubmitted(true);
    setTimeout(() => {
      setServiceSubmitted(false);
      setSelectedGuideForService(null);
    }, 2500);
  };

  return (
    <div className="max-w-6xl mx-auto my-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="badge-pink text-xs px-2.5 py-1">Verified Local Experts</span>
            <h1 className="text-3xl font-extrabold text-navy-900 mt-2">Local Guides & Travel Hosts</h1>
            <p className="text-sm text-slate-500 mt-1">
              Connect with licensed tour guides, photographers, trekkers, and authentic storytellers.
            </p>
          </div>
          {onBack && (
            <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
              Back to Trip
            </button>
          )}
        </div>

        {/* City Filter Chips */}
        <div className="flex items-center gap-2 mt-6 pt-4 border-t border-slate-100 flex-wrap">
          <span className="text-xs font-bold text-slate-400 mr-2">Filter by City:</span>
          {['All', 'New Delhi', 'Jaipur', 'Kochi', 'Paris'].map(city => (
            <button
              key={city}
              onClick={() => setSelectedCity(city)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                selectedCity === city ? 'bg-brand-600 text-white shadow-soft' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {city}
            </button>
          ))}
        </div>
      </div>

      {/* Guide Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredGuides.map(guide => (
          <div key={guide.id} className="card-clean p-6 bg-white border border-slate-100 shadow-soft flex flex-col justify-between space-y-4">
            <div className="flex items-start gap-4">
              <img 
                src={guide.avatarUrl} 
                alt={guide.name} 
                className="w-16 h-16 rounded-2xl object-cover ring-2 ring-brand-100 shrink-0" 
              />
              <div className="space-y-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <h3 className="font-bold text-base text-navy-900">{guide.name}</h3>
                  {guide.verified && (
                    <span className="badge-blue text-[10px] px-2 py-0.5 flex items-center gap-1 font-bold">
                      <ShieldCheck className="w-3 h-3 text-brand-600" />
                      <span>Verified</span>
                    </span>
                  )}
                </div>

                <p className="text-xs text-slate-500 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-brand-600" />
                  <span>{guide.city}, {guide.country} • {guide.experienceYears} Years Exp.</span>
                </p>

                <div className="flex items-center gap-2 text-xs pt-1">
                  <div className="flex items-center gap-1 text-amber-500 font-bold">
                    <Star className="w-3.5 h-3.5 fill-amber-400" />
                    <span>{guide.rating}</span>
                  </div>
                  <span className="text-slate-300">•</span>
                  <span className="text-slate-500">{guide.reviewsCount} verified reviews</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed bg-surface-50 p-3 rounded-xl">
              "{guide.bio}"
            </p>

            <div className="space-y-2 text-xs">
              <div className="flex items-center gap-2 text-slate-500">
                <Globe className="w-3.5 h-3.5 text-slate-400" />
                <span>Languages: <strong>{guide.languages.join(', ')}</strong></span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {guide.services.map(s => (
                  <span key={s} className="badge-pink text-[10px] px-2 py-0.5 font-medium">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Bottom Bar & Booking CTA */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-100">
              <div>
                <span className="text-[10px] text-slate-400 font-bold block uppercase">Rate</span>
                <span className="text-sm font-extrabold text-brand-600">{guide.currency} {guide.hourlyRate}/hr</span>
              </div>

              <button
                onClick={() => setSelectedGuideForService(guide as any)}
                className="btn-primary text-xs py-2 px-4 shadow-soft"
              >
                <span>Request Service</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Service Request Modal */}
      {selectedGuideForService && (
        <div className="fixed inset-0 z-50 bg-navy-900/40 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="card-clean max-w-md w-full p-6 bg-white shadow-soft-xl animate-fadeIn space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <span className="badge-pink text-[10px] px-2 py-0.5">Demo / Mock Booking</span>
                <h4 className="font-bold text-sm text-navy-900 mt-1">Connect with {selectedGuideForService.name}</h4>
              </div>
              <button onClick={() => setSelectedGuideForService(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {serviceSubmitted ? (
              <div className="p-6 text-center space-y-3">
                <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto animate-bounce" />
                <h5 className="font-bold text-base text-navy-900">Request Sent Successfully!</h5>
                <p className="text-xs text-slate-500">
                  {selectedGuideForService.name} in {selectedGuideForService.city} has received your service details.
                </p>
                <div className="text-[11px] text-slate-400 bg-slate-50 p-2 rounded-lg">
                  Prototype Demo: No payment was charged.
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmitRequest} className="space-y-3 text-xs">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Your Name</label>
                  <input 
                    type="text"
                    value={travelerName}
                    onChange={(e) => setTravelerName(e.target.value)}
                    required
                    className="w-full p-2.5 rounded-xl border border-slate-200"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Travel Date</label>
                  <input 
                    type="date"
                    value={travelDate}
                    onChange={(e) => setTravelDate(e.target.value)}
                    required
                    className="w-full p-2.5 rounded-xl border border-slate-200"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Service Type</label>
                  <select className="w-full p-2.5 rounded-xl border border-slate-200 bg-white">
                    <option>Full Day Heritage Walking Tour (6 hrs)</option>
                    <option>Evening Culinary Street Food Trail (3 hrs)</option>
                    <option>Custom Photography Tour</option>
                  </select>
                </div>

                <div className="p-3 bg-brand-50 rounded-xl text-[11px] text-brand-800">
                  🔒 Verified Guide Guarantee • Free cancellation up to 24 hrs before trip.
                </div>

                <button type="submit" className="btn-primary w-full text-xs py-3 mt-2">
                  Confirm Service Request
                </button>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

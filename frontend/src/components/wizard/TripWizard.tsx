import React, { useState } from 'react';
import { 
  Sparkles, 
  ArrowLeft, 
  ArrowRight, 
  MapPin, 
  Calendar, 
  Users, 
  BadgeDollarSign, 
  Compass, 
  Heart, 
  Coffee, 
  Hotel, 
  Car, 
  CheckCircle2, 
  HelpCircle,
  Briefcase,
  Flame,
  SunMedium,
  Globe
} from 'lucide-react';
import { TripWizardState, TripType, TravelStyle, TravelPace } from '../../types';

interface TripWizardProps {
  onComplete: (data: TripWizardState) => void;
  onExploreDestinations: () => void;
  onCancel: () => void;
}

const TRIP_TYPES: { type: TripType; icon: any; label: string; desc: string }[] = [
  { type: 'Honeymoon', icon: Heart, label: 'Honeymoon & Romance', desc: 'Private palace suites, rooftop dining & intimate sunset views' },
  { type: 'Family', icon: Users, label: 'Family & Multi-Gen', desc: 'Child & elder-friendly pacing, verified hotels & zero-rush transit' },
  { type: 'Friends', icon: Flame, label: 'Friends & Adventure', desc: 'Shared experiences, cultural crawls, nightlife & group excursions' },
  { type: 'Solo', icon: Compass, label: 'Solo Explorer', desc: 'Safe routes, authentic boutique stays, verified guides & flexible hours' },
  { type: 'Business', icon: Briefcase, label: 'Bleisure (Work + Leisure)', desc: 'Meeting-friendly scheduling, fast Wi-Fi lounges & premium transfers' },
  { type: 'Adventure', icon: SunMedium, label: 'Alpine & Thrill', desc: 'Mountain trekking, glacier passes, watersports & safari permits' },
  { type: 'Relaxation', icon: Coffee, label: 'Wellness & Spa', desc: 'Ayurveda retreats, onsen springs, peaceful waters & calm cafes' },
];

const CURRENCIES = ['USD', 'EUR', 'GBP', 'INR', 'AED', 'SGD', 'JPY', 'CHF'];

const INTEREST_OPTIONS = [
  'Heritage & Palaces', 'Michelin & Street Food Crawls', 'Landscape Photography', 'Nature & Wildlife',
  'Spiritual & Ancient Temples', 'Scenic Train Journeys', 'Local Artisan Workshops', 'Beach & Coastal Sunsets',
  'Luxury Bazaars & Shopping', 'Rooftop Lounges & Nightlife', 'Art Museums & Architecture', 'Mountain Passes & Trekking'
];

const FOOD_PREFS = [
  'Vegetarian', 'Vegan', 'Jain Friendly', 'Halal', 'Authentic Street Food', 'Fine Dining Gastronomy', 'Seafood Specialties'
];

export const TripWizard: React.FC<TripWizardProps> = ({ onComplete, onExploreDestinations, onCancel }) => {
  const [step, setStep] = useState<number>(1);
  const totalSteps = 15;

  const [formData, setFormData] = useState<TripWizardState>({
    tripType: 'Family',
    destination: 'Jaipur, Rajasthan, India',
    startLocation: 'Delhi, India',
    numTravelers: 2,
    startDate: '2026-10-15',
    endDate: '2026-10-20',
    numDays: 5,
    totalBudget: 1200,
    currency: 'USD',
    travelStyle: 'Balanced',
    travelPace: 'Balanced',
    interests: ['Heritage & Palaces', 'Michelin & Street Food Crawls', 'Landscape Photography'],
    foodPreferences: ['Vegetarian', 'Authentic Street Food'],
    accommodationPreference: 'Boutique Hotel / 4-Star',
    transportationPreference: 'Private Cab & Chauffeur',
    specialRequirements: ''
  });

  const updateField = (field: keyof TripWizardState, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const toggleArrayItem = (field: 'interests' | 'foodPreferences', item: string) => {
    setFormData(prev => {
      const list = prev[field];
      if (list.includes(item)) {
        return { ...prev, [field]: list.filter(i => i !== item) };
      } else {
        return { ...prev, [field]: [...list, item] };
      }
    });
  };

  const nextStep = () => {
    if (step < totalSteps) setStep(step + 1);
    else onComplete(formData);
  };

  const prevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="max-w-3xl mx-auto my-8 px-4 sm:px-6">
      {/* Container with Luxury Card Aesthetic */}
      <div className="card-luxury p-6 sm:p-10 bg-white border border-blush-200 shadow-xl">
        {/* Progress Header */}
        <div className="flex items-center justify-between mb-6 pb-4 border-b border-blush-100">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              Step {step} of {totalSteps}
            </div>
            <h2 className="font-serif text-xl sm:text-2xl font-bold text-charcoal-900 mt-1">
              {step === 1 && "What type of journey are you planning?"}
              {step === 2 && "Where would you like to travel?"}
              {step === 3 && "Where is your departure starting point?"}
              {step === 4 && "How many travelers in your party?"}
              {step === 5 && "Select your planned travel dates"}
              {step === 6 && "How many days is your total trip?"}
              {step === 7 && "What is your estimated total budget?"}
              {step === 8 && "Select your preferred currency"}
              {step === 9 && "Choose your desired travel style"}
              {step === 10 && "What is your preferred daily travel pace?"}
              {step === 11 && "What interests excite you the most?"}
              {step === 12 && "Any dietary or culinary preferences?"}
              {step === 13 && "Preferred accommodation tier"}
              {step === 14 && "Preferred transportation mode"}
              {step === 15 && "Special requirements & accessibility notes"}
            </h2>
          </div>
          <button onClick={onCancel} className="text-xs text-charcoal-400 hover:text-charcoal-700 font-medium">
            Cancel
          </button>
        </div>

        {/* Visual Progress Bar */}
        <div className="w-full bg-blush-100 h-2 rounded-full overflow-hidden mb-8">
          <div 
            className="bg-gradient-to-r from-rose-500 via-rose-600 to-warm-pink h-full rounded-full transition-all duration-300"
            style={{ width: `${(step / totalSteps) * 100}%` }}
          />
        </div>

        {/* Step Content */}
        <div className="min-h-[280px]">
          {/* Step 1: Trip Type */}
          {step === 1 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {TRIP_TYPES.map(t => {
                const Icon = t.icon;
                const isSelected = formData.tripType === t.type;
                return (
                  <div 
                    key={t.type}
                    onClick={() => updateField('tripType', t.type)}
                    className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                      isSelected 
                        ? 'border-rose-500 bg-rose-50/50 shadow-sm ring-2 ring-rose-200' 
                        : 'border-blush-200 hover:border-blush-300 hover:bg-cream'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-2xl flex items-center justify-center ${isSelected ? 'bg-rose-600 text-white' : 'bg-blush-100 text-charcoal-700'}`}>
                        <Icon className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="font-bold text-sm text-charcoal-900">{t.label}</h4>
                        <p className="text-xs text-charcoal-500 mt-0.5 leading-snug">{t.desc}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Step 2: Destination */}
          {step === 2 && (
            <div className="space-y-4">
              <label className="block text-sm font-semibold text-charcoal-900">
                Destination City (Discrete Canonical Location)
              </label>
              <div className="relative">
                <MapPin className="w-5 h-5 text-rose-600 absolute left-4 top-1/2 -translate-y-1/2" />
                <input 
                  type="text"
                  value={formData.destination}
                  onChange={(e) => updateField('destination', e.target.value)}
                  placeholder="e.g. Jaipur, Rajasthan, India"
                  className="input-blush pl-12 text-sm font-medium"
                />
              </div>

              {/* Quick Suggestion Chips */}
              <div className="pt-2">
                <span className="text-xs text-charcoal-500 font-medium block mb-2">
                  Curated Global Hubs:
                </span>
                <div className="flex flex-wrap gap-2">
                  {[
                    'Jaipur, Rajasthan, India',
                    'Udaipur, Rajasthan, India',
                    'Tokyo, Japan',
                    'Paris, France',
                    'Interlaken, Switzerland',
                    'Dubai, United Arab Emirates',
                    'Bali, Indonesia',
                    'Goa, India'
                  ].map(dest => (
                    <button
                      key={dest}
                      onClick={() => updateField('destination', dest)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                        formData.destination === dest
                          ? 'bg-rose-600 text-white border-rose-600'
                          : 'bg-cream text-charcoal-700 border-blush-200 hover:bg-blush-100'
                      }`}
                    >
                      {dest}
                    </button>
                  ))}
                </div>
              </div>

              {/* Discovery Trigger */}
              <div className="mt-4 p-4 rounded-2xl bg-blush-50 border border-blush-200 flex items-center justify-between">
                <div>
                  <h5 className="font-serif font-bold text-xs text-charcoal-900">Need expert inspiration?</h5>
                  <p className="text-[11px] text-charcoal-600">Explore our global destination hubs with luxury stays and video guides.</p>
                </div>
                <button 
                  onClick={onExploreDestinations}
                  className="btn-secondary text-xs py-2 px-3 shrink-0"
                >
                  <Globe className="w-3.5 h-3.5 text-rose-500" />
                  <span>Browse Hubs</span>
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Starting Location */}
          {step === 3 && (
            <div className="space-y-4">
              <label className="block text-sm font-semibold text-charcoal-900">Your Starting Departure City / Airport</label>
              <div className="relative">
                <Compass className="w-5 h-5 text-rose-600 absolute left-4 top-1/2 -translate-y-1/2" />
                <input 
                  type="text"
                  value={formData.startLocation}
                  onChange={(e) => updateField('startLocation', e.target.value)}
                  placeholder="e.g. Delhi, Mumbai, London, New York, Tokyo"
                  className="input-blush pl-12 text-sm font-medium"
                />
              </div>
              <div className="flex flex-wrap gap-2">
                {['Delhi, India', 'Mumbai, India', 'London, UK', 'New York, USA', 'Tokyo, Japan', 'Dubai, UAE'].map(city => (
                  <button
                    key={city}
                    onClick={() => updateField('startLocation', city)}
                    className="text-xs bg-cream hover:bg-blush-100 border border-blush-200 text-charcoal-700 px-3.5 py-1.5 rounded-full font-medium transition-colors"
                  >
                    {city}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 4: Number of Travelers */}
          {step === 4 && (
            <div className="space-y-6">
              <div className="flex items-center justify-center gap-6 py-6">
                <button 
                  onClick={() => updateField('numTravelers', Math.max(1, formData.numTravelers - 1))}
                  className="w-12 h-12 rounded-2xl border border-blush-200 flex items-center justify-center text-xl font-bold text-charcoal-700 hover:bg-blush-50"
                >
                  -
                </button>
                <span className="font-serif text-4xl font-extrabold text-charcoal-900 w-16 text-center">{formData.numTravelers}</span>
                <button 
                  onClick={() => updateField('numTravelers', formData.numTravelers + 1)}
                  className="w-12 h-12 rounded-2xl border border-blush-200 flex items-center justify-center text-xl font-bold text-charcoal-700 hover:bg-blush-50"
                >
                  +
                </button>
              </div>
              <p className="text-center text-xs text-charcoal-500">
                {formData.numTravelers === 1 ? 'Solo trip: Maximizing flexibility, boutique vibes & safe navigation.' : `${formData.numTravelers} travelers: Group conflict engine will balance compromises and scheduling.`}
              </p>
            </div>
          )}

          {/* Step 5: Travel Dates */}
          {step === 5 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-charcoal-600 mb-1">Start Date</label>
                <input 
                  type="date"
                  value={formData.startDate}
                  onChange={(e) => updateField('startDate', e.target.value)}
                  className="input-blush text-sm font-medium"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-charcoal-600 mb-1">End Date</label>
                <input 
                  type="date"
                  value={formData.endDate}
                  onChange={(e) => updateField('endDate', e.target.value)}
                  className="input-blush text-sm font-medium"
                />
              </div>
            </div>
          )}

          {/* Step 6: Number of Days */}
          {step === 6 && (
            <div className="space-y-6 text-center py-4">
              <span className="font-serif text-4xl font-extrabold text-rose-600">{formData.numDays} Days</span>
              <input 
                type="range"
                min={2}
                max={14}
                value={formData.numDays}
                onChange={(e) => updateField('numDays', parseInt(e.target.value))}
                className="w-full accent-rose-600 h-2 bg-blush-200 rounded-lg cursor-pointer"
              />
              <div className="flex justify-between text-xs text-charcoal-400 font-medium px-1">
                <span>Weekend (2 Days)</span>
                <span>Standard (5-7 Days)</span>
                <span>Grand Tour (14 Days)</span>
              </div>
            </div>
          )}

          {/* Step 7: Budget */}
          {step === 7 && (
            <div className="space-y-4">
              <label className="block text-sm font-semibold text-charcoal-900">Total Trip Budget</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 font-bold text-charcoal-500">{formData.currency}</span>
                <input 
                  type="number"
                  value={formData.totalBudget}
                  onChange={(e) => updateField('totalBudget', parseFloat(e.target.value) || 0)}
                  className="input-blush pl-16 text-lg font-bold text-charcoal-900"
                />
              </div>
              <div className="flex gap-2 flex-wrap">
                {[600, 1200, 2400, 4500].map(amt => (
                  <button
                    key={amt}
                    onClick={() => updateField('totalBudget', amt)}
                    className="text-xs bg-cream hover:bg-blush-100 hover:text-rose-600 border border-blush-200 px-3 py-1.5 rounded-xl font-semibold transition-colors"
                  >
                    {formData.currency} {amt.toLocaleString()}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 8: Currency */}
          {step === 8 && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {CURRENCIES.map(curr => (
                <button
                  key={curr}
                  onClick={() => updateField('currency', curr)}
                  className={`p-4 rounded-2xl border text-center font-bold text-sm transition-all ${
                    formData.currency === curr 
                      ? 'bg-rose-600 text-white border-rose-600 shadow-md shadow-rose-200' 
                      : 'bg-white text-charcoal-700 border-blush-200 hover:bg-cream'
                  }`}
                >
                  {curr}
                </button>
              ))}
            </div>
          )}

          {/* Step 9: Travel Style */}
          {step === 9 && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                { style: 'Budget', desc: 'Boutique hostels, express metro, local street food gems & high value' },
                { style: 'Balanced', desc: 'Curated 4-star boutique stays, private cabs, mix of heritage dining & cafes' },
                { style: 'Luxury', desc: '5-star heritage palaces, private chauffeur, fine dining tasting menus & VIP passes' },
              ].map(item => (
                <div
                  key={item.style}
                  onClick={() => updateField('travelStyle', item.style as TravelStyle)}
                  className={`p-5 rounded-2xl border cursor-pointer transition-all ${
                    formData.travelStyle === item.style
                      ? 'border-rose-500 bg-rose-50/50 shadow-sm ring-2 ring-rose-200'
                      : 'border-blush-200 hover:bg-cream'
                  }`}
                >
                  <h4 className="font-serif font-bold text-base text-charcoal-900">{item.style}</h4>
                  <p className="text-xs text-charcoal-500 mt-1 leading-relaxed">{item.desc}</p>
                </div>
              ))}
            </div>
          )}

          {/* Step 10: Travel Pace */}
          {step === 10 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {[
                { pace: 'Relaxed', desc: 'Max 2 POIs/day, +45m buffer times, afternoon rest & zero rush' },
                { pace: 'Balanced', desc: '3-4 POIs/day, +20m buffer times, optimal coverage & leisure' },
                { pace: 'Packed', desc: '5+ POIs/day, high density exploration for ambitious sightseers' },
                { pace: 'Adventure', desc: 'Dynamic outdoor activities, early sunrises & trail timings' },
              ].map(item => (
                <div
                  key={item.pace}
                  onClick={() => updateField('travelPace', item.pace as TravelPace)}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                    formData.travelPace === item.pace
                      ? 'border-rose-500 bg-rose-50/50 shadow-sm ring-2 ring-rose-200'
                      : 'border-blush-200 hover:bg-cream'
                  }`}
                >
                  <h4 className="font-bold text-sm text-charcoal-900">{item.pace}</h4>
                  <p className="text-xs text-charcoal-500 mt-0.5">{item.desc}</p>
                </div>
              ))}
            </div>
          )}

          {/* Step 11: Interests */}
          {step === 11 && (
            <div className="flex flex-wrap gap-2.5">
              {INTEREST_OPTIONS.map(interest => {
                const isSelected = formData.interests.includes(interest);
                return (
                  <button
                    key={interest}
                    onClick={() => toggleArrayItem('interests', interest)}
                    className={`px-4 py-2 rounded-full text-xs font-semibold transition-all ${
                      isSelected
                        ? 'bg-rose-600 text-white shadow-sm'
                        : 'bg-cream text-charcoal-700 hover:bg-blush-100 border border-blush-200'
                    }`}
                  >
                    {interest}
                  </button>
                );
              })}
            </div>
          )}

          {/* Step 12: Food Preferences */}
          {step === 12 && (
            <div className="flex flex-wrap gap-2.5">
              {FOOD_PREFS.map(food => {
                const isSelected = formData.foodPreferences.includes(food);
                return (
                  <button
                    key={food}
                    onClick={() => toggleArrayItem('foodPreferences', food)}
                    className={`px-4 py-2 rounded-full text-xs font-semibold transition-all ${
                      isSelected
                        ? 'bg-emerald-600 text-white shadow-sm'
                        : 'bg-cream text-charcoal-700 hover:bg-blush-100 border border-blush-200'
                    }`}
                  >
                    {food}
                  </button>
                );
              })}
            </div>
          )}

          {/* Step 13: Accommodation */}
          {step === 13 && (
            <div className="space-y-3">
              {['Boutique Hotel / 4-Star', 'Heritage Haveli & Palatial Resort', 'Luxury 5-Star Hotel', 'Scenic Mountain Chalet & Villa', 'Cozy High-End Homestay'].map(stay => (
                <div
                  key={stay}
                  onClick={() => updateField('accommodationPreference', stay)}
                  className={`p-3.5 rounded-2xl border cursor-pointer font-semibold text-xs flex items-center justify-between transition-all ${
                    formData.accommodationPreference === stay
                      ? 'border-rose-500 bg-rose-50 text-rose-700'
                      : 'border-blush-200 text-charcoal-700 hover:bg-cream'
                  }`}
                >
                  <span>{stay}</span>
                  {formData.accommodationPreference === stay && <CheckCircle2 className="w-4 h-4 text-rose-600" />}
                </div>
              ))}
            </div>
          )}

          {/* Step 14: Transportation */}
          {step === 14 && (
            <div className="space-y-3">
              {['Private Cab & Chauffeur', 'High-Speed Rail & Metro', 'Scenic Ferry & Private Transfer', 'Walking & Traditional Auto-Rickshaw'].map(trans => (
                <div
                  key={trans}
                  onClick={() => updateField('transportationPreference', trans)}
                  className={`p-3.5 rounded-2xl border cursor-pointer font-semibold text-xs flex items-center justify-between transition-all ${
                    formData.transportationPreference === trans
                      ? 'border-rose-500 bg-rose-50 text-rose-700'
                      : 'border-blush-200 text-charcoal-700 hover:bg-cream'
                  }`}
                >
                  <span>{trans}</span>
                  {formData.transportationPreference === trans && <CheckCircle2 className="w-4 h-4 text-rose-600" />}
                </div>
              ))}
            </div>
          )}

          {/* Step 15: Special Requirements */}
          {step === 15 && (
            <div className="space-y-4">
              <label className="block text-sm font-semibold text-charcoal-900">Any Special Requirements, Accessibility, or Group Notes?</label>
              <textarea
                rows={4}
                value={formData.specialRequirements}
                onChange={(e) => updateField('specialRequirements', e.target.value)}
                placeholder="e.g. Traveling with infant (need stroller access), wheelchair accessibility needed, celebrating wedding anniversary on Day 3..."
                className="input-blush text-sm"
              />
              <div className="p-3 bg-blush-50 rounded-2xl text-xs text-rose-900 font-medium border border-blush-200">
                ✨ When you click "Launch 15-Agent Debate", all 15 specialized agents will evaluate your criteria, verify routes, calculate transit buffers, and construct an optimized non-repeating itinerary.
              </div>
            </div>
          )}
        </div>

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between mt-8 pt-6 border-t border-blush-100">
          <button
            onClick={prevStep}
            disabled={step === 1}
            className={`btn-secondary text-xs py-2.5 px-4 ${step === 1 ? 'opacity-40 cursor-not-allowed' : ''}`}
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>

          <button
            onClick={nextStep}
            className="btn-primary text-xs py-2.5 px-6 shadow-md shadow-rose-200"
          >
            <span>{step === totalSteps ? 'Launch 15-Agent Debate' : 'Next Step'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

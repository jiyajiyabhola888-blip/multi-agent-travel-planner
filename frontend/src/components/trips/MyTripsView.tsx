import React, { useState, useEffect } from 'react';
import { 
  Calendar, MapPin, DollarSign, Clock, CheckCircle2, AlertTriangle, 
  ExternalLink, Trash2, ArrowRight, Shield, Sparkles, Navigation, Plus
} from 'lucide-react';
import { BookingRecord } from '../../types';
import { apiService } from '../../services/api';

interface MyTripsViewProps {
  onPlanNewTrip: () => void;
  onExploreDestination: (city: string) => void;
  onLaunchRecovery: (tripId: string) => void;
}

export const MyTripsView: React.FC<MyTripsViewProps> = ({
  onPlanNewTrip,
  onExploreDestination,
  onLaunchRecovery,
}) => {
  const [activeTab, setActiveTab] = useState<'upcoming' | 'active' | 'completed' | 'bookings'>('upcoming');
  const [bookings, setBookings] = useState<BookingRecord[]>([]);
  const [loading, setLoading] = useState(true);

  // Mock trips data enhanced for World Travelholic
  const mockTrips = [
    {
      id: 'TRIP-JP-2026',
      title: 'Royal Heritage & Palaces of Jaipur',
      destination: 'Jaipur, Rajasthan, India',
      status: 'upcoming',
      startDate: '2026-10-15',
      endDate: '2026-10-19',
      coverImage: 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1000&q=80',
      budget: '$850 USD',
      days: 5,
      agentsActive: 15,
      countdownDays: 26,
      highlights: ['Amber Palace private tour', 'LMB Johari Bazaar feast', 'Hawa Mahal sunrise photo op'],
      hasDisruptionRisk: true,
    },
    {
      id: 'TRIP-TYO-2026',
      title: 'Neon & Tradition Tokyo Expedition',
      destination: 'Tokyo, Japan',
      status: 'active',
      startDate: '2026-09-18',
      endDate: '2026-09-24',
      coverImage: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1000&q=80',
      budget: '$2,400 USD',
      days: 7,
      agentsActive: 15,
      countdownDays: 0,
      highlights: ['Senso-ji morning ritual', 'Shibuya Sky sunset pass', 'Tsukiji Outer Market sushi tour'],
      hasDisruptionRisk: false,
    },
    {
      id: 'TRIP-PAR-2025',
      title: 'Romantic Haussmann Escape',
      destination: 'Paris, France',
      status: 'completed',
      startDate: '2025-05-10',
      endDate: '2025-05-16',
      coverImage: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1000&q=80',
      budget: '$1,900 USD',
      days: 6,
      agentsActive: 15,
      countdownDays: null,
      highlights: ['Louvre VIP nocturne', 'Seine river cruise', 'Le Marais boutique stroll'],
      hasDisruptionRisk: false,
    },
  ];

  useEffect(() => {
    loadBookings();
  }, []);

  const loadBookings = async () => {
    setLoading(true);
    try {
      const data = await apiService.listBookings();
      setBookings(data);
    } catch (err) {
      console.warn('Using default demo bookings:', err);
      setBookings([
        {
          id: 'BK-DEMO-101',
          item_type: 'stay',
          title: 'The Raj Palace Heritage Grand Suite',
          destination: 'Jaipur, Rajasthan, India',
          start_date: '2026-10-15',
          end_date: '2026-10-19',
          guests: 2,
          total_price: 1350,
          currency: 'USD',
          status: 'CONFIRMED',
          is_sandbox: true,
          created_at: '2026-09-18T10:00:00Z',
        },
        {
          id: 'BK-DEMO-102',
          item_type: 'experience',
          title: 'Private Sunset Hot Air Balloon Safari',
          destination: 'Jaipur, Rajasthan, India',
          start_date: '2026-10-16',
          guests: 2,
          total_price: 360,
          currency: 'USD',
          status: 'CONFIRMED',
          is_sandbox: true,
          created_at: '2026-09-18T11:30:00Z',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const filteredTrips = mockTrips.filter((t) => t.status === activeTab);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Header Banner */}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-charcoal-900 via-charcoal-800 to-rose-950 p-8 sm:p-10 text-white shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/20 border border-rose-400/30 text-rose-200 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5 text-rose-300" />
              World Travelholic Command Center
            </div>
            <h1 className="font-serif text-3xl sm:text-4xl font-bold tracking-tight">
              My Trips & Reservations
            </h1>
            <p className="text-sm text-blush-200 mt-2 max-w-xl">
              Track your autonomous 15-agent itineraries, live flight updates, hotel bookings, and
              instant one-click recovery options.
            </p>
          </div>
          <button
            onClick={onPlanNewTrip}
            className="btn-primary self-start md:self-auto flex items-center gap-2 text-xs py-3 px-6 shadow-lg shadow-rose-900/50"
          >
            <Plus className="w-4 h-4" />
            Plan New AI Trip
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-blush-200 pb-2 overflow-x-auto">
        {[
          { id: 'upcoming', label: 'Upcoming Trips', count: 1 },
          { id: 'active', label: 'Live Active Trip', count: 1 },
          { id: 'completed', label: 'Past Journeys', count: 1 },
          { id: 'bookings', label: 'Sandbox Bookings', count: bookings.length },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 rounded-2xl text-xs font-bold transition-all flex items-center gap-2 whitespace-nowrap ${
              activeTab === tab.id
                ? 'bg-rose-600 text-white shadow-md shadow-rose-200'
                : 'text-charcoal-600 hover:bg-blush-100 hover:text-charcoal-900'
            }`}
          >
            <span>{tab.label}</span>
            <span
              className={`px-2 py-0.5 rounded-full text-[10px] ${
                activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-blush-200 text-charcoal-700'
              }`}
            >
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Trips Grid View */}
      {activeTab !== 'bookings' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTrips.map((trip) => (
            <div
              key={trip.id}
              className="card-luxury overflow-hidden group flex flex-col justify-between"
            >
              <div>
                {/* Image & Badges */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={trip.coverImage}
                    alt={trip.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/80 via-transparent to-transparent" />

                  <div className="absolute top-3 left-3 flex items-center gap-2">
                    <span
                      className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider backdrop-blur-md shadow-sm ${
                        trip.status === 'active'
                          ? 'bg-emerald-500/90 text-white'
                          : trip.status === 'upcoming'
                          ? 'bg-rose-600/90 text-white'
                          : 'bg-charcoal-700/90 text-white'
                      }`}
                    >
                      {trip.status}
                    </span>
                    {trip.countdownDays !== null && trip.countdownDays > 0 && (
                      <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-white/90 text-charcoal-800 backdrop-blur-md shadow-sm">
                        In {trip.countdownDays} Days
                      </span>
                    )}
                  </div>

                  <div className="absolute bottom-3 left-3 right-3 text-white">
                    <h3 className="font-serif text-lg font-bold line-clamp-1">{trip.title}</h3>
                    <p className="text-xs text-blush-200 flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-rose-300" />
                      {trip.destination}
                    </p>
                  </div>
                </div>

                {/* Details Body */}
                <div className="p-5 space-y-4">
                  <div className="grid grid-cols-3 gap-2 text-center text-xs py-2 bg-cream rounded-2xl border border-blush-100">
                    <div>
                      <span className="text-[10px] text-charcoal-400 block">Duration</span>
                      <span className="font-bold text-charcoal-800">{trip.days} Days</span>
                    </div>
                    <div className="border-x border-blush-200">
                      <span className="text-[10px] text-charcoal-400 block">Budget</span>
                      <span className="font-bold text-rose-600">{trip.budget}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-charcoal-400 block">AI Engine</span>
                      <span className="font-bold text-charcoal-800">15 Agents</span>
                    </div>
                  </div>

                  {/* Highlights list */}
                  <div>
                    <h4 className="text-[11px] font-bold uppercase tracking-wider text-charcoal-500 mb-2">
                      Key Planned Highlights
                    </h4>
                    <ul className="space-y-1 text-xs text-charcoal-700">
                      {trip.highlights.map((h, i) => (
                        <li key={i} className="flex items-center gap-2">
                          <CheckCircle2 className="w-3.5 h-3.5 text-rose-500 shrink-0" />
                          <span className="truncate">{h}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Disruption Alert */}
                  {trip.hasDisruptionRisk && (
                    <div className="p-3 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                        <span>Monsoon weather watch active</span>
                      </div>
                      <button
                        onClick={() => onLaunchRecovery(trip.id)}
                        className="text-[10px] font-bold text-amber-800 underline hover:text-amber-900 whitespace-nowrap"
                      >
                        Simulate Recovery
                      </button>
                    </div>
                  )}
                </div>
              </div>

              {/* Card Footer */}
              <div className="p-5 pt-0 border-t border-blush-100 mt-2 flex items-center justify-between gap-3">
                <button
                  onClick={() => onExploreDestination(trip.destination.split(',')[0].trim())}
                  className="text-xs font-semibold text-charcoal-600 hover:text-rose-600 flex items-center gap-1 transition-colors"
                >
                  Explore City Hub
                  <ExternalLink className="w-3 h-3" />
                </button>
                <button
                  onClick={() => onLaunchRecovery(trip.id)}
                  className="btn-secondary text-xs py-2 px-4 flex items-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  View Multi-Agent Plan
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Sandbox Bookings Tab */}
      {activeTab === 'bookings' && (
        <div className="space-y-4">
          <div className="p-4 rounded-2xl bg-cream border border-blush-200 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-rose-500/10 text-rose-600 flex items-center justify-center font-bold">
                💳
              </div>
              <div>
                <h3 className="font-serif text-base font-bold text-charcoal-900">
                  Confirmed Sandbox Bookings
                </h3>
                <p className="text-xs text-charcoal-500">
                  Simulated reservations for stays, verified local guides, and activities.
                </p>
              </div>
            </div>
            <span className="badge-demo">SANDBOX ACTIVE</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {bookings.map((b) => (
              <div
                key={b.id}
                className="p-5 rounded-3xl bg-white border border-blush-200 shadow-sm space-y-3 relative overflow-hidden"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">
                      {b.item_type}
                    </span>
                    <h4 className="font-bold text-charcoal-900 text-sm mt-1">{b.title}</h4>
                    <p className="text-xs text-charcoal-500 flex items-center gap-1 mt-0.5">
                      <MapPin className="w-3.5 h-3.5 text-rose-500" />
                      {b.destination}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="block text-xs font-bold text-emerald-600 uppercase">
                      {b.status}
                    </span>
                    <span className="font-mono text-[10px] text-charcoal-400">{b.id}</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 py-2 border-y border-blush-100 text-xs text-charcoal-600">
                  <div>
                    <span className="text-[10px] text-charcoal-400 block">Dates</span>
                    <span className="font-semibold text-charcoal-800">{b.start_date}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-charcoal-400 block">Party Size</span>
                    <span className="font-semibold text-charcoal-800">{b.guests} Guests</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-charcoal-400 block">Total Paid</span>
                    <span className="font-bold text-rose-600">${b.total_price}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs pt-1">
                  <span className="text-[11px] text-charcoal-400">Sandbox Transaction Verified</span>
                  <button
                    onClick={() => alert(`Showing voucher confirmation for ${b.id}`)}
                    className="text-rose-600 hover:text-rose-700 font-bold flex items-center gap-1"
                  >
                    View Voucher <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

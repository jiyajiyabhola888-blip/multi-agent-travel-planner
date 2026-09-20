import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  MapPin, 
  Calendar, 
  Clock, 
  BadgeDollarSign, 
  Star, 
  Hotel, 
  Utensils, 
  Landmark, 
  Play, 
  ArrowLeft, 
  Heart, 
  Share2, 
  CheckCircle2, 
  ShieldCheck, 
  Info, 
  Globe, 
  Compass, 
  UserCheck, 
  Camera, 
  X,
  ExternalLink
} from 'lucide-react';
import { getDestinationDetail, toggleWishlistItem } from '../../services/api';
import { DestinationDetail, HotelStayItem, RestaurantVenueItem, AttractionItem } from '../../types';

interface DestinationDetailPageProps {
  destinationName?: string;
  cityIdentifier?: string;
  onPlanTrip: (destName: string) => void;
  onBookItem?: (item: any) => void;
  onBack: () => void;
}

export const DestinationDetailPage: React.FC<DestinationDetailPageProps> = ({
  destinationName,
  cityIdentifier,
  onPlanTrip,
  onBookItem,
  onBack
}) => {
  const targetCity = cityIdentifier || destinationName || 'jaipur';
  const [data, setData] = useState<DestinationDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [errorType, setErrorType] = useState<'not_found' | 'unavailable' | null>(null);
  const [activeTab, setActiveTab] = useState<'all' | 'attractions' | 'stays' | 'food' | 'guides' | 'videos' | 'requirements'>('all');
  const [isSaved, setIsSaved] = useState<boolean>(false);
  const [activeVideoModal, setActiveVideoModal] = useState<string | null>(null);

  const FALLBACK_HERO = "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200&auto=format&fit=crop&q=80";
  const FALLBACK_STAY = "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80";
  const FALLBACK_FOOD = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80";
  const FALLBACK_POI = "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80";

  const loadData = () => {
    setLoading(true);
    setErrorType(null);
    getDestinationDetail(targetCity)
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load destination details:", err);
        if (err.response?.status === 404) {
          setErrorType('not_found');
        } else {
          setErrorType('unavailable');
        }
        setLoading(false);
      });
  };

  useEffect(() => {
    loadData();
  }, [targetCity]);

  const handleSaveToggle = async () => {
    if (!data) return;
    setIsSaved(!isSaved);
    await toggleWishlistItem({
      item_type: 'destination',
      item_id: `dest_${data.id}`,
      title: `${data.name}, ${data.country_name}`,
      location: data.country_name,
      image_url: data.image_url,
      rating: 4.9
    });
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-12 h-12 border-4 border-rose-200 border-t-rose-600 rounded-full animate-spin mx-auto" />
        <h3 className="text-xl font-bold text-charcoal-900">Loading {destinationName || targetCity} Travel Hub...</h3>
        <p className="text-xs text-charcoal-500">Curating top stays, local food trails, attractions, and travel insights.</p>
      </div>
    );
  }

  if (errorType === 'not_found') {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-6">
        <div className="w-16 h-16 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto shadow-sm">
          <Globe className="w-8 h-8 text-rose-600" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-serif font-bold text-charcoal-900">Destination not found.</h2>
          <p className="text-sm text-charcoal-500 max-w-md mx-auto">
            We could not find travel records matching "{targetCity}". Try searching for another city, country, or landmark.
          </p>
        </div>
        <div className="flex items-center justify-center gap-3">
          <button onClick={onBack} className="btn-primary text-sm py-2.5 px-6">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Explore</span>
          </button>
        </div>
      </div>
    );
  }

  if (errorType === 'unavailable' || !data) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-6">
        <div className="w-16 h-16 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto shadow-sm">
          <Info className="w-8 h-8 text-amber-600" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-serif font-bold text-charcoal-900">
            Travel data is temporarily unavailable. Please try again.
          </h2>
          <p className="text-sm text-charcoal-500 max-w-md mx-auto">
            Our server connection timed out or is temporarily synchronizing global catalog updates.
          </p>
        </div>
        <div className="flex items-center justify-center gap-3">
          <button onClick={loadData} className="btn-primary text-sm py-2.5 px-6">
            <span>Try Again</span>
          </button>
          <button onClick={onBack} className="btn-secondary text-sm py-2.5 px-6">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Explore</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-24 space-y-10">
      {/* Top Floating Breadcrumb Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 flex items-center justify-between">
        <button 
          onClick={onBack}
          className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-rose-200 text-xs font-bold text-charcoal-700 hover:text-rose-600 hover:bg-rose-50 shadow-xs transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Explore</span>
        </button>

        <div className="flex items-center gap-2">
          <button 
            onClick={handleSaveToggle}
            className={`p-2.5 rounded-xl border transition-all ${
              isSaved 
                ? 'bg-rose-50 border-rose-300 text-rose-600' 
                : 'bg-white border-rose-200 text-charcoal-600 hover:text-rose-600 hover:bg-rose-50'
            }`}
          >
            <Heart className={`w-4 h-4 ${isSaved ? 'fill-rose-500' : ''}`} />
          </button>
          <button 
            onClick={() => onPlanTrip(`${data.name}, ${data.country_name}`)}
            className="btn-primary text-xs sm:text-sm py-2.5 px-5 shadow-soft"
          >
            <Sparkles className="w-4 h-4" />
            <span>Plan with 15 Agents</span>
          </button>
        </div>
      </div>

      {/* Hero Banner Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative h-[340px] sm:h-[420px] rounded-3xl overflow-hidden shadow-soft-xl group bg-charcoal-900">
          <img 
            src={data.image_url || FALLBACK_HERO} 
            alt={data.name} 
            onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_HERO; }}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
          />
          <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/95 via-charcoal-900/40 to-transparent" />

          {/* Hero Overlay Content */}
          <div className="absolute bottom-6 left-6 right-6 sm:bottom-10 sm:left-10 sm:right-10 flex flex-col sm:flex-row sm:items-end justify-between gap-6 text-white">
            <div className="space-y-2 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md border border-white/30 text-xs font-bold uppercase tracking-wider">
                <Globe className="w-3.5 h-3.5 text-rose-300" />
                <span>{data.region_name ? `${data.region_name}, ${data.country_name}` : data.country_name}</span>
              </div>
              <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight drop-shadow-md">
                {data.name}
              </h1>
              <p className="text-xs sm:text-sm text-rose-100/90 leading-relaxed drop-shadow-sm line-clamp-2 sm:line-clamp-none">
                {data.description}
              </p>
            </div>

            {/* Quick Stats Pill */}
            <div className="flex flex-wrap gap-2 sm:gap-3 bg-white/10 backdrop-blur-md p-3 sm:p-4 rounded-2xl border border-white/20 text-xs font-semibold shrink-0">
              <div>
                <span className="text-[10px] text-rose-200 block uppercase">Best Season</span>
                <span className="font-bold text-white">{data.best_months}</span>
              </div>
              <div className="w-px h-8 bg-white/20 hidden sm:block" />
              <div>
                <span className="text-[10px] text-rose-200 block uppercase">Avg Budget</span>
                <span className="font-bold text-white">₹{data.avg_daily_budget_inr.toLocaleString()}/day</span>
              </div>
              <div className="w-px h-8 bg-white/20 hidden sm:block" />
              <div>
                <span className="text-[10px] text-rose-200 block uppercase">Timezone</span>
                <span className="font-bold text-white">{data.timezone}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Filter Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2 overflow-x-auto pb-2 no-scrollbar border-b border-rose-100">
          {[
            { id: 'all', label: 'Overview & All', icon: Globe },
            { id: 'attractions', label: `Top Attractions (${data.attractions.length})`, icon: Landmark },
            { id: 'stays', label: `Where to Stay (${data.stays.length})`, icon: Hotel },
            { id: 'food', label: `Where to Eat (${data.restaurants.length})`, icon: Utensils },
            { id: 'guides', label: `Local Guides (${data.guides.length})`, icon: UserCheck },
            { id: 'videos', label: `Video Guides (${data.videos.length})`, icon: Play },
            { id: 'requirements', label: 'Travel Info & Visa', icon: Info },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold whitespace-nowrap flex items-center gap-2 transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-brand-500 to-rose-600 text-white shadow-soft'
                    : 'bg-white text-charcoal-700 hover:bg-rose-50 hover:text-brand-600 border border-rose-100'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* SECTION 1: TOP ATTRACTIONS */}
      {(activeTab === 'all' || activeTab === 'attractions') && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <span className="badge-pink text-xs font-bold">Must-Visit Sights</span>
              <h2 className="text-2xl font-extrabold text-charcoal-900 mt-1">Top Attractions in {data.name}</h2>
            </div>
            <span className="text-xs text-slate-500 font-medium hidden sm:block">Door-to-door clustered routes</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.attractions.map((poi) => (
              <div key={poi.id} className="card-clean overflow-hidden group flex flex-col justify-between">
                <div>
                  <div className="h-48 overflow-hidden relative bg-charcoal-900">
                    <img 
                      src={poi.image_url || data.image_url || FALLBACK_POI} 
                      alt={poi.name} 
                      onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_POI; }}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                    />
                    <div className="absolute top-3 left-3 flex gap-1.5">
                      <span className="bg-charcoal-900/80 backdrop-blur-xs text-white text-[11px] font-bold px-2.5 py-0.5 rounded-md">
                        {poi.category}
                      </span>
                      <span className="bg-white/90 text-charcoal-800 text-[11px] font-bold px-2 py-0.5 rounded-md">
                        {poi.indoor_outdoor}
                      </span>
                    </div>
                  </div>

                  <div className="p-5 space-y-2.5">
                    <h3 className="font-bold text-base text-charcoal-900 group-hover:text-brand-600 transition-colors">
                      {poi.name}
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">
                      {poi.description}
                    </p>

                    <div className="flex items-center gap-4 text-xs text-slate-600 pt-2 border-t border-rose-50">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-brand-500" />
                        {poi.duration_minutes} mins
                      </span>
                      <span className="flex items-center gap-1 font-semibold text-charcoal-900">
                        <BadgeDollarSign className="w-3.5 h-3.5 text-emerald-600" />
                        {poi.entry_fee_inr === 0 ? 'Free Entry' : `₹${poi.entry_fee_inr} fee`}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="p-5 pt-0">
                  <button 
                    onClick={() => onPlanTrip(`${data.name}, ${data.country_name}`)}
                    className="w-full py-2.5 rounded-xl bg-rose-50 hover:bg-brand-500 hover:text-white text-brand-700 font-bold text-xs transition-all flex items-center justify-center gap-1.5"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Include in AI Itinerary</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 2: WHERE TO STAY */}
      {(activeTab === 'all' || activeTab === 'stays') && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <span className="badge-rose text-xs font-bold">Where Should You Stay?</span>
              <h2 className="text-2xl font-extrabold text-charcoal-900 mt-1">Best Hotels, Resorts & Stays</h2>
            </div>
            <span className="text-xs text-amber-700 bg-amber-50 px-3 py-1 rounded-full font-bold border border-amber-200">
              Demo / Mock Availability
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {data.stays.map((hotel) => (
              <div key={hotel.id} className="card-clean overflow-hidden flex flex-col justify-between group">
                <div>
                  <div className="h-44 overflow-hidden relative bg-charcoal-900">
                    <img 
                      src={hotel.image_url || data.image_url || FALLBACK_STAY} 
                      alt={hotel.name} 
                      onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_STAY; }}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                    />
                    <span className="absolute top-3 left-3 bg-charcoal-900/80 text-white text-[11px] font-bold px-2.5 py-0.5 rounded-md">
                      {hotel.property_type}
                    </span>
                    <div className="absolute bottom-3 right-3 bg-white/95 text-charcoal-900 font-extrabold text-xs px-2 py-0.5 rounded-md shadow-xs flex items-center gap-1">
                      <Star className="w-3 h-3 text-amber-500 fill-amber-500" />
                      <span>{hotel.rating}</span>
                    </div>
                  </div>

                  <div className="p-4 space-y-2">
                    <h3 className="font-bold text-sm text-charcoal-900 line-clamp-1 group-hover:text-brand-600 transition-colors">
                      {hotel.name}
                    </h3>
                    <p className="text-[11px] text-slate-500 flex items-center gap-1">
                      <MapPin className="w-3 h-3 text-brand-500 shrink-0" />
                      <span className="truncate">{hotel.location_area} • {hotel.distance_to_attraction}</span>
                    </p>

                    {hotel.amenities && (
                      <div className="flex flex-wrap gap-1 pt-1">
                        {hotel.amenities.slice(0, 2).map((amenity, aIdx) => (
                          <span key={aIdx} className="text-[10px] bg-rose-50 text-brand-700 px-2 py-0.5 rounded font-medium">
                            {amenity}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="p-4 pt-2 border-t border-rose-50 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] text-slate-400 block">From</span>
                    <span className="text-sm font-extrabold text-brand-600">₹{hotel.price_per_night_inr.toLocaleString()}<span className="text-[10px] text-slate-500 font-normal">/night</span></span>
                  </div>
                  <button 
                    onClick={() => onBookItem?.({
                      id: hotel.id,
                      title: hotel.name,
                      type: 'stay',
                      price: Math.round(hotel.price_per_night_inr / 83) || 120,
                      location: `${hotel.location_area}, ${data.name}`,
                      rating: hotel.rating,
                      imageUrl: hotel.image_url || data.image_url
                    })}
                    className="btn-primary text-xs py-1.5 px-3"
                  >
                    <span>Book (Demo)</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 3: WHERE TO EAT & RESTAURANTS */}
      {(activeTab === 'all' || activeTab === 'food') && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <span className="badge-pink text-xs font-bold">Where Should You Eat?</span>
              <h2 className="text-2xl font-extrabold text-charcoal-900 mt-1">Best Local Food & Top Restaurants</h2>
            </div>
            <span className="text-xs text-slate-500 font-medium">Authentic & Hygiene-Checked</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {data.restaurants.map((rest) => (
              <div key={rest.id} className="card-clean overflow-hidden flex flex-col justify-between group">
                <div>
                  <div className="h-44 overflow-hidden relative bg-charcoal-900">
                    <img 
                      src={rest.image_url || data.image_url || FALLBACK_FOOD} 
                      alt={rest.name} 
                      onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_FOOD; }}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                    />
                    <span className="absolute top-3 left-3 bg-charcoal-900/80 text-white text-[11px] font-bold px-2.5 py-0.5 rounded-md">
                      {rest.category}
                    </span>
                    <span className="absolute bottom-3 right-3 bg-white/95 text-charcoal-900 text-xs font-bold px-2 py-0.5 rounded-md">
                      {rest.price_level} • ~₹{rest.avg_meal_cost_inr}/meal
                    </span>
                  </div>

                  <div className="p-5 space-y-2.5">
                    <div className="flex items-center justify-between">
                      <h3 className="font-bold text-base text-charcoal-900 group-hover:text-brand-600 transition-colors">
                        {rest.name}
                      </h3>
                      <div className="flex items-center gap-1 text-xs font-extrabold text-amber-500">
                        <Star className="w-3.5 h-3.5 fill-amber-400" />
                        <span>{rest.rating}</span>
                      </div>
                    </div>

                    <p className="text-xs text-brand-700 font-semibold">{rest.cuisine_type}</p>
                    <p className="text-xs text-slate-500 leading-relaxed">{rest.description}</p>

                    {rest.popular_dishes && (
                      <div className="pt-2">
                        <span className="text-[11px] font-bold text-charcoal-800 block mb-1">Famous Dishes:</span>
                        <div className="flex flex-wrap gap-1">
                          {rest.popular_dishes.map((dish, dIdx) => (
                            <span key={dIdx} className="text-[10px] bg-rose-50 text-charcoal-700 px-2 py-0.5 rounded font-medium">
                              {dish}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="p-5 pt-0">
                  <button 
                    onClick={() => onBookItem?.({
                      id: rest.id,
                      title: `Reservation: ${rest.name}`,
                      type: 'experience',
                      price: Math.round(rest.avg_meal_cost_inr / 83) || 25,
                      location: `${rest.location_area}, ${data.name}`,
                      rating: rest.rating,
                      imageUrl: rest.image_url || data.image_url
                    })}
                    className="w-full py-2.5 rounded-xl bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-700 font-bold text-xs transition-all flex items-center justify-center gap-1.5"
                  >
                    <Utensils className="w-3.5 h-3.5" />
                    <span>Reserve Table (Demo)</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 4: LOCAL GUIDES & EXPERIENCES */}
      {(activeTab === 'all' || activeTab === 'guides') && data.guides.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div>
            <span className="badge-rose text-xs font-bold">Local Experts</span>
            <h2 className="text-2xl font-extrabold text-charcoal-900 mt-1">Verified Local Guides in {data.name}</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {data.guides.map((guide) => (
              <div key={guide.id} className="card-clean p-5 flex items-start gap-4">
                <img 
                  src={guide.avatarUrl || "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"} 
                  alt={guide.name} 
                  onError={(e) => { (e.currentTarget as HTMLImageElement).src = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"; }}
                  className="w-16 h-16 rounded-2xl object-cover border-2 border-rose-200 shrink-0" 
                />
                <div className="flex-1 space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-bold text-sm text-charcoal-900">{guide.name}</h4>
                      <p className="text-xs text-brand-600 font-medium">{guide.specialization || 'Heritage & Culture'}</p>
                    </div>
                    <div className="text-right">
                      <span className="text-xs font-extrabold text-brand-700">₹{guide.hourlyRate}/hr</span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-500 leading-relaxed">{guide.bio}</p>
                  
                  <div className="flex items-center justify-between pt-2">
                    <span className="text-[11px] text-slate-400">{guide.languages?.join(', ')} • {guide.experienceYears}y exp</span>
                    <button 
                      onClick={() => onBookItem?.({
                        id: guide.id,
                        title: `Private Tour with ${guide.name}`,
                        type: 'guide',
                        price: Math.round(guide.hourlyRate * 3 / 83) || 60,
                        location: data.name,
                        rating: guide.rating,
                        imageUrl: guide.avatarUrl
                      })}
                      className="btn-primary text-xs py-1.5 px-3"
                    >
                      <span>Book Guide</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 5: DESTINATION VIDEOS */}
      {(activeTab === 'all' || activeTab === 'videos') && data.videos.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div>
            <span className="badge-pink text-xs font-bold">Visual Preview</span>
            <h2 className="text-2xl font-extrabold text-charcoal-900 mt-1">Destination Videos</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {data.videos.map((vid) => (
              <div 
                key={vid.id}
                onClick={() => setActiveVideoModal(vid.title)}
                className="card-clean overflow-hidden group cursor-pointer"
              >
                <div className="h-56 relative overflow-hidden bg-charcoal-900">
                  <img 
                    src={vid.thumbnail_url || data.image_url || FALLBACK_HERO} 
                    alt={vid.title} 
                    onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_HERO; }}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                  <div className="absolute inset-0 bg-charcoal-900/40 flex items-center justify-center group-hover:bg-charcoal-900/30 transition-colors">
                    <div className="w-14 h-14 rounded-full bg-brand-500 text-white flex items-center justify-center shadow-glow-pink group-hover:scale-110 transition-transform">
                      <Play className="w-6 h-6 fill-white ml-0.5" />
                    </div>
                  </div>
                  <span className="absolute bottom-3 right-3 bg-charcoal-900/80 text-white text-xs font-bold px-2 py-0.5 rounded">
                    {vid.duration_str}
                  </span>
                </div>
                <div className="p-4">
                  <h4 className="font-bold text-sm text-charcoal-900 group-hover:text-brand-600 transition-colors">{vid.title}</h4>
                  <p className="text-xs text-slate-500 mt-0.5">{vid.category}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SECTION 6: TRAVEL REQUIREMENTS & VISA */}
      {(activeTab === 'all' || activeTab === 'requirements') && data.travel_requirement && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="p-6 sm:p-8 bg-rose-50/70 border border-rose-200 rounded-3xl space-y-4">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-6 h-6 text-brand-600" />
              <h3 className="text-lg font-bold text-charcoal-900">Official Travel & Visa Requirements ({data.country_name})</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
              <div className="p-4 rounded-2xl bg-white border border-rose-100 space-y-1">
                <span className="font-bold text-brand-700 block">Passport & Entry Rules</span>
                <p className="text-slate-600">{data.travel_requirement.passport_validity}</p>
              </div>

              <div className="p-4 rounded-2xl bg-white border border-rose-100 space-y-1">
                <span className="font-bold text-brand-700 block">Visa Requirements</span>
                <p className="text-slate-600">{data.travel_requirement.visa_requirement}</p>
              </div>

              <div className="p-4 rounded-2xl bg-white border border-rose-100 space-y-1">
                <span className="font-bold text-brand-700 block">Customs & Currency</span>
                <p className="text-slate-600">{data.travel_requirement.customs_advisory}</p>
              </div>

              <div className="p-4 rounded-2xl bg-white border border-rose-100 space-y-1">
                <span className="font-bold text-brand-700 block">Official Government Portal</span>
                <p className="text-slate-600">{data.travel_requirement.official_portal_url}</p>
              </div>
            </div>

            <p className="text-[11px] text-brand-800 italic pt-2">
              ⚠️ {data.travel_requirement.disclaimer}
            </p>
          </div>
        </section>
      )}

      {/* Video Modal Placeholder */}
      {activeVideoModal && (
        <div className="fixed inset-0 bg-charcoal-900/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 space-y-4 relative">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-base text-charcoal-900">{activeVideoModal}</h3>
              <button onClick={() => setActiveVideoModal(null)} className="p-1 hover:bg-slate-100 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="h-64 sm:h-80 bg-charcoal-900 rounded-2xl flex flex-col items-center justify-center text-white text-center p-6 space-y-3">
              <Play className="w-12 h-12 text-rose-500 animate-pulse" />
              <p className="text-sm font-semibold">Video Guide Stream Ready</p>
              <p className="text-xs text-slate-400">Embedded video simulation for {activeVideoModal}. Ready for YouTube / CDN video provider integration.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

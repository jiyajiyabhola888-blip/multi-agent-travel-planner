import React, { useState, useEffect, useRef } from 'react';
import { 
  MapPin, 
  Sparkles, 
  Compass, 
  Star, 
  ChevronRight, 
  Filter, 
  Globe, 
  ArrowRight, 
  Search,
  Plus,
  Minus,
  Maximize2,
  RefreshCw,
  Layers
} from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { getMapDestinations } from '../../services/api';

interface WorldMapExplorerProps {
  onSelectDestination: (cityIdentifier: string) => void;
  onPlanTrip: (cityName: string) => void;
}

export interface MapDestination {
  id: number;
  city: string;
  name: string;
  region: string;
  country: string;
  country_code: string;
  continent: string;
  latitude: number;
  longitude: number;
  image_url: string;
  vibe: string;
  category: string;
  avg_daily_budget_inr: number;
  best_months: string;
  rating: number;
  poi_count: number;
  canonical_id: string;
  canonical_name: string;
}

const FALLBACK_IMAGE = "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&auto=format&fit=crop&q=80";

export const WorldMapExplorer: React.FC<WorldMapExplorerProps> = ({
  onSelectDestination,
  onPlanTrip,
}) => {
  const [destinations, setDestinations] = useState<MapDestination[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedRegion, setSelectedRegion] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeLocation, setActiveLocation] = useState<MapDestination | null>(null);

  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markersLayerRef = useRef<L.LayerGroup | null>(null);
  const markersMapRef = useRef<{ [key: string]: L.Marker }>({});

  // 1. Fetch map destination coordinates from backend
  useEffect(() => {
    setLoading(true);
    getMapDestinations()
      .then((data: MapDestination[]) => {
        if (data && data.length > 0) {
          setDestinations(data);
          // Set initial active location
          const jaipur = data.find(d => d.city.toLowerCase().includes('jaipur')) || data[0];
          setActiveLocation(jaipur);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load map destinations:", err);
        setLoading(false);
      });
  }, []);

  // 2. Initialize Leaflet Map Instance
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Create real interactive world map
    const map = L.map(mapContainerRef.current, {
      center: [24, 20],
      zoom: 2.5,
      minZoom: 2,
      maxZoom: 17,
      zoomControl: false,
      worldCopyJump: true,
      attributionControl: true,
    });

    // Real OpenStreetMap Tile Layer (CartoDB Voyager style for sleek luxury aesthetics)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
    }).addTo(map);

    const markersGroup = L.layerGroup().addTo(map);
    markersLayerRef.current = markersGroup;
    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // 3. Render and update map pins when destinations or filters change
  useEffect(() => {
    const map = mapInstanceRef.current;
    const markersGroup = markersLayerRef.current;
    if (!map || !markersGroup) return;

    markersGroup.clearLayers();
    markersMapRef.current = {};

    const filtered = destinations.filter((loc) => {
      const regionMatch = selectedRegion === 'all' || 
        (loc.continent && loc.continent.toLowerCase() === selectedRegion.toLowerCase()) ||
        (loc.country && loc.country.toLowerCase() === selectedRegion.toLowerCase());
      
      const searchMatch = !searchQuery.trim() || 
        loc.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
        loc.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (loc.vibe && loc.vibe.toLowerCase().includes(searchQuery.toLowerCase()));

      return regionMatch && searchMatch;
    });

    filtered.forEach((loc) => {
      if (!loc.latitude || !loc.longitude) return;

      const isSelected = activeLocation?.id === loc.id;

      // Custom Rose Glassmorphic Pin
      const customIcon = L.divIcon({
        className: 'custom-leaflet-marker',
        html: `
          <div class="relative flex items-center justify-center cursor-pointer group">
            <div class="absolute -inset-2 bg-rose-500/25 rounded-full blur-xs transition-all group-hover:scale-150 ${isSelected ? 'scale-150 ring-4 ring-rose-400/40' : ''}"></div>
            <div class="relative w-8 h-8 rounded-2xl flex items-center justify-center shadow-lg transition-transform duration-300 ${isSelected ? 'bg-gradient-to-tr from-rose-600 to-brand-500 scale-110 text-white ring-2 ring-white' : 'bg-white text-rose-600 border border-rose-200 group-hover:bg-rose-600 group-hover:text-white'}">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
            </div>
            <div class="absolute top-full mt-1 px-2 py-0.5 rounded-md bg-charcoal-900/90 text-white text-[10px] font-bold tracking-tight shadow-md whitespace-nowrap pointer-events-none transition-opacity ${isSelected ? 'opacity-100' : 'opacity-85 group-hover:opacity-100'}">
              ${loc.city}
            </div>
          </div>
        `,
        iconSize: [32, 42],
        iconAnchor: [16, 21],
        popupAnchor: [0, -22],
      });

      const marker = L.marker([loc.latitude, loc.longitude], { icon: customIcon });

      // Click to focus and select
      marker.on('click', () => {
        setActiveLocation(loc);
        map.flyTo([loc.latitude, loc.longitude], Math.max(map.getZoom(), 5), {
          duration: 1.2,
          easeLinearity: 0.25,
        });
      });

      markersGroup.addLayer(marker);
      markersMapRef.current[loc.id] = marker;
    });
  }, [destinations, selectedRegion, searchQuery, activeLocation?.id]);

  const handleSelectLocationCard = (loc: MapDestination) => {
    setActiveLocation(loc);
    if (mapInstanceRef.current && loc.latitude && loc.longitude) {
      mapInstanceRef.current.flyTo([loc.latitude, loc.longitude], 6, {
        duration: 1.4,
        easeLinearity: 0.25,
      });
    }
  };

  const handleZoomIn = () => {
    if (mapInstanceRef.current) mapInstanceRef.current.zoomIn();
  };

  const handleZoomOut = () => {
    if (mapInstanceRef.current) mapInstanceRef.current.zoomOut();
  };

  const handleResetView = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.flyTo([24, 20], 2.5, { duration: 1 });
      setActiveLocation(destinations[0] || null);
    }
  };

  const filteredLocations = destinations.filter((loc) => {
    const regionMatch = selectedRegion === 'all' || 
      (loc.continent && loc.continent.toLowerCase() === selectedRegion.toLowerCase()) ||
      (loc.country && loc.country.toLowerCase() === selectedRegion.toLowerCase());
    
    const searchMatch = !searchQuery.trim() || 
      loc.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
      loc.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (loc.vibe && loc.vibe.toLowerCase().includes(searchQuery.toLowerCase()));

    return regionMatch && searchMatch;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Top Banner Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-rose-200 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold mb-2">
            <Globe className="w-3.5 h-3.5 text-rose-600" />
            <span>Interactive OpenStreetMap Canvas</span>
          </div>
          <h1 className="font-serif text-3xl sm:text-4xl font-bold text-charcoal-900">
            Real Global World Map
          </h1>
          <p className="text-xs sm:text-sm text-charcoal-500 mt-1 max-w-2xl">
            Live geographic exploration powered by OpenStreetMap. Pan and zoom globally, click destination pins to inspect verified stays and attractions, or launch instant 15-agent itinerary planning.
          </p>
        </div>

        {/* Region Filter Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          {['all', 'Asia', 'Europe', 'Middle East'].map((r) => (
            <button
              key={r}
              onClick={() => setSelectedRegion(r)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-bold transition-all ${
                selectedRegion === r
                  ? 'bg-gradient-to-r from-brand-500 to-rose-600 text-white shadow-soft'
                  : 'bg-white text-charcoal-600 hover:bg-rose-50 border border-rose-200'
              }`}
            >
              {r === 'all' ? 'All Continents' : r}
            </button>
          ))}
        </div>
      </div>

      {/* Search & Map Quick Controls Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-3 rounded-2xl border border-rose-200 shadow-sm">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-rose-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search map destinations (e.g. Jaipur, Tokyo, Paris)..."
            className="w-full pl-9 pr-4 py-2 text-xs font-semibold text-charcoal-900 placeholder:text-charcoal-400 bg-rose-50/40 border border-rose-100 rounded-xl focus:outline-none focus:border-rose-400 focus:ring-2 focus:ring-rose-100"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto justify-end text-xs text-charcoal-600">
          <span className="font-semibold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-200">
            {filteredLocations.length} Destinations Available
          </span>
          <button
            onClick={handleResetView}
            className="p-2 rounded-xl bg-white border border-rose-200 hover:bg-rose-50 text-charcoal-700 hover:text-rose-600 transition-colors"
            title="Reset Global View"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Real Interactive Map Canvas Box */}
      <div className="relative w-full h-[520px] sm:h-[620px] rounded-3xl overflow-hidden border-2 border-rose-200 shadow-2xl bg-[#E6F0F6]">
        {/* Leaflet Map DOM Element */}
        <div ref={mapContainerRef} className="w-full h-full z-0" />

        {/* Custom Map Floating Zoom Controls */}
        <div className="absolute top-4 right-4 z-20 flex flex-col gap-1.5 shadow-lg">
          <button
            onClick={handleZoomIn}
            className="w-9 h-9 rounded-xl bg-white/95 backdrop-blur-md border border-rose-200 text-charcoal-800 hover:bg-rose-50 hover:text-rose-600 flex items-center justify-center font-bold text-sm shadow-sm transition-all"
            title="Zoom In"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            className="w-9 h-9 rounded-xl bg-white/95 backdrop-blur-md border border-rose-200 text-charcoal-800 hover:bg-rose-50 hover:text-rose-600 flex items-center justify-center font-bold text-sm shadow-sm transition-all"
            title="Zoom Out"
          >
            <Minus className="w-4 h-4" />
          </button>
          <button
            onClick={handleResetView}
            className="w-9 h-9 rounded-xl bg-white/95 backdrop-blur-md border border-rose-200 text-charcoal-800 hover:bg-rose-50 hover:text-rose-600 flex items-center justify-center font-bold text-sm shadow-sm transition-all"
            title="Reset View"
          >
            <Maximize2 className="w-4 h-4" />
          </button>
        </div>

        {/* Floating Active Location Card (Over Map) */}
        {activeLocation && (
          <div className="absolute bottom-4 left-4 right-4 sm:right-auto sm:max-w-sm bg-white/95 backdrop-blur-md rounded-3xl p-4 shadow-2xl border border-rose-200 animate-slide-up z-20">
            <div className="relative h-36 rounded-2xl overflow-hidden mb-3 bg-charcoal-900">
              <img
                src={activeLocation.image_url || FALLBACK_IMAGE}
                alt={activeLocation.city}
                onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_IMAGE; }}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/80 via-transparent to-transparent" />
              
              <span className="absolute top-2.5 left-2.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-charcoal-900/80 text-white backdrop-blur-xs">
                {activeLocation.category}
              </span>
              
              <span className="absolute top-2.5 right-2.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-white/95 text-amber-600 flex items-center gap-1 shadow-xs">
                <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
                <span>{activeLocation.rating || 4.9}</span>
              </span>

              <div className="absolute bottom-2.5 left-3 right-3 text-white">
                <h3 className="font-serif text-lg font-bold">
                  {activeLocation.city}
                </h3>
                <p className="text-[11px] text-rose-200">
                  {activeLocation.region ? `${activeLocation.region}, ${activeLocation.country}` : activeLocation.country}
                </p>
              </div>
            </div>

            <p className="text-xs text-charcoal-600 line-clamp-2 leading-relaxed">
              {activeLocation.vibe}
            </p>

            <div className="grid grid-cols-2 gap-2 my-2.5 text-[11px] py-2 border-y border-rose-100 text-charcoal-600">
              <div>
                <span className="text-charcoal-400 block text-[10px] uppercase font-bold">Best Months</span>
                <span className="font-semibold text-charcoal-800">{activeLocation.best_months}</span>
              </div>
              <div>
                <span className="text-charcoal-400 block text-[10px] uppercase font-bold">Est. Daily Cost</span>
                <span className="font-semibold text-rose-700">₹{activeLocation.avg_daily_budget_inr.toLocaleString()}</span>
              </div>
            </div>

            <div className="flex items-center gap-2 pt-1">
              <button
                onClick={() => onSelectDestination(activeLocation.canonical_id || String(activeLocation.id))}
                className="flex-1 btn-secondary text-xs py-2 px-3 flex items-center justify-center gap-1.5"
              >
                <Compass className="w-3.5 h-3.5 text-rose-600" />
                <span>Explore Hub</span>
              </button>
              <button
                onClick={() => onPlanTrip(`${activeLocation.city}, ${activeLocation.country}`)}
                className="flex-1 btn-primary text-xs py-2 px-3 flex items-center justify-center gap-1.5"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Plan with AI</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Destination Grid List Below Real Map */}
      <div className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <h2 className="font-serif text-xl font-bold text-charcoal-900">
            Available World Travelholic Hubs ({filteredLocations.length})
          </h2>
          <span className="text-xs text-charcoal-500">
            Click any destination to fly on the map or explore detailed stays & food
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {filteredLocations.map((loc) => {
            const isSelected = activeLocation?.id === loc.id;
            return (
              <div
                key={loc.id}
                className={`card-luxury overflow-hidden group cursor-pointer transition-all ${
                  isSelected ? 'ring-2 ring-rose-500 shadow-md' : 'bg-white'
                }`}
                onClick={() => handleSelectLocationCard(loc)}
              >
                <div className="relative h-44 overflow-hidden bg-charcoal-900">
                  <img
                    src={loc.image_url || FALLBACK_IMAGE}
                    alt={loc.city}
                    onError={(e) => { (e.currentTarget as HTMLImageElement).src = FALLBACK_IMAGE; }}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/85 via-charcoal-900/20 to-transparent" />
                  
                  <span className="absolute top-2.5 left-2.5 px-2 py-0.5 rounded-full text-[10px] font-bold bg-charcoal-900/80 text-white backdrop-blur-xs">
                    {loc.category}
                  </span>

                  <div className="absolute bottom-2.5 left-3 right-3 text-white">
                    <h4 className="font-serif font-bold text-base">{loc.city}</h4>
                    <p className="text-[11px] text-rose-200">{loc.country}</p>
                  </div>
                </div>

                <div className="p-4 space-y-3">
                  <p className="text-xs text-charcoal-500 line-clamp-1">{loc.vibe}</p>
                  
                  <div className="flex items-center justify-between pt-2 border-t border-rose-100">
                    <span className="text-xs font-bold text-rose-600">
                      ₹{loc.avg_daily_budget_inr.toLocaleString()}/day
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectDestination(loc.canonical_id || String(loc.id));
                      }}
                      className="text-xs font-bold text-charcoal-700 hover:text-rose-600 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform"
                    >
                      <span>Explore</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};


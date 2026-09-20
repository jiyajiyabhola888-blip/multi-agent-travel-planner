import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Globe, Landmark, Sparkles, ArrowRight, X } from 'lucide-react';
import { autocompleteDestinations } from '../../services/api';

interface GlobalSearchProps {
  onSelectDestination?: (destName: string, action?: 'view' | 'plan') => void;
  onSelectCity?: (cityIdentifier: string) => void;
  onPlanCity?: (cityName: string) => void;
  placeholder?: string;
  className?: string;
  autoFocus?: boolean;
}

export const GlobalSearch: React.FC<GlobalSearchProps> = ({
  onSelectDestination,
  onSelectCity,
  onPlanCity,
  placeholder = "Where do you want to explore? (e.g. Jaipur, Tokyo, Paris, Interlaken, Dubai, Bali)",
  className = "",
  autoFocus = false
}) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Debounced search autocomplete
  useEffect(() => {
    if (!query.trim() || query.length < 2) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    const timer = setTimeout(async () => {
      const results = await autocompleteDestinations(query.trim());
      setSuggestions(results);
      setLoading(false);
      setIsOpen(true);
    }, 180);

    return () => clearTimeout(timer);
  }, [query]);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (itemOrString: any, action: 'view' | 'plan' = 'view') => {
    let canonical = '';
    let canonicalId = '';
    let cityName = '';

    if (typeof itemOrString === 'string') {
      canonical = itemOrString;
      cityName = itemOrString.split(',')[0].trim();
      canonicalId = cityName.toLowerCase();
    } else if (itemOrString && typeof itemOrString === 'object') {
      canonical = itemOrString.canonical_value || itemOrString.title || '';
      cityName = itemOrString.title || itemOrString.canonical_value?.split(',')[0].trim() || '';
      canonicalId = itemOrString.canonical_id || (itemOrString.id ? `city:${itemOrString.id}` : cityName.toLowerCase());
      if (itemOrString.type === 'attraction' && itemOrString.city_id) {
        canonicalId = `city:${itemOrString.city_id}`;
      }
    }

    setQuery(canonical || cityName);
    setIsOpen(false);
    
    if (action === 'plan') {
      if (onPlanCity) onPlanCity(canonical || cityName);
      else if (onSelectDestination) onSelectDestination(canonical || cityName, 'plan');
    } else {
      if (onSelectCity) onSelectCity(canonicalId || cityName);
      else if (onSelectDestination) onSelectDestination(canonical || cityName, 'view');
    }
  };

  return (
    <div ref={containerRef} className={`relative w-full max-w-2xl mx-auto ${className}`}>
      {/* Search Input Bar with Rose/Blush Glow */}
      <div className="relative flex items-center bg-white rounded-full border-2 border-blush-200 shadow-xl hover:border-rose-300 focus-within:border-rose-500 focus-within:ring-4 focus-within:ring-rose-100 transition-all">
        <div className="pl-5 text-rose-500">
          <Search className="w-5 h-5" />
        </div>

        <input
          type="text"
          value={query}
          autoFocus={autoFocus}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && query.trim()) {
              if (suggestions.length > 0) {
                handleSelect(suggestions[0], 'view');
              } else {
                handleSelect(query.trim(), 'view');
              }
            }
          }}
          placeholder={placeholder}
          className="w-full pl-3 pr-10 py-3.5 sm:py-4 text-xs sm:text-sm font-semibold text-charcoal-900 placeholder:text-charcoal-400 focus:outline-none bg-transparent"
        />

        {query && (
          <button
            onClick={() => { setQuery(''); setSuggestions([]); }}
            className="pr-4 text-charcoal-400 hover:text-rose-600 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}

        <button
          onClick={() => query && handleSelect(query, 'view')}
          className="mr-2 hidden sm:inline-flex items-center gap-1.5 px-5 py-2.5 rounded-full btn-primary text-xs font-bold shadow-md shadow-rose-200"
        >
          <span>Search</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Autocomplete Dropdown */}
      {isOpen && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-3xl border border-blush-200 shadow-2xl z-50 overflow-hidden max-h-[380px] overflow-y-auto animate-scale-in">
          <div className="p-3 border-b border-blush-100 flex items-center justify-between bg-blush-50/50 px-5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-rose-700">
              Instant Global Suggestions
            </span>
            {loading && <span className="text-xs text-rose-500 animate-pulse">Searching...</span>}
          </div>

          <div className="divide-y divide-blush-100">
            {suggestions.map((item, idx) => (
              <div
                key={idx}
                className="p-4 hover:bg-blush-50/60 flex items-center justify-between cursor-pointer transition-colors group"
                onClick={() => handleSelect(item, 'view')}
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-2xl bg-blush-100 text-rose-600 flex items-center justify-center shrink-0 group-hover:bg-rose-600 group-hover:text-white transition-colors">
                    {item.type === 'country' ? (
                      <Globe className="w-4 h-4" />
                    ) : item.type === 'attraction' ? (
                      <Landmark className="w-4 h-4" />
                    ) : (
                      <MapPin className="w-4 h-4" />
                    )}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-sm text-charcoal-900 group-hover:text-rose-600 transition-colors">
                        {item.title}
                      </h4>
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-50 text-rose-700 uppercase">
                        {item.type}
                      </span>
                    </div>
                    {item.subtitle && (
                      <p className="text-xs text-charcoal-500 mt-0.5">{item.subtitle}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleSelect(item, 'plan');
                    }}
                    className="px-3 py-1.5 rounded-full bg-white border border-blush-200 text-rose-600 hover:bg-rose-50 text-xs font-bold flex items-center gap-1 shadow-xs transition-all"
                  >
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Plan AI</span>
                  </button>
                  <ArrowRight className="w-4 h-4 text-charcoal-300 group-hover:text-rose-500 group-hover:translate-x-0.5 transition-all" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

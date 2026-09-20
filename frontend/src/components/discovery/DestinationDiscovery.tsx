import React, { useState } from 'react';
import { Sparkles, MapPin, ArrowRight, Compass, ShieldCheck, Heart, Filter, Star, Eye } from 'lucide-react';

interface DestinationDiscoveryProps {
  onSelectDestination: (destName: string) => void;
  onExploreHub?: (city: string) => void;
  onBack: () => void;
}

export const DestinationDiscovery: React.FC<DestinationDiscoveryProps> = ({ 
  onSelectDestination, 
  onExploreHub,
  onBack 
}) => {
  const [filterContinent, setFilterContinent] = useState<string>('All');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const destinations = [
    {
      name: "Jaipur, Rajasthan, India",
      city: "Jaipur",
      cityId: "jaipur",
      country: "India",
      continent: "Asia",
      category: "Heritage",
      vibe: "The Pink City of Royal Fortresses, Palaces & Johari Bazaars",
      bestSeason: "Oct - Mar",
      estDailyBudget: "$90/day (₹7,500)",
      suitabilityScore: 98,
      suitabilityReason: "Ranked #1 for majestic forts, palace courtyards & vibrant traditional artisan crafts.",
      majorPois: ["Amber Palace", "Hawa Mahal", "City Palace", "Jantar Mantar"],
      image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Udaipur, Rajasthan, India",
      city: "Udaipur",
      cityId: "udaipur",
      country: "India",
      continent: "Asia",
      category: "Romantic",
      vibe: "The Venice of the East with Lake Pichola & Floating Marble Palaces",
      bestSeason: "Sep - Mar",
      estDailyBudget: "$110/day (₹9,200)",
      suitabilityScore: 97,
      suitabilityReason: "World-class romantic getaway with boat cruises, Jagmandir island & rooftop palace dining.",
      majorPois: ["City Palace Udaipur", "Lake Pichola", "Jagdish Temple", "Saheliyon-ki-Bari"],
      image: "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Tokyo, Japan",
      city: "Tokyo",
      cityId: "tokyo",
      country: "Japan",
      continent: "Asia",
      category: "Futuristic",
      vibe: "Cyberpunk Neon Skylines, Ancient Shinto Shrines & Michelin Ramen",
      bestSeason: "Mar - May, Oct - Nov",
      estDailyBudget: "$220/day (¥33,000)",
      suitabilityScore: 96,
      suitabilityReason: "Safest global solo/family travel with unmatched culinary craft and bullet trains.",
      majorPois: ["Shibuya Crossing", "Senso-ji Temple", "teamLab Planets", "Meiji Shrine"],
      image: "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Paris, France",
      city: "Paris",
      cityId: "paris",
      country: "France",
      continent: "Europe",
      category: "Romantic",
      vibe: "Haute Couture, Louvre Masterpieces & Haussmannian Cafes",
      bestSeason: "Apr - Oct",
      estDailyBudget: "$260/day (€240)",
      suitabilityScore: 95,
      suitabilityReason: "World-class cultural immersion, Louvre masterpieces, and Seine river walks.",
      majorPois: ["Eiffel Tower", "Louvre Museum", "Montmartre", "Sainte-Chapelle"],
      image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Interlaken, Switzerland",
      city: "Interlaken",
      cityId: "interlaken",
      country: "Switzerland",
      continent: "Europe",
      category: "Alpine",
      vibe: "Glacial Mountain Peaks, Cogwheel Trains & Crystal Alpine Lakes",
      bestSeason: "Year-round",
      estDailyBudget: "$280/day (CHF 260)",
      suitabilityScore: 97,
      suitabilityReason: "Unsurpassed alpine landscapes, cogwheel trains, and pristine fresh mountain air.",
      majorPois: ["Jungfraujoch Top of Europe", "Lake Brienz Cruise", "Grindelwald First", "Harder Kulm"],
      image: "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Dubai, United Arab Emirates",
      city: "Dubai",
      cityId: "dubai",
      country: "UAE",
      continent: "Middle East",
      category: "Luxury",
      vibe: "Futuristic Architecture, Desert Safaris & World-Class Shopping",
      bestSeason: "Nov - Apr",
      estDailyBudget: "$210/day (AED 780)",
      suitabilityScore: 94,
      suitabilityReason: "Ideal for family luxury, world-record skyscrapers, and desert safaris.",
      majorPois: ["Burj Khalifa", "Desert Safari Dunes", "Museum of the Future", "Dubai Mall"],
      image: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Bali, Indonesia",
      city: "Bali",
      cityId: "bali",
      country: "Indonesia",
      continent: "Asia",
      category: "Tropical",
      vibe: "Ubud Waterfalls, Sacred Temples & Coastal Sunsets",
      bestSeason: "Apr - Oct",
      estDailyBudget: "$95/day",
      suitabilityScore: 96,
      suitabilityReason: "Spiritual retreats, lush terraced jungles, surfing, and relaxing beach clubs.",
      majorPois: ["Ubud Sacred Monkey Forest", "Tegallalang Rice Terraces", "Tanah Lot Temple", "Uluwatu Cliff"],
      image: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&auto=format&fit=crop&q=80"
    },
    {
      name: "Goa, India",
      city: "Goa",
      cityId: "goa",
      country: "India",
      continent: "Asia",
      category: "Tropical",
      vibe: "Portuguese Latin Quarter, Arabian Sea Beaches & Coastal Seafood",
      bestSeason: "Nov - Feb",
      estDailyBudget: "$75/day (₹6,200)",
      suitabilityScore: 95,
      suitabilityReason: "Relaxed coastal lifestyle, historic churches, and serene sunset shacks.",
      majorPois: ["Fontainhas Latin Quarter", "Basilica of Bom Jesus", "Palolem Beach", "Chapora Fort"],
      image: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop&q=80"
    },
  ];

  const filtered = destinations.filter(d => {
    if (filterContinent !== 'All' && d.continent !== filterContinent) return false;
    if (selectedCategory !== 'All' && d.category !== selectedCategory) return false;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto my-8 px-4 sm:px-6 lg:px-8 space-y-8 animate-fade-in">
      {/* Header */}
      <div className="card-luxury p-6 sm:p-8 bg-white border border-blush-200 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              World Travelholic Global Network
            </div>
            <h1 className="font-serif text-3xl sm:text-4xl font-bold text-charcoal-900">
              Curated Destination Hubs
            </h1>
            <p className="text-xs text-charcoal-500 mt-1 max-w-xl">
              Discover discrete global destinations equipped with verified stays, video guides,
              authentic dining spots, and transparent AI suitability scores.
            </p>
          </div>
          <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-5 self-start sm:self-auto">
            Back to Planner
          </button>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 mt-6 pt-4 border-t border-blush-100 flex-wrap">
          <span className="text-xs font-bold text-charcoal-400 mr-2 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Continents:
          </span>
          {['All', 'Asia', 'Europe', 'Middle East'].map(tag => (
            <button
              key={tag}
              onClick={() => setFilterContinent(tag)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                filterContinent === tag 
                  ? 'bg-rose-600 text-white shadow-sm' 
                  : 'bg-cream text-charcoal-700 hover:bg-blush-100 border border-blush-200'
              }`}
            >
              {tag}
            </button>
          ))}

          <div className="h-4 w-[1px] bg-blush-200 mx-2 hidden sm:block" />

          <span className="text-xs font-bold text-charcoal-400 mr-2 flex items-center gap-1">
            Vibe:
          </span>
          {['All', 'Heritage', 'Romantic', 'Alpine', 'Luxury', 'Tropical'].map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-full text-[11px] font-semibold transition-all ${
                selectedCategory === cat 
                  ? 'bg-rose-500 text-white' 
                  : 'bg-white text-charcoal-600 hover:bg-blush-50 border border-blush-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Destination Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((dest) => (
          <div key={dest.cityId} className="card-luxury overflow-hidden group flex flex-col justify-between">
            <div>
              {/* Image with Tag */}
              <div className="relative h-52 overflow-hidden">
                <img 
                  src={dest.image} 
                  alt={dest.name} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                />
                <div className="absolute top-3 right-3 bg-white/95 backdrop-blur-md px-2.5 py-1 rounded-full text-[11px] font-bold text-charcoal-900 shadow-sm flex items-center gap-1">
                  <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
                  {dest.suitabilityScore}% Match
                </div>
                <div className="absolute bottom-3 left-3 bg-charcoal-900/80 backdrop-blur-sm text-white px-2.5 py-0.5 rounded-full text-[10px] font-semibold">
                  Best: {dest.bestSeason}
                </div>
              </div>

              {/* Body */}
              <div className="p-5 space-y-3">
                <div>
                  <h3 className="font-serif font-bold text-lg text-charcoal-900 leading-snug">{dest.name}</h3>
                  <p className="text-xs text-charcoal-500 mt-0.5">{dest.vibe}</p>
                </div>

                <p className="text-xs text-charcoal-700 leading-relaxed bg-blush-50/70 p-3 rounded-2xl border border-blush-200">
                  {dest.suitabilityReason}
                </p>

                <div className="space-y-1.5">
                  <span className="text-[10px] font-bold text-charcoal-400 block uppercase tracking-wider">
                    Key Highlights:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {dest.majorPois.map(p => (
                      <span key={p} className="text-[10px] bg-cream text-charcoal-700 px-2.5 py-0.5 rounded-md border border-blush-100">
                        {p}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="p-5 pt-0 flex items-center gap-2 border-t border-blush-100 mt-2">
              <button
                onClick={() => onExploreHub?.(dest.cityId)}
                className="flex-1 btn-secondary text-xs py-2 px-3 flex items-center justify-center gap-1"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Explore Hub</span>
              </button>
              <button
                onClick={() => onSelectDestination(dest.name)}
                className="flex-1 btn-primary text-xs py-2 px-3 flex items-center justify-center gap-1 shadow-sm"
              >
                <span>Plan Trip</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

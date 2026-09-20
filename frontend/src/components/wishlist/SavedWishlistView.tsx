import React, { useState, useEffect } from 'react';
import { Heart, MapPin, Star, Sparkles, Trash2, ArrowRight, Compass, Hotel, Utensils } from 'lucide-react';
import { apiService } from '../../services/api';

interface SavedWishlistViewProps {
  onPlanTripForDestination: (city: string) => void;
  onExploreDestination: (city: string) => void;
  onBookItem: (item: any) => void;
}

export const SavedWishlistView: React.FC<SavedWishlistViewProps> = ({
  onPlanTripForDestination,
  onExploreDestination,
  onBookItem,
}) => {
  const [filter, setFilter] = useState<'all' | 'destination' | 'stay' | 'restaurant' | 'experience'>('all');
  const [items, setItems] = useState<any[]>([
    {
      id: 'fav-1',
      item_type: 'destination',
      item_id: 'jaipur',
      title: 'Jaipur, Rajasthan',
      subtitle: 'The Pink City of Maharajas & Forts',
      image_url: 'https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=1000&q=80',
      rating: 4.9,
      tags: ['Heritage', 'Culture', 'Luxury Palaces'],
      price: '$120/day',
    },
    {
      id: 'fav-2',
      item_type: 'stay',
      item_id: 'stay-jp-1',
      title: 'The Raj Palace Heritage Grand Suite',
      subtitle: 'Jaipur, Rajasthan, India',
      image_url: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1000&q=80',
      rating: 4.9,
      tags: ['Heritage Palace', 'Spa', 'Pool'],
      price: '$350/night',
    },
    {
      id: 'fav-3',
      item_type: 'destination',
      item_id: 'tokyo',
      title: 'Tokyo, Japan',
      subtitle: 'Futuristic Metropolises & Timeless Temples',
      image_url: 'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1000&q=80',
      rating: 4.95,
      tags: ['Modern', 'Culinary', 'Culture'],
      price: '$220/day',
    },
    {
      id: 'fav-4',
      item_type: 'destination',
      item_id: 'paris',
      title: 'Paris, France',
      subtitle: 'City of Lights, Art & Haute Cuisine',
      image_url: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1000&q=80',
      rating: 4.9,
      tags: ['Romance', 'Museums', 'Gastronomy'],
      price: '$280/day',
    },
  ]);

  const removeItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  const filteredItems = items.filter((item) => filter === 'all' || item.item_type === filter);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-blush-200 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold mb-2">
            <Heart className="w-3.5 h-3.5 fill-rose-500 text-rose-500" />
            Curated Inspiration
          </div>
          <h1 className="font-serif text-3xl font-bold text-charcoal-900">Saved Wishlist</h1>
          <p className="text-xs text-charcoal-500 mt-1">
            Your saved dreamy destinations, luxury stays, and memorable bucket-list experiences.
          </p>
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          {[
            { id: 'all', label: 'All Items' },
            { id: 'destination', label: 'Destinations' },
            { id: 'stay', label: 'Stays' },
            { id: 'experience', label: 'Experiences' },
          ].map((f) => (
            <button
              key={f.id}
              onClick={() => setFilter(f.id as any)}
              className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all ${
                filter === f.id
                  ? 'bg-rose-600 text-white shadow-sm'
                  : 'bg-cream text-charcoal-600 hover:bg-blush-100 border border-blush-200'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Empty State */}
      {filteredItems.length === 0 ? (
        <div className="p-12 text-center card-luxury max-w-md mx-auto space-y-4">
          <div className="w-16 h-16 rounded-full bg-blush-100 text-rose-500 flex items-center justify-center mx-auto text-2xl">
            💔
          </div>
          <h3 className="font-serif text-lg font-bold text-charcoal-900">Your wishlist is empty</h3>
          <p className="text-xs text-charcoal-500">
            Explore global destinations or browse our luxury stays catalog and tap the heart icon to
            save them here.
          </p>
        </div>
      ) : (
        /* Grid */
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="card-luxury overflow-hidden group flex flex-col justify-between"
            >
              <div>
                <div className="relative h-52 overflow-hidden">
                  <img
                    src={item.image_url}
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/70 via-transparent to-transparent" />

                  <button
                    onClick={() => removeItem(item.id)}
                    className="absolute top-3 right-3 p-2 rounded-full bg-white/80 hover:bg-white text-rose-600 shadow-md backdrop-blur-sm transition-all"
                    title="Remove from wishlist"
                  >
                    <Heart className="w-4 h-4 fill-rose-600" />
                  </button>

                  <span className="absolute top-3 left-3 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-charcoal-900/80 text-white backdrop-blur-sm">
                    {item.item_type}
                  </span>

                  <div className="absolute bottom-3 left-3 right-3 text-white">
                    <h3 className="font-serif text-lg font-bold line-clamp-1">{item.title}</h3>
                    <p className="text-xs text-blush-200 line-clamp-1">{item.subtitle}</p>
                  </div>
                </div>

                <div className="p-5 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="flex items-center gap-1 font-bold text-amber-600">
                      <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                      {item.rating}
                    </span>
                    <span className="font-bold text-rose-600">{item.price}</span>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {item.tags?.map((t: string, idx: number) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded-md bg-blush-50 text-[10px] text-charcoal-600 border border-blush-100"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="p-5 pt-0 border-t border-blush-100 mt-2 flex items-center justify-between gap-2">
                <button
                  onClick={() =>
                    onExploreDestination(
                      item.item_type === 'destination' ? item.item_id : 'jaipur'
                    )
                  }
                  className="text-xs font-semibold text-charcoal-600 hover:text-rose-600 flex items-center gap-1"
                >
                  <Compass className="w-3.5 h-3.5" />
                  Explore Hub
                </button>
                <button
                  onClick={() =>
                    item.item_type === 'destination'
                      ? onPlanTripForDestination(item.title)
                      : onBookItem({
                          id: item.item_id,
                          title: item.title,
                          type: item.item_type,
                          price: parseInt(item.price.replace(/[^0-9]/g, '')) || 150,
                          imageUrl: item.image_url,
                          location: item.subtitle,
                        })
                  }
                  className="btn-primary text-xs py-2 px-4 flex items-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  {item.item_type === 'destination' ? 'Plan AI Trip' : 'Book Now'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

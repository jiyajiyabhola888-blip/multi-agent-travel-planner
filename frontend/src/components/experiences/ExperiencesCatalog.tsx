import React, { useState } from 'react';
import { Sparkles, Star, MapPin, Clock, Users, ArrowRight, Heart } from 'lucide-react';
import { MOCK_EXPERIENCES } from '../../services/mockData';

interface ExperiencesCatalogProps {
  onBack?: () => void;
  onBookExperience?: (title: string) => void;
}

export const ExperiencesCatalog: React.FC<ExperiencesCatalogProps> = ({ onBack, onBookExperience }) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const filtered = MOCK_EXPERIENCES.filter(exp => {
    if (selectedCategory === 'All') return true;
    return exp.category.toLowerCase().includes(selectedCategory.toLowerCase());
  });

  return (
    <div className="max-w-6xl mx-auto my-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="card-clean p-6 sm:p-8 bg-white border border-slate-100 shadow-soft">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="badge-pink text-xs px-2.5 py-1">Authentic Culture</span>
            <h1 className="text-3xl font-extrabold text-navy-900 mt-2">Local Experience Marketplace</h1>
            <p className="text-sm text-slate-500 mt-1">
              Hand-picked workshops, culinary safaris, and secret village treks led by native artisans and guides.
            </p>
          </div>
          {onBack && (
            <button onClick={onBack} className="btn-secondary text-xs py-2.5 px-4 self-start sm:self-auto">
              Back to Trip
            </button>
          )}
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-2 mt-6 pt-4 border-t border-slate-100 flex-wrap">
          <span className="text-xs font-bold text-slate-400 mr-2">Categories:</span>
          {['All', 'Culinary Tour', 'Craft & Workshop', 'Village Experience'].map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                selectedCategory === cat ? 'bg-brand-600 text-white shadow-soft' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Experience Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {filtered.map(exp => (
          <div key={exp.id} className="card-clean overflow-hidden group flex flex-col justify-between">
            <div>
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={exp.imageUrl} 
                  alt={exp.title} 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute top-3 left-3 badge-pink text-[10px] px-2 py-0.5 shadow-soft">
                  {exp.category}
                </div>
                <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-md px-2 py-0.5 rounded-full text-[11px] font-bold text-navy-900 flex items-center gap-1 shadow-soft">
                  <Star className="w-3 h-3 text-amber-500 fill-amber-400" />
                  <span>{exp.rating}</span>
                </div>
              </div>

              <div className="p-5 space-y-2.5">
                <div className="flex items-center gap-3 text-xs text-slate-400 font-medium">
                  <span className="flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-brand-600" />
                    <span>{exp.city}</span>
                  </span>
                  <span>•</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-brand-600" />
                    <span>{exp.durationHours} hrs</span>
                  </span>
                </div>

                <h3 className="font-bold text-base text-navy-900 leading-snug">{exp.title}</h3>
                <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">{exp.description}</p>
              </div>
            </div>

            <div className="p-5 pt-0 flex items-center justify-between border-t border-slate-100 mt-4">
              <div>
                <span className="text-[10px] text-slate-400 block uppercase font-bold">From</span>
                <span className="text-base font-extrabold text-brand-600">{exp.currency} {exp.pricePerPerson.toLocaleString()}</span>
              </div>

              <button
                onClick={() => onBookExperience?.(exp.title)}
                className="btn-primary text-xs py-2 px-4 shadow-soft"
              >
                <span>Reserve Experience</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

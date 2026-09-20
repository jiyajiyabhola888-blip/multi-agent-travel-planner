import React, { useState } from 'react';
import { X, Calendar, Users, DollarSign, Shield, CheckCircle2, Clock, MapPin, Star, AlertCircle } from 'lucide-react';
import { BookingItem } from '../../types';

interface BookingModalProps {
  isOpen: boolean;
  onClose: () => void;
  item: BookingItem | null;
  onProceedToPayment: (bookingData: {
    item: BookingItem;
    startDate: string;
    endDate?: string;
    guests: number;
    specialRequests: string;
    totalPrice: number;
  }) => void;
}

export const BookingModal: React.FC<BookingModalProps> = ({
  isOpen,
  onClose,
  item,
  onProceedToPayment,
}) => {
  const [startDate, setStartDate] = useState(
    new Date(Date.now() + 86400000 * 3).toISOString().split('T')[0]
  );
  const [endDate, setEndDate] = useState(
    new Date(Date.now() + 86400000 * 6).toISOString().split('T')[0]
  );
  const [guests, setGuests] = useState(2);
  const [specialRequests, setSpecialRequests] = useState('');

  if (!isOpen || !item) return null;

  // Calculate pricing
  const nights = Math.max(
    1,
    Math.round(
      (new Date(endDate).getTime() - new Date(startDate).getTime()) /
        (1000 * 60 * 60 * 24)
    )
  );

  const pricePerUnit = item.price || 120;
  const multiplier = item.type === 'stay' ? nights : 1;
  const basePrice = pricePerUnit * multiplier * (item.type === 'experience' ? guests : 1);
  const taxesAndFees = Math.round(basePrice * 0.12);
  const totalPrice = basePrice + taxesAndFees;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onProceedToPayment({
      item,
      startDate,
      endDate: item.type === 'stay' ? endDate : undefined,
      guests,
      specialRequests,
      totalPrice,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-charcoal-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-blush-200 overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="relative p-6 bg-gradient-to-r from-blush-50 via-cream to-rose-50 border-b border-blush-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-rose-500/10 border border-rose-200 flex items-center justify-center text-rose-600 font-bold">
              {item.type === 'stay' ? '🏨' : item.type === 'guide' ? '🧭' : '✨'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-serif text-lg font-bold text-charcoal-900">
                  Instant Booking Request
                </h3>
                <span className="badge-demo text-[10px]">SANDBOX DEMO</span>
              </div>
              <p className="text-xs text-charcoal-500">
                Reserve your {item.type} with flexible cancellation
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-full text-charcoal-400 hover:text-charcoal-700 hover:bg-blush-100/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-6 flex-1">
          {/* Selected Item Summary Card */}
          <div className="p-4 rounded-2xl bg-cream border border-blush-200 flex items-center gap-4">
            {item.imageUrl ? (
              <img
                src={item.imageUrl}
                alt={item.title}
                className="w-20 h-20 rounded-xl object-cover border border-blush-200 shadow-sm"
              />
            ) : (
              <div className="w-20 h-20 rounded-xl bg-blush-100 flex items-center justify-center text-2xl">
                🌍
              </div>
            )}
            <div className="flex-1 min-w-0">
              <span className="text-[10px] font-bold tracking-wider uppercase text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">
                {item.type}
              </span>
              <h4 className="font-bold text-charcoal-900 text-sm truncate mt-1">
                {item.title}
              </h4>
              {item.location && (
                <p className="text-xs text-charcoal-500 flex items-center gap-1 mt-0.5">
                  <MapPin className="w-3 h-3 text-rose-500" />
                  {item.location}
                </p>
              )}
              <div className="flex items-center gap-3 mt-1 text-xs">
                {item.rating && (
                  <span className="flex items-center gap-0.5 font-bold text-amber-600">
                    <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
                    {item.rating}
                  </span>
                )}
                <span className="font-bold text-rose-600">
                  ${pricePerUnit}
                  <span className="text-[10px] text-charcoal-400 font-normal">
                    /{item.type === 'stay' ? 'night' : 'person'}
                  </span>
                </span>
              </div>
            </div>
          </div>

          {/* Form Inputs */}
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-charcoal-700 mb-1.5 flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-rose-500" />
                  {item.type === 'stay' ? 'Check-in Date' : 'Experience Date'}
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="input-blush"
                  required
                />
              </div>

              {item.type === 'stay' && (
                <div>
                  <label className="block text-xs font-semibold text-charcoal-700 mb-1.5 flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5 text-rose-500" />
                    Check-out Date ({nights} night{nights > 1 ? 's' : ''})
                  </label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="input-blush"
                    required
                  />
                </div>
              )}

              <div className={item.type !== 'stay' ? 'sm:col-span-2' : ''}>
                <label className="block text-xs font-semibold text-charcoal-700 mb-1.5 flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-rose-500" />
                  Number of Guests
                </label>
                <select
                  value={guests}
                  onChange={(e) => setGuests(parseInt(e.target.value))}
                  className="input-blush"
                >
                  {[1, 2, 3, 4, 5, 6, 8, 10].map((num) => (
                    <option key={num} value={num}>
                      {num} {num === 1 ? 'Guest' : 'Guests'}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-charcoal-700 mb-1.5">
                Special Requests or Notes (Optional)
              </label>
              <textarea
                value={specialRequests}
                onChange={(e) => setSpecialRequests(e.target.value)}
                placeholder="e.g. Quiet room high floor, airport pick-up, dietary preferences..."
                rows={2}
                className="input-blush resize-none"
              />
            </div>
          </div>

          {/* Pricing Breakdown Card */}
          <div className="p-4 rounded-2xl bg-blush-50/70 border border-blush-200 space-y-2 text-xs">
            <div className="flex justify-between text-charcoal-600">
              <span>
                Base Rate (${pricePerUnit} × {item.type === 'stay' ? `${nights} nights` : `${guests} guests`})
              </span>
              <span className="font-semibold text-charcoal-900">${basePrice}</span>
            </div>
            <div className="flex justify-between text-charcoal-600">
              <span>Estimated Taxes & Local Tourism Fees (12%)</span>
              <span className="font-semibold text-charcoal-900">${taxesAndFees}</span>
            </div>
            <div className="border-t border-blush-200 pt-2 flex justify-between items-baseline font-bold text-sm text-charcoal-900">
              <span>Estimated Total</span>
              <span className="text-base text-rose-600 font-serif">${totalPrice}</span>
            </div>
          </div>

          {/* Guarantee Badges */}
          <div className="flex items-center gap-4 text-[11px] text-charcoal-500 pt-1">
            <span className="flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-emerald-600" /> Free cancellation up to 48h
            </span>
            <span className="flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-rose-600" /> Instant verification
            </span>
          </div>

          {/* Action Footer */}
          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 rounded-full border border-blush-200 text-xs font-semibold text-charcoal-600 hover:bg-blush-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary flex items-center gap-2 text-xs py-2.5 px-6"
            >
              <DollarSign className="w-4 h-4" />
              Proceed to Sandbox Checkout (${totalPrice})
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

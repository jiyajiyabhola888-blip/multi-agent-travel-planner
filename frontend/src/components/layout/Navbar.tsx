import React, { useState, useEffect } from 'react';
import { 
  Globe, Sparkles, Heart, Bell, User, MessageSquare, Compass, 
  MapPin, Check, ChevronDown, CheckCircle2, DollarSign
} from 'lucide-react';
import { NotificationItem } from '../../types';
import { apiService } from '../../services/api';

interface NavbarProps {
  onNavigate?: (route: string) => void;
  activeRoute?: string;
  onOpenWanderAI?: () => void;
  wishlistCount?: number;
}

export const Navbar: React.FC<NavbarProps> = ({ 
  onNavigate, 
  activeRoute = 'home',
  onOpenWanderAI,
  wishlistCount = 4
}) => {
  const [selectedCurrency, setSelectedCurrency] = useState<'USD' | 'EUR' | 'GBP' | 'INR' | 'JPY'>('USD');
  const [showCurrencyDropdown, setShowCurrencyDropdown] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState(2);

  useEffect(() => {
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const data = await apiService.getNotifications();
      setNotifications(data);
      setUnreadCount(data.filter((n: NotificationItem) => !n.is_read).length);
    } catch {
      setNotifications([
        {
          id: 1,
          title: 'Jaipur Weather Update',
          message: 'Clear sunny skies forecasted for Amber Palace morning tour (24°C).',
          severity: 'info',
          is_read: false,
          created_at: '10m ago',
        },
        {
          id: 2,
          title: 'Sandbox Booking Confirmed',
          message: 'The Raj Palace Heritage Suite confirmed for Oct 15-19.',
          severity: 'success',
          is_read: false,
          created_at: '1h ago',
        },
      ]);
    }
  };

  const markAllRead = async () => {
    try {
      await apiService.markAllNotificationsRead();
      setNotifications((prev) => prev.map((n: NotificationItem) => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch {
      setNotifications((prev) => prev.map((n: NotificationItem) => ({ ...n, is_read: true })));
      setUnreadCount(0);
    }
  };

  const currencySymbols = {
    USD: '$ USD',
    EUR: '€ EUR',
    GBP: '£ GBP',
    INR: '₹ INR',
    JPY: '¥ JPY',
  };

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-blush-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Brand & Logo */}
          <div 
            className="flex items-center gap-3 cursor-pointer group"
            onClick={() => onNavigate?.('home')}
          >
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-rose-600 via-rose-500 to-warm-pink flex items-center justify-center text-white shadow-md shadow-rose-200 group-hover:scale-105 transition-transform">
              <Globe className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-serif font-extrabold text-lg sm:text-xl tracking-tight text-charcoal-900">
                  WORLD <span className="text-rose-600">TRAVELHOLIC</span>
                </span>
                <span className="text-sm">🌍</span>
              </div>
              <p className="text-[11px] text-charcoal-500 font-medium -mt-0.5 tracking-wide">
                Explore More. Travel Smarter.
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden lg:flex items-center gap-6 xl:gap-8">
            <button 
              onClick={() => onNavigate?.('home')}
              className={`text-xs font-bold transition-colors ${
                activeRoute === 'home' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              Overview
            </button>
            <button 
              onClick={() => onNavigate?.('discover')}
              className={`text-xs font-bold transition-colors ${
                activeRoute === 'discover' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              Destinations
            </button>
            <button 
              onClick={() => onNavigate?.('map-explorer')}
              className={`text-xs font-bold transition-colors flex items-center gap-1 ${
                activeRoute === 'map-explorer' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              <Compass className="w-3.5 h-3.5 text-rose-500" />
              World Map
            </button>
            <button 
              onClick={() => onNavigate?.('experiences')}
              className={`text-xs font-bold transition-colors ${
                activeRoute === 'experiences' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              Experiences
            </button>
            <button 
              onClick={() => onNavigate?.('guides')}
              className={`text-xs font-bold transition-colors ${
                activeRoute === 'guides' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              Local Guides
            </button>
            <button 
              onClick={() => onNavigate?.('my-trips')}
              className={`text-xs font-bold transition-colors ${
                activeRoute === 'my-trips' ? 'text-rose-600' : 'text-charcoal-600 hover:text-charcoal-900'
              }`}
            >
              My Trips
            </button>
          </nav>

          {/* Right Action Icons & CTAs */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Currency Selector */}
            <div className="relative hidden sm:block">
              <button
                onClick={() => setShowCurrencyDropdown(!showCurrencyDropdown)}
                className="px-2.5 py-1.5 rounded-xl border border-blush-200 text-[11px] font-bold text-charcoal-700 hover:bg-blush-50 transition-colors flex items-center gap-1"
              >
                <span>{currencySymbols[selectedCurrency]}</span>
                <ChevronDown className="w-3 h-3 text-charcoal-400" />
              </button>

              {showCurrencyDropdown && (
                <div className="absolute right-0 mt-2 w-32 bg-white rounded-2xl shadow-xl border border-blush-200 py-1.5 z-50 animate-scale-in">
                  {(['USD', 'EUR', 'GBP', 'INR', 'JPY'] as const).map((curr) => (
                    <button
                      key={curr}
                      onClick={() => {
                        setSelectedCurrency(curr);
                        setShowCurrencyDropdown(false);
                      }}
                      className={`w-full text-left px-3 py-1.5 text-xs flex items-center justify-between hover:bg-blush-50 ${
                        selectedCurrency === curr ? 'text-rose-600 font-bold' : 'text-charcoal-700'
                      }`}
                    >
                      <span>{currencySymbols[curr]}</span>
                      {selectedCurrency === curr && <Check className="w-3.5 h-3.5" />}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Saved Wishlist Heart */}
            <button
              onClick={() => onNavigate?.('wishlist')}
              className="relative p-2 rounded-xl text-charcoal-600 hover:text-rose-600 hover:bg-blush-50 transition-colors"
              title="Saved Wishlist"
            >
              <Heart className="w-5 h-5" />
              {wishlistCount > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-rose-600 text-white text-[9px] font-bold flex items-center justify-center ring-2 ring-white">
                  {wishlistCount}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 rounded-xl text-charcoal-600 hover:text-rose-600 hover:bg-blush-50 transition-colors"
                title="Notifications"
              >
                <Bell className="w-5 h-5" />
                {unreadCount > 0 && (
                  <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 rounded-full bg-rose-500 ring-2 ring-white animate-ping" />
                )}
              </button>

              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-3xl shadow-2xl border border-blush-200 p-4 z-50 animate-scale-in space-y-3">
                  <div className="flex items-center justify-between border-b border-blush-100 pb-2">
                    <span className="font-serif font-bold text-sm text-charcoal-900">
                      Notifications
                    </span>
                    <button
                      onClick={markAllRead}
                      className="text-[11px] text-rose-600 hover:underline font-semibold"
                    >
                      Mark all read
                    </button>
                  </div>

                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {notifications.map((n) => (
                      <div
                        key={n.id}
                        className={`p-3 rounded-2xl text-xs space-y-1 ${
                          n.is_read ? 'bg-cream/50 text-charcoal-600' : 'bg-blush-50 text-charcoal-900 font-medium'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-charcoal-900">{n.title}</span>
                          <span className="text-[10px] text-charcoal-400">{n.created_at}</span>
                        </div>
                        <p className="text-[11px] text-charcoal-600 leading-snug">{n.message}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* WanderAI Assistant Trigger */}
            <button
              onClick={onOpenWanderAI}
              className="hidden sm:flex items-center gap-1.5 px-3 py-2 rounded-2xl bg-gradient-to-r from-blush-100 to-rose-100 border border-blush-200 text-rose-700 hover:bg-rose-200 text-xs font-bold transition-all shadow-xs"
              title="Open WanderAI Concierge"
            >
              <MessageSquare className="w-3.5 h-3.5 text-rose-600" />
              <span>WanderAI</span>
            </button>

            {/* Plan My Trip Primary CTA */}
            <button 
              onClick={() => onNavigate?.('plan')}
              className="btn-primary text-xs py-2.5 px-4 sm:px-5 flex items-center gap-1.5 shadow-md shadow-rose-200"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Plan AI Trip</span>
            </button>

            {/* User Dashboard */}
            <button 
              onClick={() => onNavigate?.('dashboard')}
              className="p-2 text-charcoal-600 hover:text-rose-600 hover:bg-blush-50 rounded-xl transition-colors"
              title="Traveler Profile & Settings"
            >
              <User className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

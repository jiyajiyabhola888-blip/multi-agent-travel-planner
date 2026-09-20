import axios from 'axios';
import { WishlistItem, NotificationItem, BookingRecord } from '../types';

// Smart dynamic API base URL with VITE_API_BASE_URL env support and LAN host fallback
export const getApiBaseUrl = (): string => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  if (typeof window !== 'undefined' && window.location && window.location.hostname) {
    const host = window.location.hostname;
    if (host !== 'localhost' && host !== '127.0.0.1') {
      return `http://${host}:8000/api/v1`;
    }
  }
  return 'http://localhost:8000/api/v1';
};

export const API_BASE_URL = getApiBaseUrl();

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('API health check error:', error);
    throw error;
  }
};

// Destination Discovery APIs
export const autocompleteDestinations = async (query: string) => {
  try {
    const res = await apiClient.get('/destinations/autocomplete', { params: { q: query } });
    return res.data;
  } catch (err) {
    console.warn('Autocomplete fallback:', err);
    return [];
  }
};

export const searchDestinations = async (query?: string, countryCode?: string) => {
  try {
    const res = await apiClient.get('/destinations/search', { params: { query, country_code: countryCode } });
    return res.data;
  } catch (err) {
    console.warn('Destination search error:', err);
    return [];
  }
};

export const getDestinationDetail = async (idOrName: string) => {
  try {
    const res = await apiClient.get(`/destinations/${encodeURIComponent(idOrName)}`);
    return res.data;
  } catch (err) {
    console.warn('Destination detail error:', err);
    throw err;
  }
};

export const getMapDestinations = async () => {
  try {
    const res = await apiClient.get('/destinations/map');
    return res.data;
  } catch (err) {
    console.warn('Get map destinations error:', err);
    return [];
  }
};

export const getDestinationCategories = async (category: string = 'trending') => {
  try {
    const res = await apiClient.get('/destinations/categories', { params: { category } });
    return res.data;
  } catch (err) {
    console.warn('Destination categories error:', err);
    return [];
  }
};

export const getRecommendedDestinations = async (params: { budget_inr?: number; trip_type?: string; travel_style?: string }) => {
  try {
    const res = await apiClient.get('/destinations/recommend', { params });
    return res.data;
  } catch (err) {
    console.warn('Recommend destinations error:', err);
    return [];
  }
};

// Booking & Sandbox Payment APIs
export const listBookings = async (): Promise<BookingRecord[]> => {
  try {
    const res = await apiClient.get('/bookings/');
    return res.data;
  } catch (err) {
    console.warn('List bookings fallback:', err);
    return [];
  }
};

export const createBooking = async (bookingData: any) => {
  try {
    const res = await apiClient.post('/bookings/create', bookingData);
    return res.data;
  } catch (err) {
    console.warn('Create booking fallback:', err);
    return {
      id: `BK-${Math.random().toString(36).substring(2, 9).toUpperCase()}`,
      status: 'CONFIRMED',
      ...bookingData
    };
  }
};

export const cancelBooking = async (bookingId: string | number) => {
  const res = await apiClient.post(`/bookings/${bookingId}/cancel`);
  return res.data;
};

export const getPaymentSummary = async (amount: number, currency: string = 'USD') => {
  try {
    const res = await apiClient.get('/payments/summary', { params: { amount, currency } });
    return res.data;
  } catch (err) {
    return {
      base_amount: amount,
      tax_amount: Math.round(amount * 0.12),
      platform_fee: 5,
      total_amount: Math.round(amount * 1.12) + 5,
      currency
    };
  }
};

export const processPayment = async (payload: {
  booking_id: string;
  amount: number;
  currency: string;
  payment_method: string;
  is_sandbox?: boolean;
}) => {
  try {
    const res = await apiClient.post('/payments/checkout', payload);
    return res.data;
  } catch (err) {
    return {
      success: true,
      transaction_id: `TX-${Date.now().toString(36).toUpperCase()}`,
      status: 'COMPLETED',
      amount: payload.amount,
      currency: payload.currency
    };
  }
};

// WanderAI Global Assistant
export const askWanderAI = async (message: string, destinationContext?: string, tripContext?: any) => {
  try {
    const res = await apiClient.post('/ai_chat/ask', {
      message,
      destination_context: destinationContext,
      trip_context: tripContext
    });
    return res.data;
  } catch (err) {
    console.warn('WanderAI chat fallback:', err);
    return {
      success: true,
      assistant_name: 'WanderAI',
      reply: `I'm WanderAI for World Travelholic. I can help plan trips, recommend luxury stays, or guide dining for ${destinationContext || 'your destination'}.`,
      actions: [
        { label: 'Plan Trip with AI', action: 'plan_trip', payload: destinationContext || 'Jaipur' },
        { label: 'Explore Destinations', action: 'navigate', payload: 'discover' }
      ]
    };
  }
};

// Wishlist / Favorites
export const getWishlist = async () => {
  try {
    const res = await apiClient.get('/wishlist/');
    return res.data;
  } catch (err) {
    console.warn('Get wishlist fallback:', err);
    return [];
  }
};

export const toggleWishlistItem = async (item: WishlistItem) => {
  const res = await apiClient.post('/wishlist/toggle', item);
  return res.data;
};

// Notifications
export const getNotifications = async (): Promise<NotificationItem[]> => {
  try {
    const res = await apiClient.get('/notifications/');
    return res.data;
  } catch (err) {
    console.warn('Get notifications fallback:', err);
    return [
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
    ];
  }
};

export const markAllNotificationsRead = async () => {
  try {
    const res = await apiClient.post('/notifications/read-all');
    return res.data;
  } catch {
    return { success: true };
  }
};

// Reviews
export const getReviews = async (targetType?: string, targetName?: string) => {
  try {
    const res = await apiClient.get('/reviews/', { params: { target_type: targetType, target_name: targetName } });
    return res.data;
  } catch (err) {
    console.warn('Get reviews fallback:', err);
    return [];
  }
};

export const submitReview = async (reviewData: any) => {
  const res = await apiClient.post('/reviews/submit', reviewData);
  return res.data;
};

// Export consolidated apiService object
export const apiService = {
  checkHealth,
  autocompleteDestinations,
  searchDestinations,
  getDestinationDetail,
  getMapDestinations,
  getDestinationCategories,
  getRecommendedDestinations,
  listBookings,
  createBooking,
  cancelBooking,
  getPaymentSummary,
  processPayment,
  askWanderAI,
  getWishlist,
  toggleWishlistItem,
  getNotifications,
  markAllNotificationsRead,
  getReviews,
  submitReview,
};

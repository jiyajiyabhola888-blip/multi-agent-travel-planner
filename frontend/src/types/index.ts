// Comprehensive Global Types for WORLD TRAVELHOLIC 🌍

export type TripType = 
  | 'Honeymoon'
  | 'Family'
  | 'Friends'
  | 'Solo'
  | 'Business'
  | 'Backpacking'
  | 'Adventure'
  | 'Relaxation'
  | 'Food & Culture'
  | 'Photography'
  | 'Luxury'
  | 'Budget'
  | 'Custom';

export type TravelStyle = 'Budget' | 'Balanced' | 'Luxury';
export type TravelPace = 'Relaxed' | 'Balanced' | 'Packed' | 'Adventure';

export interface TripWizardState {
  tripType: TripType;
  destination: string;
  startLocation: string;
  numTravelers: number;
  startDate: string;
  endDate: string;
  numDays: number;
  totalBudget: number;
  currency: string;
  travelStyle: TravelStyle;
  travelPace: TravelPace;
  interests: string[];
  foodPreferences: string[];
  accommodationPreference: string;
  transportationPreference: string;
  specialRequirements: string;
}

export interface AgentDebateMessage {
  agent_name: string;
  agent_role: string;
  stance: string;
  message: string;
  proposed_adjustments?: string[];
  timestamp?: string;
  metadata?: any;
}

export interface ActivityItemSchema {
  id: string;
  order_index: number;
  time_slot: string;
  start_time: string;
  end_time: string;
  activity_name: string;
  category: string;
  location_name: string;
  estimated_cost: number;
  transit_time_from_prev_mins: number;
  transit_mode: string;
  buffer_security_mins: number;
  booking_required: boolean;
  why_explanation: string;
  is_indoor: boolean;
}

export interface ItineraryDaySchema {
  day_number: number;
  date: string;
  theme: string;
  city_name: string;
  weather_summary: string;
  daily_budget_allocated: number;
  daily_cost_estimated: number;
  activities: ActivityItemSchema[];
}

export interface TripResponse {
  id: number;
  title: string;
  trip_type: string;
  destination: string;
  start_location: string;
  start_date: string;
  end_date: string;
  num_days: number;
  num_travelers: number;
  total_budget: number;
  currency: string;
  travel_style: string;
  travel_pace: string;
  budget_breakdown: Record<string, number>;
  readiness_score: number;
  debate_log: AgentDebateMessage[];
  itinerary_days: ItineraryDaySchema[];
  created_at: string;
}

export interface AttractionItem {
  id: number;
  name: string;
  category: string;
  duration_minutes: number;
  entry_fee_inr: number;
  indoor_outdoor: string;
  opening_hours?: string;
  best_time_of_day?: string;
  description?: string;
  image_url?: string;
}

export interface HotelStayItem {
  id: number;
  name: string;
  property_type: string;
  price_per_night_inr: number;
  rating: number;
  review_count: number;
  location_area: string;
  distance_to_attraction: string;
  amenities: string[];
  image_url?: string;
  description?: string;
  is_demo_availability: boolean;
}

export interface RestaurantVenueItem {
  id: number;
  name: string;
  cuisine_type: string;
  category: string;
  price_level: string;
  avg_meal_cost_inr: number;
  rating: number;
  review_count: number;
  location_area: string;
  popular_dishes: string[];
  dietary_tags: string[];
  opening_hours?: string;
  image_url?: string;
  description?: string;
  is_demo_reservation: boolean;
}

export interface DestinationVideoItem {
  id: number;
  title: string;
  duration_str: string;
  thumbnail_url?: string;
  video_url?: string;
  category: string;
}

export interface TravelRequirementInfo {
  passport_validity: string;
  visa_requirement: string;
  customs_advisory: string;
  currency_regulations: string;
  official_portal_url?: string;
  disclaimer: string;
}

export interface DestinationDetail {
  id: number;
  name: string;
  region_name: string;
  country_name: string;
  country_code: string;
  currency_code: string;
  timezone: string;
  latitude: number;
  longitude: number;
  avg_daily_budget_inr: number;
  best_months: string;
  vibe: string;
  description: string;
  image_url: string;
  attractions: AttractionItem[];
  stays: HotelStayItem[];
  restaurants: RestaurantVenueItem[];
  videos: DestinationVideoItem[];
  guides: LocalGuideProfile[];
  experiences: LocalExperienceItem[];
  travel_requirement?: TravelRequirementInfo;
}

export interface LocalGuideProfile {
  id: string | number;
  name: string;
  avatarUrl?: string;
  city: string;
  country?: string;
  experienceYears: number;
  languages: string[];
  hourlyRate: number;
  currency: string;
  services?: string[];
  rating: number;
  reviewsCount?: number;
  review_count?: number;
  verified?: boolean;
  specialization?: string;
  bio: string;
}

export interface LocalExperienceItem {
  id: string | number;
  guideId?: string | number;
  title: string;
  category: string;
  city?: string;
  city_name?: string;
  durationHours?: number;
  duration_hours?: number;
  pricePerPerson?: number;
  price_per_person?: number;
  currency: string;
  rating: number;
  review_count?: number;
  description: string;
  imageUrl?: string;
  highlights?: string[];
}

export interface BookingItem {
  id: string | number;
  title: string;
  type: 'stay' | 'guide' | 'experience' | 'activity';
  price: number;
  location?: string;
  rating?: number;
  imageUrl?: string;
  meta?: Record<string, any>;
}

export interface BookingRecord {
  id: string;
  item_type: string;
  title: string;
  destination: string;
  start_date: string;
  end_date?: string;
  guests: number;
  total_price: number;
  currency: string;
  status: string;
  is_sandbox?: boolean;
  created_at?: string;
}

export interface TripBookingItem {
  id: number;
  booking_reference: string;
  booking_type: string;
  title: string;
  provider_name: string;
  destination_name: string;
  start_date: string;
  end_date?: string;
  guests_count: number;
  amount: number;
  currency: string;
  status: 'Pending' | 'Confirmed' | 'Cancelled' | 'Completed';
  is_sandbox_mock: boolean;
  cancellation_policy: string;
  details?: Record<string, any>;
  created_at: string;
}

export interface WishlistItem {
  id?: number | string;
  item_type: 'destination' | 'hotel' | 'restaurant' | 'attraction' | 'guide' | 'experience' | 'stay';
  item_id: string;
  title: string;
  subtitle?: string;
  location?: string;
  image_url?: string;
  price_info?: string;
  price?: string;
  rating?: number;
  tags?: string[];
}

export interface NotificationItem {
  id: number | string;
  title: string;
  message: string;
  type?: 'info' | 'warning' | 'alert' | 'success';
  category?: string;
  severity?: 'info' | 'warning' | 'alert' | 'success';
  is_read: boolean;
  action_link?: string;
  created_at: string;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  city?: string;
  actions?: Array<{ label: string; action: string; payload: Record<string, any> }>;
  timestamp: string;
}

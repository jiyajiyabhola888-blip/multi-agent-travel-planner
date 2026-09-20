from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TripCreateRequest(BaseModel):
    trip_type: str = Field(default="Family", description="Honeymoon, Family, Friends, Solo, Business, Adventure, Relaxation, Custom")
    start_location: str = Field(default="Delhi, India")
    destination: str = Field(default="Jaipur, Rajasthan, India")
    start_date: str = Field(default="2026-10-15")
    end_date: str = Field(default="2026-10-20")
    num_days: int = Field(default=5)
    num_travelers: int = Field(default=2)
    total_budget: float = Field(default=50000.0)
    currency: str = Field(default="INR")
    travel_style: str = Field(default="Balanced") # Budget, Balanced, Luxury
    travel_pace: str = Field(default="Balanced")   # Relaxed, Balanced, Packed, Adventure
    interests: List[str] = Field(default=["Heritage", "Photography", "Food"])
    food_preferences: List[str] = Field(default=["Vegetarian", "Local Street Food"])
    accommodation_preference: str = Field(default="Boutique Hotel / 4-Star")
    transportation_preference: str = Field(default="Private Cab & Trains")
    special_requirements: Optional[str] = None


class ActivityItemSchema(BaseModel):
    id: str
    order_index: int
    time_slot: str
    start_time: str
    end_time: str
    activity_name: str
    category: str
    location_name: str
    estimated_cost: float
    transit_time_from_prev_mins: int
    transit_mode: str
    buffer_security_mins: int
    booking_required: bool
    why_explanation: str
    is_indoor: bool


class ItineraryDaySchema(BaseModel):
    day_number: int
    date: str
    theme: str
    city_name: str
    weather_summary: str
    daily_budget_allocated: float
    daily_cost_estimated: float
    activities: List[ActivityItemSchema]


class AgentMessageSchema(BaseModel):
    agent_name: str
    agent_role: str
    stance: str
    message: str
    proposed_adjustments: List[str] = []
    metadata: Optional[Dict[str, Any]] = None


class TripResponse(BaseModel):
    id: int
    title: str
    trip_type: str
    destination: str
    start_location: str
    start_date: str
    end_date: str
    num_days: int
    num_travelers: int
    total_budget: float
    currency: str
    travel_style: str
    travel_pace: str
    budget_breakdown: Dict[str, float]
    readiness_score: int
    debate_log: List[AgentMessageSchema]
    itinerary_days: List[ItineraryDaySchema]
    created_at: str


class SimulationRequest(BaseModel):
    trip_id: int
    scenario_type: str # rain, delay, budget_cut, attraction_closed, traveler_cancel
    custom_notes: Optional[str] = None


class RecoveryRequest(BaseModel):
    trip_id: int
    incident_type: str # cancelled_train, severe_rain, flight_delay, attraction_shut
    affected_day: int = 1
    details: str = "Train was cancelled due to track maintenance."


class ServiceBookingRequest(BaseModel):
    guide_id: Optional[int] = None
    experience_id: Optional[int] = None
    traveler_name: str
    traveler_contact: str
    travel_date: str
    num_guests: int = 2
    special_notes: Optional[str] = None

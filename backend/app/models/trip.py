from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON, Date, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(100), index=True, nullable=True)
    title = Column(String(255), nullable=False)
    trip_type = Column(String(50), default="Family") # Honeymoon, Family, Friends, Solo, Business, Adventure, Relaxation, Custom
    start_location = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    num_days = Column(Integer, default=5)
    num_travelers = Column(Integer, default=2)
    total_budget = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    travel_style = Column(String(50), default="Balanced") # Budget, Balanced, Luxury
    travel_pace = Column(String(50), default="Balanced")   # Relaxed, Balanced, Packed, Adventure
    interests = Column(JSON, default=list)
    food_preferences = Column(JSON, default=list)
    accommodation_pref = Column(String(100), default="Boutique Hotel / 4-Star")
    transport_pref = Column(String(100), default="Private Cab & Trains")
    special_requirements = Column(Text, nullable=True)
    status = Column(String(50), default="planned") # planned, active, completed, recovering
    
    # Budget allocation cache
    budget_breakdown = Column(JSON, nullable=True) # {transport: x, hotel: y, food: z, activities: a, guide: g, misc: m}
    readiness_score = Column(Integer, default=8)   # out of 10
    created_at = Column(DateTime, default=datetime.utcnow)

    days = relationship("ItineraryDay", back_populates="trip", cascade="all, delete-orphan")
    debate_logs = relationship("AgentDebateLog", back_populates="trip", cascade="all, delete-orphan")
    simulations = relationship("TripSimulation", back_populates="trip", cascade="all, delete-orphan")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    theme = Column(String(200), default="Arrival & Exploration")
    city_name = Column(String(100), nullable=False)
    weather_summary = Column(String(200), default="Sunny 24°C, Low humidity")
    daily_budget_allocated = Column(Float, default=10000.0)
    daily_cost_estimated = Column(Float, default=9500.0)

    trip = relationship("Trip", back_populates="days")
    activities = relationship("ItineraryActivity", back_populates="day", cascade="all, delete-orphan")


class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itinerary_days.id"), nullable=False)
    order_index = Column(Integer, default=1)
    time_slot = Column(String(50), default="Morning") # Morning, Breakfast, Lunch, Afternoon, Evening, Dinner, Night
    start_time = Column(String(20), default="09:00")
    end_time = Column(String(20), default="11:30")
    activity_name = Column(String(255), nullable=False)
    category = Column(String(100), default="Sightseeing")
    location_name = Column(String(255), nullable=False)
    estimated_cost = Column(Float, default=500.0)
    transit_time_from_prev_mins = Column(Integer, default=20)
    transit_mode = Column(String(50), default="Cab / Walking")
    buffer_security_mins = Column(Integer, default=15)
    booking_required = Column(Boolean, default=False)
    why_explanation = Column(Text, nullable=True)
    is_indoor = Column(Boolean, default=False)

    day = relationship("ItineraryDay", back_populates="activities")


class AgentDebateLog(Base):
    __tablename__ = "agent_debate_logs"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    round_number = Column(Integer, default=1)
    agent_name = Column(String(100), nullable=False)
    agent_role = Column(String(100), nullable=False)
    stance = Column(String(50), default="propose") # propose, critique, support, verdict
    message = Column(Text, nullable=False)
    proposed_adjustment = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="debate_logs")

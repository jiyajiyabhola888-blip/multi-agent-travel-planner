from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="traveler")  # traveler, guide, admin
    home_city = Column(String(255), default="Delhi, India")
    home_currency = Column(String(10), default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)


class TravelPreferenceMemory(Base):
    __tablename__ = "travel_preference_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)  # nullable for demo session memory
    session_id = Column(String(100), index=True, nullable=True)
    travel_style = Column(String(50), default="Balanced")  # Budget, Balanced, Luxury
    travel_pace = Column(String(50), default="Balanced")   # Relaxed, Balanced, Packed, Adventure
    interests = Column(JSON, default=list)                 # ["Heritage", "Photography", "Food"]
    food_preferences = Column(JSON, default=list)          # ["Vegetarian", "Street Food", "Local Seafood"]
    accommodation_pref = Column(String(100), default="Boutique Hotel / 4-Star")
    transport_pref = Column(String(100), default="Private Cab & Trains")
    special_requirements = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

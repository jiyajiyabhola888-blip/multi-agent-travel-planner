from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON
from app.core.database import Base


class LocalGuide(Base):
    __tablename__ = "local_guides"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    city_name = Column(String(100), nullable=False)
    country_name = Column(String(100), default="India")
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    experience_years = Column(Integer, default=5)
    languages_spoken = Column(JSON, default=lambda: ["English", "Hindi"])
    hourly_rate = Column(Float, default=800.0)
    currency = Column(String(10), default="INR")
    services_offered = Column(JSON, default=lambda: ["Walking Tour", "Food Walk", "Historical Commentary"])
    rating = Column(Float, default=4.9)
    review_count = Column(Integer, default=42)
    verified = Column(Boolean, default=True)
    contact_phone = Column(String(50), nullable=True)
    specialization = Column(String(100), default="Heritage & Hidden Gems")

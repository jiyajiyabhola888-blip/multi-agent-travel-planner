from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False) # "IN", "AE", "FR", "CH", "JP", etc.
    name = Column(String(100), nullable=False)
    continent = Column(String(50), default="Asia")
    currency_code = Column(String(10), default="INR")
    timezone = Column(String(50), default="Asia/Kolkata")
    visa_guidelines = Column(Text, nullable=True)
    hero_image = Column(String(500), nullable=True)

    regions = relationship("RegionState", back_populates="country", cascade="all, delete-orphan")


class RegionState(Base):
    __tablename__ = "regions_states"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    name = Column(String(100), nullable=False)
    is_union_territory = Column(Boolean, default=False)
    description = Column(Text, nullable=True)

    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region", cascade="all, delete-orphan")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions_states.id"), nullable=False)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    avg_daily_budget_inr = Column(Float, default=4000.0)
    best_months = Column(String(100), default="Oct-Mar")
    vibe = Column(String(100), default="Heritage & Culture")
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    region = relationship("RegionState", back_populates="cities")
    pois = relationship("AttractionPOI", back_populates="city", cascade="all, delete-orphan")
    hotels = relationship("HotelStay", back_populates="city", cascade="all, delete-orphan")
    restaurants = relationship("RestaurantVenue", back_populates="city", cascade="all, delete-orphan")
    videos = relationship("DestinationVideo", back_populates="city", cascade="all, delete-orphan")


class AttractionPOI(Base):
    __tablename__ = "attractions_pois"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), default="Sightseeing")  # Heritage, Nature, Adventure, Culinary, Shopping
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    avg_duration_minutes = Column(Integer, default=90)
    entry_fee_inr = Column(Float, default=0.0)
    indoor_outdoor = Column(String(20), default="Outdoor")  # Indoor, Outdoor, Mixed
    opening_hours = Column(String(100), default="09:00 - 18:00")
    best_time_of_day = Column(String(50), default="Morning") # Morning, Afternoon, Evening, Sunset
    family_friendly = Column(Boolean, default=True)
    honeymoon_score = Column(Float, default=4.0)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    city = relationship("City", back_populates="pois")


class HotelStay(Base):
    __tablename__ = "hotel_stays"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(200), nullable=False)
    property_type = Column(String(100), default="Hotel")  # Hotel, Resort, Hostel, Boutique, Heritage, Villa
    price_per_night_inr = Column(Float, default=3500.0)
    rating = Column(Float, default=4.6)
    review_count = Column(Integer, default=85)
    location_area = Column(String(200), default="City Center")
    distance_to_attraction = Column(String(100), default="1.5 km from center")
    amenities = Column(JSON, default=list)  # ["Free WiFi", "Pool", "Spa", "Breakfast Included"]
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_demo_availability = Column(Boolean, default=True)

    city = relationship("City", back_populates="hotels")


class RestaurantVenue(Base):
    __tablename__ = "restaurant_venues"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    name = Column(String(200), nullable=False)
    cuisine_type = Column(String(100), default="Local Cuisine")
    category = Column(String(100), default="Top Restaurant")  # Top Restaurant, Street Food, Fine Dining, Cafe, Vegetarian, Vegan
    price_level = Column(String(10), default="$$")  # $, $$, $$$, $$$$
    avg_meal_cost_inr = Column(Float, default=600.0)
    rating = Column(Float, default=4.7)
    review_count = Column(Integer, default=120)
    location_area = Column(String(200), default="Heritage Quarter")
    popular_dishes = Column(JSON, default=list)
    opening_hours = Column(String(100), default="11:00 AM - 11:00 PM")
    dietary_tags = Column(JSON, default=list)  # ["Vegetarian", "Vegan Options", "Halal"]
    image_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_demo_reservation = Column(Boolean, default=True)

    city = relationship("City", back_populates="restaurants")


class DestinationVideo(Base):
    __tablename__ = "destination_videos"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    title = Column(String(200), nullable=False)
    duration_str = Column(String(20), default="4:15")
    thumbnail_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)
    category = Column(String(100), default="Destination Guide")

    city = relationship("City", back_populates="videos")


class TravelRequirement(Base):
    __tablename__ = "travel_requirements"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String(10), unique=True, nullable=False)
    passport_validity = Column(String(200), default="Valid for at least 6 months beyond arrival date.")
    visa_requirement = Column(String(500), default="Check official embassy or government portal for current visa requirements.")
    customs_advisory = Column(String(500), default="Standard international declaration rules apply.")
    currency_regulations = Column(String(500), default="Local and foreign currency limits regulated by central bank.")
    official_portal_url = Column(String(500), nullable=True)
    verification_disclaimer = Column(Text, default="Always verify current visa and health regulations on official government portals before traveling.")


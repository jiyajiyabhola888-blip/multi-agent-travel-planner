from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class TripSimulation(Base):
    __tablename__ = "trip_simulations"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    scenario_name = Column(String(200), nullable=False) # e.g. "What if it rains?", "What if flight delayed 3h?"
    scenario_type = Column(String(100), nullable=False) # rain, delay, budget_cut, attraction_closed, traveler_cancel
    impact_summary = Column(Text, nullable=False)
    budget_delta = Column(Float, default=0.0)
    time_delta_mins = Column(Integer, default=0)
    modified_itinerary_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="simulations")


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    guide_id = Column(Integer, ForeignKey("local_guides.id"), nullable=True)
    experience_id = Column(Integer, ForeignKey("local_experiences.id"), nullable=True)
    traveler_name = Column(String(200), nullable=False)
    traveler_contact = Column(String(100), nullable=False)
    travel_date = Column(String(50), nullable=False)
    num_guests = Column(Integer, default=2)
    special_notes = Column(Text, nullable=True)
    status = Column(String(50), default="Requested (Mock)") # Requested, Confirmed, Completed
    created_at = Column(DateTime, default=datetime.utcnow)


class TripReview(Base):
    __tablename__ = "trip_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    author_name = Column(String(200), default="Traveler")
    target_type = Column(String(50), default="destination") # destination, hotel, restaurant, guide, experience, platform
    target_name = Column(String(200), nullable=False)
    rating = Column(Float, default=5.0)
    review_title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=False)
    is_verified_booking = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TripBooking(Base):
    __tablename__ = "trip_bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String(50), unique=True, index=True, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    user_id = Column(Integer, nullable=True)
    booking_type = Column(String(50), nullable=False)  # Hotel, Flight, Train, Cab, Guide, Activity, Restaurant
    title = Column(String(255), nullable=False)
    provider_name = Column(String(100), default="World Travelholic Direct")
    destination_name = Column(String(100), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=True)
    guests_count = Column(Integer, default=2)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(String(50), default="Confirmed")  # Pending, Confirmed, Cancelled, Completed
    is_sandbox_mock = Column(Boolean, default=True)
    details_json = Column(JSON, default=dict)
    cancellation_policy = Column(String(255), default="Free cancellation up to 48 hours prior to start.")
    created_at = Column(DateTime, default=datetime.utcnow)


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    booking_id = Column(Integer, ForeignKey("trip_bookings.id"), nullable=True)
    user_id = Column(Integer, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    payment_method = Column(String(50), default="Sandbox Card")  # Sandbox Card, Mock UPI, Demo NetBanking, Sandbox ApplePay
    status = Column(String(50), default="Completed")  # Completed, Pending, Refunded, Failed
    tax_amount = Column(Float, default=0.0)
    service_fee = Column(Float, default=0.0)
    gateway_name = Column(String(50), default="World Travelholic Sandbox Gateway")
    invoice_number = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class FavoriteWishlist(Base):
    __tablename__ = "favorite_wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    item_type = Column(String(50), nullable=False)  # destination, hotel, restaurant, attraction, guide, experience
    item_id = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(200), nullable=True)
    location = Column(String(200), nullable=True)
    image_url = Column(String(500), nullable=True)
    price_info = Column(String(100), nullable=True)
    rating = Column(Float, default=4.8)
    created_at = Column(DateTime, default=datetime.utcnow)


class NotificationItem(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(50), default="Trip Update")  # Booking, Weather, Flight, Recovery, Reminder, System
    severity = Column(String(20), default="info")  # info, warning, alert, success
    is_read = Column(Boolean, default=False)
    action_link = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


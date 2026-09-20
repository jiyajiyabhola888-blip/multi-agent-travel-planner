from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from app.core.database import Base


class LocalExperience(Base):
    __tablename__ = "local_experiences"

    id = Column(Integer, primary_key=True, index=True)
    guide_id = Column(Integer, ForeignKey("local_guides.id"), nullable=True)
    city_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Cultural Experience")  # Food Tour, Photography Walk, Village Tour, Trekking, Boat Ride, Workshop
    duration_hours = Column(Float, default=3.0)
    price_per_person = Column(Float, default=1200.0)
    currency = Column(String(10), default="INR")
    max_group_size = Column(Integer, default=8)
    meeting_point = Column(String(255), default="City Center Landmark")
    rating = Column(Float, default=4.92)
    review_count = Column(Integer, default=28)
    description = Column(Text, nullable=True)
    highlights = Column(JSON, default=list)
    image_url = Column(String(500), nullable=True)

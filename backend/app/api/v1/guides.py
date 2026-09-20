from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.guide import LocalGuide
from app.models.simulation import ServiceRequest
from app.schemas.trip import ServiceBookingRequest

router = APIRouter(prefix="/guides", tags=["Local Guides & Traveler Connection"])


@router.get("/")
def list_local_guides(
    city: Optional[str] = Query(None, description="Filter guides by city name"),
    specialization: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Discovers verified local tour guides, drivers, photographers, and trekkers."""
    q = db.query(LocalGuide)
    if city:
        q = q.filter(LocalGuide.city_name.ilike(f"%{city}%"))
    if specialization:
        q = q.filter(LocalGuide.specialization.ilike(f"%{specialization}%"))
    
    guides = q.all()
    return [
        {
            "id": g.id,
            "full_name": g.full_name,
            "city_name": g.city_name,
            "country_name": g.country_name,
            "avatar_url": g.avatar_url or f"https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            "bio": g.bio,
            "experience_years": g.experience_years,
            "languages_spoken": g.languages_spoken,
            "hourly_rate": g.hourly_rate,
            "currency": g.currency,
            "services_offered": g.services_offered,
            "rating": g.rating,
            "review_count": g.review_count,
            "verified": g.verified,
            "specialization": g.specialization,
            "badge": "Vetted Local Guide"
        }
        for g in guides
    ]


@router.post("/request-service")
def request_guide_service(req: ServiceBookingRequest, db: Session = Depends(get_db)):
    """Allows travelers to request guide services. Mock mode clearly labeled."""
    booking = ServiceRequest(
        guide_id=req.guide_id,
        experience_id=req.experience_id,
        traveler_name=req.traveler_name,
        traveler_contact=req.traveler_contact,
        travel_date=req.travel_date,
        num_guests=req.num_guests,
        special_notes=req.special_notes,
        status="Requested (Demo / Mock Mode)"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "success": True,
        "booking_id": booking.id,
        "status": booking.status,
        "message": f"Service request submitted for {req.traveler_name}! The local guide has been notified.",
        "is_mock": True,
        "mock_disclaimer": "This is a prototype demonstration. No real financial payment was processed."
    }

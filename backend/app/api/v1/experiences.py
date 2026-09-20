from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.experience import LocalExperience

router = APIRouter(prefix="/experiences", tags=["Local Experiences Marketplace"])


@router.get("/")
def list_experiences(
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Lists authentic local experiences: food tours, workshops, treks, village visits."""
    q = db.query(LocalExperience)
    if city:
        q = q.filter(LocalExperience.city_name.ilike(f"%{city}%"))
    if category:
        q = q.filter(LocalExperience.category.ilike(f"%{category}%"))

    experiences = q.all()
    return [
        {
            "id": exp.id,
            "title": exp.title,
            "category": exp.category,
            "city_name": exp.city_name,
            "duration_hours": exp.duration_hours,
            "price_per_person": exp.price_per_person,
            "currency": exp.currency,
            "max_group_size": exp.max_group_size,
            "meeting_point": exp.meeting_point,
            "rating": exp.rating,
            "review_count": exp.review_count,
            "description": exp.description,
            "highlights": exp.highlights,
            "badge": "Authentic Local Experience"
        }
        for exp in experiences
    ]

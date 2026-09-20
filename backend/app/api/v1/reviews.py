from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.simulation import TripReview

router = APIRouter(prefix="/reviews", tags=["Traveler Reviews & Ratings"])


class ReviewCreateSchema(BaseModel):
    target_type: str = "destination"  # destination, hotel, restaurant, guide, experience
    target_name: str
    author_name: str = "Verified Traveler"
    rating: float = 5.0
    review_title: Optional[str] = None
    comment: str


@router.get("/")
def get_reviews(
    target_type: Optional[str] = None,
    target_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieves verified traveler reviews."""
    q = db.query(TripReview)
    if target_type:
        q = q.filter(TripReview.target_type == target_type)
    if target_name:
        q = q.filter(TripReview.target_name.ilike(f"%{target_name}%"))

    reviews = q.order_by(TripReview.id.desc()).limit(30).all()
    return [
        {
            "id": r.id,
            "author_name": r.author_name,
            "target_type": r.target_type,
            "target_name": r.target_name,
            "rating": r.rating,
            "review_title": r.review_title,
            "comment": r.comment,
            "is_verified_booking": r.is_verified_booking,
            "created_at": str(r.created_at)
        }
        for r in reviews
    ]


@router.post("/submit")
def submit_review(req: ReviewCreateSchema, db: Session = Depends(get_db)):
    """Submits a traveler review."""
    rev = TripReview(
        author_name=req.author_name,
        target_type=req.target_type,
        target_name=req.target_name,
        rating=req.rating,
        review_title=req.review_title,
        comment=req.comment,
        is_verified_booking=True
    )
    db.add(rev)
    db.commit()
    db.refresh(rev)
    return {"success": True, "review_id": rev.id, "message": "Thank you! Your verified review has been published."}

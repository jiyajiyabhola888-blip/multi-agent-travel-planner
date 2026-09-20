from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.simulation import FavoriteWishlist

router = APIRouter(prefix="/wishlist", tags=["Favorites & Saved Items"])


class WishlistItemSchema(BaseModel):
    item_type: str  # destination, hotel, restaurant, attraction, guide, experience
    item_id: str
    title: str
    subtitle: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    price_info: Optional[str] = None
    rating: Optional[float] = 4.8


@router.get("/")
def get_wishlist(user_id: int = 1, db: Session = Depends(get_db)):
    """Retrieves all saved items for the user."""
    items = db.query(FavoriteWishlist).filter(FavoriteWishlist.user_id == user_id).order_by(FavoriteWishlist.id.desc()).all()
    return [
        {
            "id": it.id,
            "item_type": it.item_type,
            "item_id": it.item_id,
            "title": it.title,
            "subtitle": it.subtitle,
            "location": it.location,
            "image_url": it.image_url,
            "price_info": it.price_info,
            "rating": it.rating,
            "created_at": str(it.created_at)
        }
        for it in items
    ]


@router.post("/toggle")
def toggle_wishlist_item(req: WishlistItemSchema, user_id: int = 1, db: Session = Depends(get_db)):
    """Toggles item in wishlist (adds if not present, removes if already present)."""
    existing = db.query(FavoriteWishlist).filter(
        FavoriteWishlist.user_id == user_id,
        FavoriteWishlist.item_id == req.item_id,
        FavoriteWishlist.item_type == req.item_type
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        return {"success": True, "saved": False, "message": f"Removed '{req.title}' from Saved Wishlist."}
    else:
        new_item = FavoriteWishlist(
            user_id=user_id,
            item_type=req.item_type,
            item_id=req.item_id,
            title=req.title,
            subtitle=req.subtitle,
            location=req.location,
            image_url=req.image_url,
            price_info=req.price_info,
            rating=req.rating or 4.8
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"success": True, "saved": True, "item_id": new_item.id, "message": f"Saved '{req.title}' to Wishlist!"}

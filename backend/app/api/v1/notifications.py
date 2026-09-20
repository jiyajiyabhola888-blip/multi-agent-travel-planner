from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.simulation import NotificationItem

router = APIRouter(prefix="/notifications", tags=["Notification Center"])


@router.get("/")
def get_notifications(user_id: int = 1, db: Session = Depends(get_db)):
    """Retrieves all notifications for the traveler."""
    notifs = db.query(NotificationItem).filter(NotificationItem.user_id == user_id).order_by(NotificationItem.id.desc()).all()
    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "category": n.category,
            "severity": n.severity,
            "is_read": n.is_read,
            "action_link": n.action_link,
            "created_at": str(n.created_at)
        }
        for n in notifs
    ]


@router.post("/read-all")
def mark_all_read(user_id: int = 1, db: Session = Depends(get_db)):
    """Marks all notifications as read."""
    db.query(NotificationItem).filter(NotificationItem.user_id == user_id).update({"is_read": True})
    db.commit()
    return {"success": True, "message": "All notifications marked as read."}

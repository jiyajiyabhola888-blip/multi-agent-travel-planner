from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.booking_service import BookingService

router = APIRouter(prefix="/bookings", tags=["Trip Booking Ecosystem"])


class BookingCreateSchema(BaseModel):
    booking_type: str  # Hotel, Flight, Train, Cab, Guide, Activity, Restaurant
    title: str
    destination_name: str
    start_date: str
    amount: float
    currency: str = "INR"
    end_date: Optional[str] = None
    guests_count: int = 2
    provider_name: str = "World Travelholic Direct"
    trip_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


@router.get("/")
def list_bookings(user_id: int = 1, db: Session = Depends(get_db)):
    """Lists all active and past bookings."""
    bookings = BookingService.list_bookings(db, user_id=user_id)
    return [
        {
            "id": b.id,
            "booking_reference": b.booking_reference,
            "booking_type": b.booking_type,
            "title": b.title,
            "provider_name": b.provider_name,
            "destination_name": b.destination_name,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "guests_count": b.guests_count,
            "amount": b.amount,
            "currency": b.currency,
            "status": b.status,
            "is_sandbox_mock": b.is_sandbox_mock,
            "cancellation_policy": b.cancellation_policy,
            "details": b.details_json,
            "created_at": str(b.created_at)
        }
        for b in bookings
    ]


@router.post("/create")
def create_booking(req: BookingCreateSchema, db: Session = Depends(get_db)):
    """Creates a unified booking object in Sandbox / Demo Mode."""
    booking = BookingService.create_booking(
        db=db,
        booking_type=req.booking_type,
        title=req.title,
        destination_name=req.destination_name,
        start_date=req.start_date,
        amount=req.amount,
        currency=req.currency,
        end_date=req.end_date,
        guests_count=req.guests_count,
        provider_name=req.provider_name,
        trip_id=req.trip_id,
        details=req.details
    )

    return {
        "success": True,
        "booking_id": booking.id,
        "booking_reference": booking.booking_reference,
        "status": booking.status,
        "message": f"Successfully created {req.booking_type} reservation: {req.title}!",
        "is_sandbox_mock": True,
        "mock_disclaimer": "DEMO / TEST MODE: This reservation is simulated for prototyping purposes."
    }


@router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """Cancels a booking in sandbox mode."""
    cancelled = BookingService.cancel_booking(db, booking_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Booking not found.")

    return {
        "success": True,
        "booking_id": cancelled.id,
        "booking_reference": cancelled.booking_reference,
        "status": cancelled.status,
        "message": f"Booking {cancelled.booking_reference} has been cancelled successfully."
    }

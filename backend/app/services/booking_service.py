import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.simulation import TripBooking, PaymentTransaction


class BookingService:
    @staticmethod
    def create_booking(
        db: Session,
        booking_type: str,
        title: str,
        destination_name: str,
        start_date: str,
        amount: float,
        currency: str = "INR",
        end_date: Optional[str] = None,
        guests_count: int = 2,
        provider_name: str = "World Travelholic Direct",
        trip_id: Optional[int] = None,
        user_id: Optional[int] = 1,
        details: Optional[Dict[str, Any]] = None
    ) -> TripBooking:
        """Creates a unified booking object in Sandbox / Demo mode."""
        ref_prefix = booking_type[:3].upper() if booking_type else "TRP"
        ref_code = f"WT-{ref_prefix}-{uuid.uuid4().hex[:6].upper()}"

        booking = TripBooking(
            booking_reference=ref_code,
            trip_id=trip_id,
            user_id=user_id,
            booking_type=booking_type,
            title=title,
            provider_name=provider_name,
            destination_name=destination_name,
            start_date=start_date,
            end_date=end_date,
            guests_count=guests_count,
            amount=amount,
            currency=currency,
            status="Confirmed",
            is_sandbox_mock=True,
            details_json=details or {},
            cancellation_policy="Free cancellation up to 48 hours before scheduled start."
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    @staticmethod
    def list_bookings(db: Session, user_id: int = 1) -> List[TripBooking]:
        return db.query(TripBooking).order_by(TripBooking.id.desc()).all()

    @staticmethod
    def get_booking(db: Session, booking_id: int) -> Optional[TripBooking]:
        return db.query(TripBooking).filter(TripBooking.id == booking_id).first()

    @staticmethod
    def cancel_booking(db: Session, booking_id: int) -> Optional[TripBooking]:
        booking = db.query(TripBooking).filter(TripBooking.id == booking_id).first()
        if booking:
            booking.status = "Cancelled"
            db.commit()
            db.refresh(booking)
        return booking

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.simulation import TripBooking, PaymentTransaction


class PaymentService:
    @staticmethod
    def calculate_order_summary(base_amount: float, currency: str = "INR") -> Dict[str, Any]:
        """Calculates transparent order breakdown with taxes, processing fees, and net total."""
        tax_rate = 0.05  # 5% government tourism/GST tax
        service_fee_rate = 0.02  # 2% platform facilitation fee

        tax_amount = round(base_amount * tax_rate, 2)
        service_fee = round(base_amount * service_fee_rate, 2)
        total_amount = round(base_amount + tax_amount + service_fee, 2)

        return {
            "base_amount": base_amount,
            "tax_amount": tax_amount,
            "tax_label": "Tourism & State Tax (5%)",
            "service_fee": service_fee,
            "service_label": "Platform Facilitation Fee (2%)",
            "total_amount": total_amount,
            "currency": currency,
            "is_sandbox_mode": True,
            "sandbox_disclaimer": "TEST / SANDBOX PAYMENT MODE: No real funds or credit cards will be charged."
        }

    @staticmethod
    def process_sandbox_payment(
        db: Session,
        booking_id: int,
        payment_method: str = "Sandbox Card",
        user_id: int = 1
    ) -> Dict[str, Any]:
        """Executes simulated instant payment in Sandbox mode without storing real card data."""
        booking = db.query(TripBooking).filter(TripBooking.id == booking_id).first()
        if not booking:
            raise ValueError(f"Booking with ID {booking_id} not found.")

        order_calc = PaymentService.calculate_order_summary(booking.amount, booking.currency)
        tx_id = f"WT-TXN-{uuid.uuid4().hex[:10].upper()}"
        inv_num = f"INV-WT-{datetime.utcnow().strftime('%Y%m')}-{booking_id:04d}"

        txn = PaymentTransaction(
            transaction_id=tx_id,
            booking_id=booking.id,
            user_id=user_id,
            amount=order_calc["total_amount"],
            currency=booking.currency,
            payment_method=payment_method,
            status="Completed",
            tax_amount=order_calc["tax_amount"],
            service_fee=order_calc["service_fee"],
            gateway_name="World Travelholic Test Payment Gateway",
            invoice_number=inv_num
        )
        db.add(txn)
        booking.status = "Confirmed"
        db.commit()
        db.refresh(txn)

        return {
            "success": True,
            "transaction_id": txn.transaction_id,
            "invoice_number": txn.invoice_number,
            "booking_reference": booking.booking_reference,
            "amount_paid": txn.amount,
            "currency": txn.currency,
            "payment_method": txn.payment_method,
            "status": txn.status,
            "timestamp": str(txn.created_at),
            "is_sandbox_mock": True,
            "receipt_url": f"/receipt/{txn.transaction_id}"
        }

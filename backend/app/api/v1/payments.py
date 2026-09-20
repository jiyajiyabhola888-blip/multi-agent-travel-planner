from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payment & Sandbox Checkout"])


class CheckoutRequestSchema(BaseModel):
    booking_id: int
    payment_method: str = "Sandbox Card"  # Sandbox Card, Mock UPI, Demo NetBanking, Sandbox ApplePay


@router.get("/summary")
def get_payment_summary(amount: float = Query(..., gt=0), currency: str = Query("INR")):
    """Returns transparent breakdown of base amount, taxes, platform fee, and total."""
    return PaymentService.calculate_order_summary(base_amount=amount, currency=currency)


@router.post("/checkout")
def execute_sandbox_checkout(req: CheckoutRequestSchema, db: Session = Depends(get_db)):
    """Executes a simulated payment in Sandbox Mode and generates booking confirmation & invoice receipt."""
    try:
        result = PaymentService.process_sandbox_payment(
            db=db,
            booking_id=req.booking_id,
            payment_method=req.payment_method
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checkout error: {str(e)}")

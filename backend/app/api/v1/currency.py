from fastapi import APIRouter, Query, UploadFile, File, Form, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.currency_service import CurrencyService
from app.services.vision_service import VisionInspirationService
from app.models.user import TravelPreferenceMemory, User
from app.models.trip import Trip
from app.models.guide import LocalGuide
from app.models.experience import LocalExperience
from app.models.simulation import ServiceRequest, TripReview

router_currency = APIRouter(prefix="/currency", tags=["Multi-Currency Engine"])
router_vision = APIRouter(prefix="/vision", tags=["Inspiration & Screenshot Import"])
router_pref = APIRouter(prefix="/preferences", tags=["Preference Memory"])
router_admin = APIRouter(prefix="/admin", tags=["Admin Operations"])


# --- CURRENCY ENDPOINTS ---
@router_currency.get("/list")
def get_supported_currencies():
    return CurrencyService.get_supported_currencies()


@router_currency.get("/convert")
def convert_currency(
    amount: float = Query(..., description="Amount to convert"),
    from_curr: str = Query("INR"),
    to_curr: str = Query("USD")
):
    converted = CurrencyService.convert(amount, from_curr, to_curr)
    return {
        "original_amount": amount,
        "from_currency": from_curr.upper(),
        "to_currency": to_curr.upper(),
        "converted_amount": converted,
        "formatted_result": CurrencyService.format_currency(converted, to_curr)
    }


# --- VISION / SCREENSHOT INSPIRATION ENDPOINTS ---
@router_vision.post("/analyze")
async def analyze_inspiration(
    caption: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None)
):
    filename = file.filename if file else "travel_photo.jpg"
    result = VisionInspirationService.analyze_inspiration_image(filename=filename, caption=caption or "")
    return {
        "success": True,
        "filename": filename,
        "analysis": result
    }


# --- PREFERENCE MEMORY ENDPOINTS ---
@router_pref.get("/")
def get_preference_memory(db: Session = Depends(get_db)):
    pref = db.query(TravelPreferenceMemory).first()
    if not pref:
        pref = TravelPreferenceMemory(
            travel_style="Balanced",
            travel_pace="Balanced",
            interests=["Heritage", "Photography", "Culinary Trail"],
            food_preferences=["Vegetarian", "Street Food"],
            accommodation_pref="Boutique Hotel / 4-Star",
            transport_pref="Private Cab & Trains"
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)

    return {
        "id": pref.id,
        "travel_style": pref.travel_style,
        "travel_pace": pref.travel_pace,
        "interests": pref.interests,
        "food_preferences": pref.food_preferences,
        "accommodation_pref": pref.accommodation_pref,
        "transport_pref": pref.transport_pref,
        "special_requirements": pref.special_requirements,
        "status": "Active Preference Memory"
    }


@router_pref.post("/update")
def update_preference_memory(data: dict, db: Session = Depends(get_db)):
    pref = db.query(TravelPreferenceMemory).first()
    if not pref:
        pref = TravelPreferenceMemory()
        db.add(pref)

    pref.travel_style = data.get("travel_style", pref.travel_style)
    pref.travel_pace = data.get("travel_pace", pref.travel_pace)
    pref.interests = data.get("interests", pref.interests)
    pref.food_preferences = data.get("food_preferences", pref.food_preferences)
    pref.accommodation_pref = data.get("accommodation_pref", pref.accommodation_pref)
    pref.transport_pref = data.get("transport_pref", pref.transport_pref)
    pref.special_requirements = data.get("special_requirements", pref.special_requirements)

    db.commit()
    db.refresh(pref)
    return {"success": True, "message": "Preference memory updated successfully!", "preferences": data}


# --- ADMIN DASHBOARD ENDPOINTS ---
@router_admin.get("/metrics")
def get_admin_dashboard_metrics(db: Session = Depends(get_db)):
    total_trips = db.query(Trip).count()
    total_guides = db.query(LocalGuide).count()
    total_experiences = db.query(LocalExperience).count()
    total_requests = db.query(ServiceRequest).count()

    return {
        "platform_status": "Healthy & Operational",
        "total_trips_generated": total_trips,
        "active_ai_agents": 15,
        "verified_guides": total_guides,
        "curated_experiences": total_experiences,
        "service_requests": total_requests,
        "countries_supported": 6,
        "indian_states_and_uts_covered": 36,
        "agent_consensus_rate": "98.4%",
        "uptime": "99.98%"
    }

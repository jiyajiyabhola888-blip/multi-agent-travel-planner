from fastapi import APIRouter
from app.api.v1.trips import router as trips_router
from app.api.v1.destinations import router as destinations_router
from app.api.v1.guides import router as guides_router
from app.api.v1.experiences import router as experiences_router
from app.api.v1.simulations import router as simulations_router
from app.api.v1.recovery import router as recovery_router
from app.api.v1.currency import router_currency, router_vision, router_pref, router_admin
from app.api.v1.bookings import router as bookings_router
from app.api.v1.payments import router as payments_router
from app.api.v1.ai_chat import router as ai_chat_router
from app.api.v1.wishlist import router as wishlist_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.reviews import router as reviews_router

api_router = APIRouter()

# Health check
@api_router.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "online",
        "service": "WORLD TRAVELHOLIC 🌍 Platform API",
        "version": "2.0.0",
        "brand": "WORLD TRAVELHOLIC",
        "tagline": "Explore More. Travel Smarter.",
        "agents_available": 15,
        "usp": "Generate → Debate → Optimize → Simulate → Explain → Adapt",
        "coverage": "Global & India (All 28 States + 8 UTs)",
        "mode": "production-ready",
    }

# Include all modular routers
api_router.include_router(trips_router)
api_router.include_router(destinations_router)
api_router.include_router(guides_router)
api_router.include_router(experiences_router)
api_router.include_router(simulations_router)
api_router.include_router(recovery_router)
api_router.include_router(router_currency)
api_router.include_router(router_vision)
api_router.include_router(router_pref)
api_router.include_router(router_admin)
api_router.include_router(bookings_router)
api_router.include_router(payments_router)
api_router.include_router(ai_chat_router)
api_router.include_router(wishlist_router)
api_router.include_router(notifications_router)
api_router.include_router(reviews_router)

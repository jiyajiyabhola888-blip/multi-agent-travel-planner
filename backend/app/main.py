from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import Base, engine, SessionLocal
from app.db.init_db import init_db

# Ensure tables and seed data are populated
Base.metadata.create_all(bind=engine)
try:
    with SessionLocal() as db_session:
        init_db(db_session)
except Exception as e:
    print(f"DB init error: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="WORLD TRAVELHOLIC - Global AI-Powered Travel Ecosystem API",
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set all CORS enabled origins with regex fallback for dev network IPs and dynamic ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.CORS_ORIGINS) if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|172\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|0\.0\.0\.0)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": "Welcome to WORLD TRAVELHOLIC 🌍 Platform API",
        "tagline": "Explore More. Travel Smarter.",
        "docs": f"{settings.API_V1_STR}/docs",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

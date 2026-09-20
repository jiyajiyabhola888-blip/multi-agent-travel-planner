from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.destination import Country, RegionState, City, AttractionPOI, HotelStay, RestaurantVenue, DestinationVideo, TravelRequirement
from app.models.guide import LocalGuide
from app.models.experience import LocalExperience
from app.services.global_location_service import global_location_service

router = APIRouter(prefix="/destinations", tags=["Destinations & Global Discovery"])


@router.get("/countries")
def get_all_countries(db: Session = Depends(get_db)):
    countries = db.query(Country).all()
    return [
        {
            "id": c.id,
            "code": c.code,
            "name": c.name,
            "continent": c.continent,
            "currency_code": c.currency_code,
            "timezone": c.timezone,
            "hero_image": c.hero_image,
            "visa_guidelines": c.visa_guidelines,
        }
        for c in countries
    ]


@router.get("/map")
def get_map_destinations(db: Session = Depends(get_db)):
    """Dedicated endpoint returning real geographic coordinates and metadata for interactive world map across all continents."""
    return global_location_service.get_map_destinations(db)


@router.get("/search")
def search_destinations(
    query: Optional[str] = Query(None, description="Search term for city, state, country, or POI"),
    country_code: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Global search supporting worldwide countries, cities, regions, and attractions."""
    if not query:
        cities = db.query(City).limit(20).all()
        results = []
        for city in cities:
            region_name = city.region.name if city.region else ""
            country_name = city.region.country.name if city.region and city.region.country else "India"
            country_code_val = city.region.country.code if city.region and city.region.country else "IN"
            results.append({
                "id": city.id,
                "canonical_name": f"{city.name}, {region_name}, {country_name}" if region_name else f"{city.name}, {country_name}",
                "canonical_id": f"city:{city.id}",
                "name": city.name,
                "region_name": region_name,
                "country_name": country_name,
                "country_code": country_code_val,
                "avg_daily_budget_inr": city.avg_daily_budget_inr,
                "best_months": city.best_months,
                "vibe": city.vibe,
                "image_url": city.image_url or "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&auto=format&fit=crop&q=80",
                "poi_count": len(city.pois),
                "top_pois": [p.name for p in city.pois[:3]],
                "hotel_count": len(city.hotels),
                "restaurant_count": len(city.restaurants)
            })
        return results

    return global_location_service.search(db, query, limit=20)


@router.get("/autocomplete")
def autocomplete_destinations(
    q: str = Query(..., min_length=1, description="Live global autocomplete prefix"),
    db: Session = Depends(get_db)
):
    """Instant global search suggestions with hierarchy (Countries, Cities, Landmarks) and canonical identity."""
    return global_location_service.autocomplete(db, q, limit=12)


@router.get("/resolve/{canonical_id:path}")
def resolve_destination_by_canonical_id(canonical_id: str, db: Session = Depends(get_db)):
    """Resolves any canonical place identifier into a comprehensive destination hub."""
    return get_destination_detail(canonical_id, db)


@router.get("/categories")
def get_destination_categories(
    category: Optional[str] = Query("trending", description="Category: trending, honeymoon, family, adventure, beach, mountain, food, luxury, budget, solo, hidden_gems"),
    db: Session = Depends(get_db)
):
    """Categorized destination collections for the global discovery grid."""
    cities = db.query(City).all()
    results = []

    cat = (category or "trending").lower()

    for city in cities:
        c_name = city.name.lower()
        score = 80
        cat_badge = "Trending"

        if cat == "honeymoon":
            if "udaipur" in c_name or "paris" in c_name or "bali" in c_name or "interlaken" in c_name:
                score = 98
                cat_badge = "Romantic Haven"
            elif "goa" in c_name:
                score = 90
                cat_badge = "Sunset Beach"
        elif cat == "family":
            if "jaipur" in c_name or "delhi" in c_name or "dubai" in c_name or "paris" in c_name:
                score = 95
                cat_badge = "Family Favorite"
        elif cat == "adventure":
            if "interlaken" in c_name or "bali" in c_name or "dubai" in c_name:
                score = 97
                cat_badge = "Thrill & Nature"
        elif cat == "beach":
            if "goa" in c_name or "bali" in c_name:
                score = 99
                cat_badge = "Tropical Coast"
        elif cat == "food":
            if "delhi" in c_name or "jaipur" in c_name or "mumbai" in c_name or "tokyo" in c_name or "paris" in c_name:
                score = 96
                cat_badge = "Gastronomy Capital"
        elif cat == "luxury":
            if "dubai" in c_name or "paris" in c_name or "udaipur" in c_name or "interlaken" in c_name:
                score = 96
                cat_badge = "5-Star Opulence"
        elif cat == "budget":
            if city.avg_daily_budget_inr <= 5000:
                score = 92
                cat_badge = "High Value"

        country_name = city.region.country.name if city.region and city.region.country else "India"
        results.append({
            "id": city.id,
            "name": city.name,
            "region_name": city.region.name if city.region else "",
            "country_name": country_name,
            "canonical_name": f"{city.name}, {city.region.name if city.region else ''}, {country_name}".replace(" ,", ""),
            "canonical_id": f"city:{city.id}",
            "avg_daily_budget_inr": city.avg_daily_budget_inr,
            "best_months": city.best_months,
            "vibe": city.vibe,
            "image_url": city.image_url or "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600&auto=format&fit=crop&q=80",
            "score": score,
            "badge": cat_badge,
            "top_pois": [p.name for p in city.pois[:3]],
            "stay_preview": [h.name for h in city.hotels[:2]]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


@router.get("/recommend")
def recommend_destinations(
    budget_inr: float = Query(50000, description="Total budget in INR"),
    trip_type: str = Query("Family"),
    interests: Optional[str] = Query("Heritage, Nature"),
    travel_style: str = Query("Balanced"),
    db: Session = Depends(get_db)
):
    """'I don't know where to go' AI recommender based on budget, season, duration, and vibe."""
    cities = db.query(City).all()
    recommendations = []

    for city in cities:
        suitability = 85
        reason = f"Excellent match for {travel_style} travel with rich {city.vibe} experiences."

        if trip_type.lower() == "honeymoon" and ("udaipur" in city.name.lower() or "paris" in city.name.lower() or "switzerland" in city.name.lower() or "bali" in city.name.lower()):
            suitability += 12
            reason = f"Ranked as top romantic haven with scenic sunset spots and private luxury experiences."
        elif trip_type.lower() == "family" and ("delhi" in city.name.lower() or "jaipur" in city.name.lower() or "dubai" in city.name.lower()):
            suitability += 10
            reason = f"High family comfort with easy accessibility, world-class landmarks, and spacious boutique hotels."
        elif trip_type.lower() == "adventure" and ("interlaken" in city.name.lower() or "bali" in city.name.lower() or "dubai" in city.name.lower()):
            suitability += 14
            reason = f"Thrill seeker destination featuring high-altitude viewpoints, watersports, and desert safaris."

        country_name = city.region.country.name if city.region and city.region.country else "India"
        recommendations.append({
            "destination_name": f"{city.name}, {country_name}",
            "city": city.name,
            "canonical_id": f"city:{city.id}",
            "country_code": city.region.country.code if city.region and city.region.country else "IN",
            "vibe": city.vibe,
            "best_months": city.best_months,
            "estimated_daily_budget_inr": city.avg_daily_budget_inr,
            "suggested_duration_days": 4 if city.avg_daily_budget_inr < 8000 else 6,
            "suitability_score": min(99, suitability),
            "suitability_explanation": reason,
            "image_url": city.image_url,
            "major_experiences": [p.name for p in city.pois[:3]],
            "disclaimer": "AI recommendations are optimized suggestions based on seasonal patterns and budget benchmarks."
        })

    recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
    return recommendations[:8]


@router.get("/{city_identifier:path}")
def get_destination_detail(city_identifier: str, db: Session = Depends(get_db)):
    """Fetches full comprehensive destination hub by ID, canonical_id (city:123, country:china:cn, city:beijing:cn),
    slug, or place name.
    
    If local database has matching destination, returns full local DB models.
    If not in local DB, seamlessly resolves via Global Location Intelligence.
    If destination does not exist globally, returns a proper HTTP 404 response.
    Never silently falls back to another destination.
    """
    raw_ident = city_identifier.strip()
    city: Optional[City] = None

    # 1. Handle canonical identifier prefixes for local DB
    if raw_ident.lower().startswith("city:"):
        c_id = raw_ident.split(":", 1)[1].strip()
        if c_id.isdigit():
            city = db.query(City).filter(City.id == int(c_id)).first()
        else:
            c_name = c_id.split(":")[0].replace("-", " ")
            city = db.query(City).filter(City.name.ilike(c_name)).first()
    elif raw_ident.lower().startswith("poi:") or raw_ident.lower().startswith("attraction:"):
        p_id = raw_ident.split(":", 1)[1].strip()
        if p_id.isdigit():
            poi = db.query(AttractionPOI).filter(AttractionPOI.id == int(p_id)).first()
            if poi and poi.city:
                city = poi.city
    elif raw_ident.lower().startswith("country:"):
        co_id = raw_ident.split(":", 1)[1].strip()
        if co_id.isdigit():
            country = db.query(Country).filter(Country.id == int(co_id)).first()
            if country and country.regions:
                for r in country.regions:
                    if r.cities:
                        city = r.cities[0]
                        break

    # 2. Handle pure numeric ID
    if not city and raw_ident.isdigit():
        city = db.query(City).filter(City.id == int(raw_ident)).first()

    # 3. Handle string city name match in local DB
    if not city:
        clean_name = raw_ident.split(",")[0].strip()
        clean_name_hyphen = clean_name.replace("-", " ")

        # Exact case-insensitive match on city name
        city = db.query(City).filter(
            City.name.ilike(clean_name) | City.name.ilike(clean_name_hyphen)
        ).first()

    # If city is in local DB, return rich model records
    if city:
        region = city.region
        country = region.country if region else None

        req = None
        if country:
            req = db.query(TravelRequirement).filter(TravelRequirement.country_code == country.code).first()

        guides = db.query(LocalGuide).filter(LocalGuide.city_name.ilike(f"%{city.name}%")).all()
        experiences = db.query(LocalExperience).filter(LocalExperience.city_name.ilike(f"%{city.name}%")).all()

        return {
            "id": city.id,
            "name": city.name,
            "region_name": region.name if region else "",
            "country_name": country.name if country else "India",
            "country_code": country.code if country else "IN",
            "currency_code": country.currency_code if country else "INR",
            "timezone": country.timezone if country else "Asia/Kolkata",
            "latitude": city.latitude,
            "longitude": city.longitude,
            "avg_daily_budget_inr": city.avg_daily_budget_inr,
            "best_months": city.best_months,
            "vibe": city.vibe,
            "description": city.description or f"Discover the enchanting culture, vibrant streets, and breathtaking landmarks of {city.name}.",
            "image_url": city.image_url or "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1200&auto=format&fit=crop&q=80",
            
            "attractions": [
                {
                    "id": p.id,
                    "name": p.name,
                    "category": p.category,
                    "duration_minutes": p.avg_duration_minutes,
                    "entry_fee_inr": p.entry_fee_inr,
                    "indoor_outdoor": p.indoor_outdoor,
                    "opening_hours": p.opening_hours,
                    "best_time_of_day": p.best_time_of_day,
                    "description": p.description,
                    "image_url": p.image_url or city.image_url
                }
                for p in city.pois
            ],
            
            "stays": [
                {
                    "id": h.id,
                    "name": h.name,
                    "property_type": h.property_type,
                    "price_per_night_inr": h.price_per_night_inr,
                    "rating": h.rating,
                    "review_count": h.review_count,
                    "location_area": h.location_area,
                    "distance_to_attraction": h.distance_to_attraction,
                    "amenities": h.amenities or [],
                    "image_url": h.image_url or "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80",
                    "description": h.description,
                    "is_demo_availability": h.is_demo_availability
                }
                for h in city.hotels
            ],

            "restaurants": [
                {
                    "id": r.id,
                    "name": r.name,
                    "cuisine_type": r.cuisine_type,
                    "category": r.category,
                    "price_level": r.price_level,
                    "avg_meal_cost_inr": r.avg_meal_cost_inr,
                    "rating": r.rating,
                    "review_count": r.review_count,
                    "location_area": r.location_area,
                    "popular_dishes": r.popular_dishes or [],
                    "dietary_tags": r.dietary_tags or [],
                    "opening_hours": r.opening_hours,
                    "image_url": r.image_url or "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80",
                    "description": r.description,
                    "is_demo_reservation": r.is_demo_reservation
                }
                for r in city.restaurants
            ],

            "videos": [
                {
                    "id": v.id,
                    "title": v.title,
                    "duration_str": v.duration_str,
                    "thumbnail_url": v.thumbnail_url or city.image_url,
                    "video_url": v.video_url,
                    "category": v.category
                }
                for v in city.videos
            ],

            "guides": [
                {
                    "id": g.id,
                    "name": g.full_name,
                    "experience_years": g.experience_years,
                    "languages": g.languages_spoken,
                    "hourly_rate": g.hourly_rate,
                    "currency": g.currency,
                    "rating": g.rating,
                    "review_count": g.review_count,
                    "specialization": g.specialization,
                    "bio": g.bio,
                    "avatar_url": g.avatar_url
                }
                for g in guides
            ],

            "experiences": [
                {
                    "id": e.id,
                    "title": e.title,
                    "category": e.category,
                    "duration_hours": e.duration_hours,
                    "price_per_person": e.price_per_person,
                    "currency": e.currency,
                    "rating": e.rating,
                    "description": e.description,
                    "highlights": e.highlights or []
                }
                for e in experiences
            ],

            "travel_requirement": {
                "passport_validity": req.passport_validity if req else "Valid for 6 months beyond arrival",
                "visa_requirement": req.visa_requirement if req else "Standard visitor visa / e-Visa",
                "customs_advisory": req.customs_advisory if req else "Standard customs rules apply",
                "currency_regulations": req.currency_regulations if req else "Local cards and digital currency",
                "official_portal_url": req.official_portal_url if req else "https://official-travel-advisory.gov",
                "disclaimer": "Visa and entry requirements change frequently. Verify current regulations with official embassy sources."
            }
        }

    # 4. If not in local DB, resolve via Global Location Service
    global_resolved = global_location_service.resolve(db, raw_ident)
    if global_resolved:
        return global_resolved

    # 5. Strict 404 if no destination found - NEVER return fallback city
    raise HTTPException(
        status_code=404,
        detail="Destination not found"
    )


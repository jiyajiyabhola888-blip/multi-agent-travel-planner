import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.destination import Country, RegionState, City, AttractionPOI, HotelStay, RestaurantVenue, DestinationVideo, TravelRequirement
from app.models.guide import LocalGuide
from app.models.experience import LocalExperience
from app.models.simulation import TripBooking, TripReview, FavoriteWishlist, NotificationItem
from app.db.seed_data import COUNTRIES_DATA, LOCAL_GUIDES_DATA, LOCAL_EXPERIENCES_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session = None) -> None:
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Check if already seeded
        existing_country = db.query(Country).first()
        if existing_country:
            logger.info("Database already initialized with destinations.")
            return

        logger.info("Seeding WORLD TRAVELHOLIC global destination ecosystem...")
        # Seed Countries, Regions, Cities, POIs, Hotels, Restaurants, Videos, Requirements
        for c_data in COUNTRIES_DATA:
            country = Country(
                code=c_data["code"],
                name=c_data["name"],
                continent=c_data.get("continent", "Asia"),
                currency_code=c_data.get("currency_code", "INR"),
                timezone=c_data.get("timezone", "Asia/Kolkata"),
                visa_guidelines=c_data.get("visa_guidelines"),
                hero_image=c_data.get("hero_image"),
            )
            db.add(country)
            db.flush()

            if "requirement" in c_data:
                req_data = c_data["requirement"]
                req = TravelRequirement(
                    country_code=country.code,
                    passport_validity=req_data.get("passport_validity", "6 months beyond arrival"),
                    visa_requirement=req_data.get("visa_requirement", "Standard tourist visa"),
                    customs_advisory=req_data.get("customs_advisory", "Standard customs limits apply"),
                    currency_regulations=req_data.get("currency_regulations", "Local digital currency & cards"),
                    official_portal_url=req_data.get("official_portal_url")
                )
                db.add(req)

            for r_data in c_data.get("regions", []):
                region = RegionState(
                    country_id=country.id,
                    name=r_data["name"],
                    is_union_territory=r_data.get("is_ut", False),
                )
                db.add(region)
                db.flush()

                for city_data in r_data.get("cities", []):
                    city = City(
                        region_id=region.id,
                        name=city_data["name"],
                        latitude=city_data["lat"],
                        longitude=city_data["lon"],
                        avg_daily_budget_inr=city_data.get("budget", 4000),
                        best_months=city_data.get("best", "Oct-Mar"),
                        vibe=city_data.get("vibe", "Culture & Sightseeing"),
                        description=city_data.get("description"),
                        image_url=city_data.get("image_url"),
                    )
                    db.add(city)
                    db.flush()

                    for poi_data in city_data.get("pois", []):
                        poi = AttractionPOI(
                            city_id=city.id,
                            name=poi_data["name"],
                            category=poi_data.get("cat", "Sightseeing"),
                            avg_duration_minutes=poi_data.get("duration", 90),
                            entry_fee_inr=poi_data.get("fee", 0.0),
                            indoor_outdoor=poi_data.get("in_out", "Outdoor"),
                            description=poi_data.get("desc"),
                            image_url=poi_data.get("image_url"),
                        )
                        db.add(poi)

                    for hotel_data in city_data.get("hotels", []):
                        hotel = HotelStay(
                            city_id=city.id,
                            name=hotel_data["name"],
                            property_type=hotel_data.get("property_type", "Hotel"),
                            price_per_night_inr=hotel_data.get("price_per_night_inr", 4000),
                            rating=hotel_data.get("rating", 4.8),
                            review_count=hotel_data.get("review_count", 80),
                            location_area=hotel_data.get("location_area", "City Center"),
                            distance_to_attraction=hotel_data.get("distance_to_attraction", "1.5 km"),
                            amenities=hotel_data.get("amenities", []),
                            image_url=hotel_data.get("image_url"),
                            description=hotel_data.get("description"),
                            is_demo_availability=True
                        )
                        db.add(hotel)

                    for rest_data in city_data.get("restaurants", []):
                        restaurant = RestaurantVenue(
                            city_id=city.id,
                            name=rest_data["name"],
                            cuisine_type=rest_data.get("cuisine_type", "Local"),
                            category=rest_data.get("category", "Top Restaurant"),
                            price_level=rest_data.get("price_level", "$$"),
                            avg_meal_cost_inr=rest_data.get("avg_meal_cost_inr", 600),
                            rating=rest_data.get("rating", 4.8),
                            review_count=rest_data.get("review_count", 150),
                            location_area=rest_data.get("location_area", "Heritage Quarter"),
                            popular_dishes=rest_data.get("popular_dishes", []),
                            dietary_tags=rest_data.get("dietary_tags", []),
                            image_url=rest_data.get("image_url"),
                            description=rest_data.get("description"),
                            is_demo_reservation=True
                        )
                        db.add(restaurant)

                    for vid_data in city_data.get("videos", []):
                        video = DestinationVideo(
                            city_id=city.id,
                            title=vid_data["title"],
                            duration_str=vid_data.get("duration_str", "5:00"),
                            thumbnail_url=vid_data.get("thumbnail_url"),
                            video_url=vid_data.get("video_url"),
                            category=vid_data.get("category", "Destination Guide")
                        )
                        db.add(video)

        logger.info("Seeding local guides...")
        for g_data in LOCAL_GUIDES_DATA:
            guide = LocalGuide(
                full_name=g_data["full_name"],
                city_name=g_data["city_name"],
                country_name=g_data["country_name"],
                experience_years=g_data.get("experience_years", 5),
                languages_spoken=g_data.get("languages_spoken", ["English"]),
                hourly_rate=g_data.get("hourly_rate", 800),
                services_offered=g_data.get("services_offered", []),
                rating=g_data.get("rating", 4.9),
                review_count=g_data.get("review_count", 25),
                specialization=g_data.get("specialization", "Heritage"),
                bio=g_data.get("bio", ""),
                avatar_url=g_data.get("avatar_url")
            )
            db.add(guide)

        logger.info("Seeding local experiences...")
        for exp_data in LOCAL_EXPERIENCES_DATA:
            experience = LocalExperience(
                title=exp_data["title"],
                category=exp_data.get("category", "Culture"),
                city_name=exp_data["city_name"],
                duration_hours=exp_data.get("duration_hours", 3.0),
                price_per_person=exp_data.get("price_per_person", 1200),
                currency=exp_data.get("currency", "INR"),
                max_group_size=exp_data.get("max_group_size", 8),
                meeting_point=exp_data.get("meeting_point", "City Center"),
                rating=exp_data.get("rating", 4.9),
                review_count=exp_data.get("review_count", 30),
                description=exp_data.get("description", ""),
                highlights=exp_data.get("highlights", []),
            )
            db.add(experience)

        # Seed initial Demo Reviews
        sample_reviews = [
            TripReview(
                author_name="Dr. Vikram & Priya Malhotra",
                target_type="destination",
                target_name="Jaipur",
                rating=5.0,
                review_title="Unbelievable 15-Agent Coordination",
                comment="The 15-agent debate engine was mind-blowing! When the Risk Agent flagged our tight commute and moved our Amber Fort climb to 08:30 AM, it saved us from the afternoon heat. Everything was realistically timed!",
                is_verified_booking=True
            ),
            TripReview(
                author_name="Sarah Jenkins & Friends",
                target_type="destination",
                target_name="Paris",
                rating=5.0,
                review_title="Group Conflict Resolver Saved Our Trip",
                comment="Two of us wanted art galleries while two wanted vintage bakery trails. The AI balanced both seamlessly without exhausting anyone!",
                is_verified_booking=True
            ),
            TripReview(
                author_name="Amitabh Sen",
                target_type="destination",
                target_name="Tokyo",
                rating=5.0,
                review_title="Live Trip Recovery is a Game Changer",
                comment="When my train was delayed by rain, the Live Trip Recovery mode rearranged our entire evening in under 3 seconds.",
                is_verified_booking=True
            )
        ]
        for rev in sample_reviews:
            db.add(rev)

        # Seed initial Notifications
        sample_notifications = [
            NotificationItem(
                user_id=1,
                title="Trip Weather Advisory",
                message="Ideal mild conditions forecast for your upcoming trip to Jaipur. Low chance of rain.",
                category="Weather",
                severity="info",
                action_link="/trips"
            ),
            NotificationItem(
                user_id=1,
                title="WanderAI Ready to Assist",
                message="WanderAI is connected to help you discover hidden stays, top restaurants, and custom itineraries.",
                category="System",
                severity="success",
                action_link="/chat"
            )
        ]
        for notif in sample_notifications:
            db.add(notif)

        # Seed sample demo booking
        sample_booking = TripBooking(
            booking_reference="WT-DEMO-7821",
            user_id=1,
            booking_type="Hotel",
            title="Samode Haveli Boutique Palace (2 Nights)",
            provider_name="Samode Hospitality / World Travelholic Sandbox",
            destination_name="Jaipur, Rajasthan, India",
            start_date="2026-10-15",
            end_date="2026-10-17",
            guests_count=2,
            amount=19000,
            currency="INR",
            status="Confirmed",
            is_sandbox_mock=True,
            details_json={
                "room_type": "Heritage Deluxe Suite",
                "breakfast": "Included",
                "check_in": "14:00",
                "check_out": "11:00",
                "confirmation_code": "SMD-HA-98124"
            }
        )
        db.add(sample_booking)

        db.commit()
        logger.info("WORLD TRAVELHOLIC Database successfully seeded!")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    init_db()

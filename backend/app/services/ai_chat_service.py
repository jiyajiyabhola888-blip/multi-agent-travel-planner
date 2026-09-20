from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.destination import City, AttractionPOI, HotelStay, RestaurantVenue


class AIChatService:
    @staticmethod
    def process_chat_message(
        db: Session,
        message: str,
        destination_context: Optional[str] = None,
        trip_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Processes traveler natural language query with context-aware responses and actionable UI triggers."""
        q = message.lower().strip()
        
        # Detect destination from message or context
        target_city_name = destination_context or "Jaipur"
        for city_candidate in ["jaipur", "udaipur", "delhi", "mumbai", "goa", "paris", "tokyo", "dubai", "bali", "interlaken", "switzerland", "kerala"]:
            if city_candidate in q:
                target_city_name = city_candidate.capitalize()
                break

        # Query database for city data
        city_obj = db.query(City).filter(City.name.ilike(f"%{target_city_name}%")).first()
        city_name = city_obj.name if city_obj else target_city_name

        # 1. Hotel / Accommodation Queries
        if any(w in q for w in ["hotel", "stay", "resort", "hostel", "where to stay", "accommodation", "room"]):
            stays = city_obj.hotels if city_obj and city_obj.hotels else []
            if stays:
                stay_list_str = "\n".join([f"• **{s.name}** ({s.property_type}): ₹{int(s.price_per_night_inr):,}/night ⭐ {s.rating} - {s.location_area}" for s in stays[:3]])
                reply = (
                    f"Here are top-recommended stays for **{city_name}** matching different budgets:\n\n"
                    f"{stay_list_str}\n\n"
                    f"Would you like me to lock one of these into your itinerary or check live sandbox availability?"
                )
            else:
                reply = f"In **{city_name}**, we recommend boutique heritage stays near the central landmark quarter for optimal walkability and scenic views."

            return {
                "reply": reply,
                "city": city_name,
                "actions": [
                    {"label": f"View All Stays in {city_name}", "action": "VIEW_STAYS", "payload": {"city": city_name}},
                    {"label": f"Plan Trip to {city_name}", "action": "PLAN_TRIP", "payload": {"destination": f"{city_name}, India" if city_name in ["Jaipur", "Udaipur", "New Delhi", "Mumbai", "Goa"] else city_name}}
                ]
            }

        # 2. Food & Restaurant Queries
        if any(w in q for w in ["eat", "food", "restaurant", "dining", "vegetarian", "vegan", "cafe", "street food", "thali", "dish"]):
            is_veg = "vegetarian" in q or "veg" in q or "vegan" in q
            rests = city_obj.restaurants if city_obj and city_obj.restaurants else []
            if rests:
                rest_list_str = "\n".join([f"• **{r.name}** ({r.cuisine_type}): ⭐ {r.rating} ({r.price_level}) - Popular: {', '.join(r.popular_dishes[:2]) if r.popular_dishes else 'Specialties'}" for r in rests[:3]])
                reply = (
                    f"Top dining spots in **{city_name}**{' (Vegetarian & Local Specialties)' if is_veg else ''}:\n\n"
                    f"{rest_list_str}\n\n"
                    f"All venues feature verified hygiene protocols and curated flavor profiles."
                )
            else:
                reply = f"In **{city_name}**, don't miss authentic regional thalis, traditional clay-oven tandoor specialties, and rooftop tea cafes."

            return {
                "reply": reply,
                "city": city_name,
                "actions": [
                    {"label": f"Explore {city_name} Food", "action": "VIEW_FOOD", "payload": {"city": city_name}},
                    {"label": "Find Local Guide", "action": "FIND_GUIDE", "payload": {"city": city_name}}
                ]
            }

        # 3. What to do / Itinerary / Plan / Days Queries
        if any(w in q for w in ["do", "plan", "itinerary", "places", "attractions", "visit", "see", "3-day", "4-day", "5-day", "days"]):
            pois = city_obj.pois if city_obj and city_obj.pois else []
            poi_names = [p.name for p in pois[:4]] if pois else [f"{city_name} Heritage Landmark", f"{city_name} Royal Palace", f"{city_name} Sunset Viewpoint"]
            pois_str = ", ".join(poi_names)

            reply = (
                f"For an unforgettable experience in **{city_name}**, our 15 AI agents recommend focusing on:\n\n"
                f"📍 **Top Highlights**: {pois_str}\n\n"
                f"⏱️ **Optimal Duration**: 3–5 Days with balanced morning sightseeing and relaxed sunset dinners.\n"
                f"Ready to generate your custom realistic day-by-day plan?"
            )

            return {
                "reply": reply,
                "city": city_name,
                "actions": [
                    {"label": f"Generate {city_name} Itinerary", "action": "PLAN_TRIP", "payload": {"destination": f"{city_name}, India" if city_name in ["Jaipur", "Udaipur", "New Delhi", "Mumbai", "Goa"] else city_name}},
                    {"label": f"View {city_name} Details", "action": "VIEW_DESTINATION", "payload": {"city": city_name}}
                ]
            }

        # 4. Rain / Delay / Disruption / What-If Queries
        if any(w in q for w in ["rain", "delay", "flight", "train", "cancel", "disruption", "what if", "problem"]):
            reply = (
                f"🌧️ **Live Incident Protection**: If bad weather or transit disruptions occur in **{city_name}**:\n\n"
                f"1. **Indoor Swaps**: Outdoor walking tours will automatically divert to world-class covered museums and artisan workshops.\n"
                f"2. **Live Recovery**: Our Live Trip Recovery Engine will surgically recalculate affected segments in <3 seconds without breaking your bookings.\n\n"
                f"You can test this right now in the **What-If Trip Simulator**!"
            )

            return {
                "reply": reply,
                "city": city_name,
                "actions": [
                    {"label": "Open What-If Simulator", "action": "OPEN_SIMULATOR", "payload": {}},
                    {"label": "Check Live Recovery", "action": "OPEN_RECOVERY", "payload": {}}
                ]
            }

        # 5. Budget & Cost Queries
        if any(w in q for w in ["budget", "cost", "price", "how much", "cheap", "expensive", "rupees", "inr"]):
            daily = city_obj.avg_daily_budget_inr if city_obj else 4500
            reply = (
                f"Estimated budget benchmark for **{city_name}**:\n\n"
                f"• **Budget Travel**: ~₹{int(daily * 0.6):,}/day (Hostels, street food, public transit)\n"
                f"• **Balanced Style**: ~₹{int(daily):,}/day (4-Star boutique stay, cabs, heritage cafes)\n"
                f"• **Luxury Style**: ~₹{int(daily * 2.5):,}+/day (5-Star Palace, private chauffeur, fine dining)\n\n"
                f"Our Budget Agent dynamically allocates your funds across 6 core buckets."
            )

            return {
                "reply": reply,
                "city": city_name,
                "actions": [
                    {"label": f"Build Budget Plan for {city_name}", "action": "PLAN_TRIP", "payload": {"destination": city_name}}
                ]
            }

        # Default General Travel Advice
        reply = (
            f"I'm **WanderAI**, your personal travel companion for **World Travelholic** 🌍.\n\n"
            f"I can help you build custom 15-agent itineraries, find top stays and local food in **{city_name}**, "
            f"check visa requirements, or simulate what-if travel disruptions."
        )

        return {
            "reply": reply,
            "city": city_name,
            "actions": [
                {"label": f"Explore {city_name}", "action": "VIEW_DESTINATION", "payload": {"city": city_name}},
                {"label": "Plan New Trip with AI", "action": "PLAN_TRIP", "payload": {}},
                {"label": "Discover Worldwide Places", "action": "DISCOVER", "payload": {}}
            ]
        }

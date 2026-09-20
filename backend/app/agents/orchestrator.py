import datetime
from typing import Dict, Any, List
from app.agents.base import AgentOutput
from app.agents.preference_agent import PreferenceAgent
from app.agents.destination_agent import DestinationAgent
from app.agents.route_agent import RouteAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.stay_agent import StayAgent, FoodAgent, WeatherAgent, ExperienceAgent
from app.agents.risk_agent import RiskAgent
from app.agents.judge_agent import GroupConflictAgent, BookingAgent, SimulationAgent, RecoveryAgent, ExplainabilityAgent, JudgeAgent
from app.services.currency_service import CurrencyService
from app.services.routing_service import RoutingService
from app.services.weather_service import WeatherService


class MultiAgentOrchestrator:
    def __init__(self):
        self.preference_agent = PreferenceAgent()
        self.destination_agent = DestinationAgent()
        self.route_agent = RouteAgent()
        self.budget_agent = BudgetAgent()
        self.stay_agent = StayAgent()
        self.food_agent = FoodAgent()
        self.weather_agent = WeatherAgent()
        self.experience_agent = ExperienceAgent()
        self.risk_agent = RiskAgent()
        self.group_conflict_agent = GroupConflictAgent()
        self.booking_agent = BookingAgent()
        self.simulation_agent = SimulationAgent()
        self.recovery_agent = RecoveryAgent()
        self.explainability_agent = ExplainabilityAgent()
        self.judge_agent = JudgeAgent()

    def run_debate(self, context: Dict[str, Any]) -> List[AgentOutput]:
        """Runs the multi-agent proposal, critique, and judge arbitration debate rounds."""
        debate_messages: List[AgentOutput] = []

        # Round 1: Core Proposals
        debate_messages.append(self.preference_agent.evaluate(context))
        debate_messages.append(self.destination_agent.evaluate(context))
        debate_messages.append(self.budget_agent.evaluate(context))
        debate_messages.append(self.stay_agent.evaluate(context))
        debate_messages.append(self.food_agent.evaluate(context))
        debate_messages.append(self.weather_agent.evaluate(context))
        debate_messages.append(self.experience_agent.evaluate(context))

        # Round 2: Scrutiny & Critique
        debate_messages.append(self.route_agent.evaluate(context))
        debate_messages.append(self.risk_agent.evaluate(context))
        debate_messages.append(self.group_conflict_agent.evaluate(context))
        debate_messages.append(self.booking_agent.evaluate(context))
        debate_messages.append(self.simulation_agent.evaluate(context))
        debate_messages.append(self.recovery_agent.evaluate(context))

        # Round 3: Synthesis & Rationale
        debate_messages.append(self.explainability_agent.evaluate(context))

        # Round 4: Final Golden Verdict from Judge Agent
        debate_messages.append(self.judge_agent.evaluate(context))

        return debate_messages

    def generate_smart_itinerary(self, context: Dict[str, Any], available_pois: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Synthesizes a realistic, day-by-day door-to-door itinerary with non-repeating activities, meal stops, buffer times, and transit."""
        num_days = int(context.get("num_days", 5))
        raw_dest = context.get("destination", "New Delhi, India")
        # Ensure canonical single city name
        dest_city = raw_dest.split(",")[0].strip()
        start_date_str = context.get("start_date", str(datetime.date.today()))
        pace = context.get("travel_pace", "Balanced")
        total_budget = float(context.get("total_budget", 50000))
        currency = context.get("currency", "INR")
        trip_type = context.get("trip_type", "Family")

        daily_budget = round(total_budget / max(1, num_days), 2)
        weather_data = WeatherService.get_forecast(dest_city, start_date_str, num_days)

        # Build diverse catalog of activities for this specific city
        pois = list(available_pois) if available_pois and len(available_pois) >= 1 else []
        
        # If POIs from database are fewer than needed, dynamically supplement with city-specific realistic activities
        supplemental_pool = [
            {"name": f"{dest_city} Historic Old Town & Landmark Heritage Walk", "cat": "Heritage", "duration": 120, "fee": 50, "in_out": "Outdoor", "desc": f"Walk through the historic heritage corridors of {dest_city}."},
            {"name": f"{dest_city} Royal Palace & Museum of Fine Arts", "cat": "Heritage", "duration": 150, "fee": 150, "in_out": "Mixed", "desc": f"Grand architectural marvel showcasing royal collections of {dest_city}."},
            {"name": f"{dest_city} Artisans Market & Local Craft Bazaar", "cat": "Culinary", "duration": 120, "fee": 0, "in_out": "Mixed", "desc": f"Authentic handloom, spices, and souvenirs in {dest_city}."},
            {"name": f"{dest_city} Panoramic Hilltop Viewpoint & Sunset Fortress", "cat": "Sightseeing", "duration": 120, "fee": 80, "in_out": "Outdoor", "desc": f"Spectacular twilight vantage point overlooking {dest_city}."},
            {"name": f"{dest_city} Botanical Gardens & Lake Promenade", "cat": "Nature", "duration": 90, "fee": 30, "in_out": "Outdoor", "desc": f"Lush peaceful gardens and serene waterfront in {dest_city}."},
            {"name": f"{dest_city} Modern Arts Quarter & Independent Boutiques", "cat": "Culture", "duration": 100, "fee": 50, "in_out": "Indoor", "desc": f"Contemporary cultural district with galleries and artisan cafes."},
            {"name": f"{dest_city} Ancient Temple & Sacred Riverside Sanctuary", "cat": "Spiritual", "duration": 90, "fee": 0, "in_out": "Outdoor", "desc": f"Peaceful spiritual landmark in {dest_city}."},
            {"name": f"{dest_city} Scenic Nature Trail & Forest Overlook", "cat": "Adventure", "duration": 180, "fee": 100, "in_out": "Outdoor", "desc": f"Picturesque hiking trail on the outskirts of {dest_city}."}
        ]

        # Combine database POIs with non-repeating supplemental POIs
        combined_pool = []
        for p in pois:
            combined_pool.append(p)
        for sp in supplemental_pool:
            if not any(sp["name"].lower() == cp["name"].lower() for cp in combined_pool):
                combined_pool.append(sp)

        # Dynamic non-repeating daily themes
        theme_templates = [
            f"Arrival, Settling in & Twilight Orientation in {dest_city}",
            f"Grand Heritage Wonders & Royal Architecture of {dest_city}",
            f"Authentic Neighborhoods, Hidden Alleyways & Artisan Bazaars",
            f"Scenic Nature Escapes, Lakes & Panoramic Vistas",
            f"Cultural Immersion, Local Craft Workshops & Gastronomy Trail",
            f"Off-The-Beaten-Path Treasures & Local Life in {dest_city}",
            f"Scenic Day Excursion & Panoramic Sunset Lookout",
            f"Artisan Souvenir Hunting, Vintage Cafes & Farewell Gala Dinner"
        ]

        days = []
        poi_index = 0

        for d in range(num_days):
            day_num = d + 1
            theme_idx = min(d, len(theme_templates) - 1)
            day_theme = f"Day {day_num}: {theme_templates[theme_idx]}"

            day_weather = weather_data["daily_forecasts"][min(d, len(weather_data["daily_forecasts"]) - 1)]

            # Get 2 unique POIs for morning and afternoon
            p1 = combined_pool[poi_index % len(combined_pool)]
            poi_index += 1
            p2 = combined_pool[poi_index % len(combined_pool)]
            poi_index += 1

            transit1 = RoutingService.get_realistic_transit(3.8, pace, "cab")
            transit2 = RoutingService.get_realistic_transit(2.4, pace, "walking")

            activities = [
                {
                    "id": f"act_{day_num}_1",
                    "order_index": 1,
                    "time_slot": "Morning",
                    "start_time": "09:00",
                    "end_time": "11:30",
                    "activity_name": p1["name"],
                    "category": p1.get("cat", "Heritage"),
                    "location_name": p1.get("name", dest_city),
                    "estimated_cost": CurrencyService.convert(p1.get("fee", 100) * 1.5, "INR", currency),
                    "transit_time_from_prev_mins": transit1["raw_travel_time_mins"],
                    "transit_mode": transit1["recommended_mode"],
                    "buffer_security_mins": transit1["security_queue_buffer_mins"] + transit1["pace_rest_buffer_mins"],
                    "booking_required": False,
                    "why_explanation": f"Morning visit scheduled to enjoy optimal ambient lighting and avoid midday crowd congestion.",
                    "is_indoor": p1.get("in_out") == "Indoor"
                },
                {
                    "id": f"act_{day_num}_2",
                    "order_index": 2,
                    "time_slot": "Lunch & Rest",
                    "start_time": "12:00",
                    "end_time": "13:45",
                    "activity_name": f"Authentic Regional Lunch & Cafe Relaxation",
                    "category": "Culinary",
                    "location_name": f"Top-Rated Local Bistro near {p1['name'][:25]}",
                    "estimated_cost": CurrencyService.convert(650, "INR", currency),
                    "transit_time_from_prev_mins": 10,
                    "transit_mode": "Short Walk (250m)",
                    "buffer_security_mins": 15,
                    "booking_required": False,
                    "why_explanation": "Mandatory 75-minute leisurely dining break respecting dietary preferences and avoiding afternoon heat.",
                    "is_indoor": True
                },
                {
                    "id": f"act_{day_num}_3",
                    "order_index": 3,
                    "time_slot": "Afternoon",
                    "start_time": "14:15",
                    "end_time": "16:45",
                    "activity_name": p2["name"],
                    "category": p2.get("cat", "Sightseeing"),
                    "location_name": p2.get("name", dest_city),
                    "estimated_cost": CurrencyService.convert(p2.get("fee", 150), "INR", currency),
                    "transit_time_from_prev_mins": transit2["raw_travel_time_mins"],
                    "transit_mode": transit2["recommended_mode"],
                    "buffer_security_mins": transit2["security_queue_buffer_mins"],
                    "booking_required": True,
                    "why_explanation": f"Geographically clustered near afternoon route; ideal match for {trip_type} travel style.",
                    "is_indoor": p2.get("in_out") == "Indoor"
                },
                {
                    "id": f"act_{day_num}_4",
                    "order_index": 4,
                    "time_slot": "Evening & Dinner",
                    "start_time": "17:30",
                    "end_time": "21:00",
                    "activity_name": f"{dest_city} Sunset Promenade & Signature Dinner",
                    "category": "Romantic" if trip_type == "Honeymoon" else "Experience",
                    "location_name": f"Scenic Waterfront & Rooftop Quarter, {dest_city}",
                    "estimated_cost": CurrencyService.convert(1250, "INR", currency),
                    "transit_time_from_prev_mins": 20,
                    "transit_mode": "Private Cab",
                    "buffer_security_mins": 20,
                    "booking_required": False,
                    "why_explanation": f"Captures golden hour atmosphere across {dest_city} paired with curated dinner dining.",
                    "is_indoor": False
                }
            ]

            day_cost = sum(a["estimated_cost"] for a in activities)

            try:
                start_d = datetime.date.fromisoformat(start_date_str)
            except Exception:
                start_d = datetime.date.today()

            days.append({
                "day_number": day_num,
                "date": str(start_d + datetime.timedelta(days=d)),
                "theme": day_theme,
                "city_name": raw_dest,
                "weather_summary": f"{day_weather['condition']}, {day_weather['temperature_celsius']}°C",
                "daily_budget_allocated": daily_budget,
                "daily_cost_estimated": round(day_cost, 2),
                "activities": activities
            })

        return days

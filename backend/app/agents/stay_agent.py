from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput


class StayAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Stay Agent", role="Hospitality & Neighborhood Strategist")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        pref = context.get("accommodation_preference", "Boutique Hotel / 4-Star")
        trip_type = context.get("trip_type", "Family")

        message = (
            f"Selected central, safe accommodations matching '{pref}' preference. "
            f"Ensured high connectivity to metro/cab lines to minimize morning commute."
        )
        if trip_type.lower() == "honeymoon":
            message += " Prioritized scenic balconies, private suites, and couples spa availability."

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Recommend single hotel base for entire stay to avoid re-packing fatigue."]
        )


class FoodAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Food Agent", role="Culinary & Dietary Specialist")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        food_prefs = context.get("food_preferences", ["Local Delicacies"])
        prefs_str = ", ".join(food_prefs) if food_prefs else "Authentic Local Cuisine"

        message = (
            f"Mapped curated breakfast, lunch, and dinner stops honoring '{prefs_str}'. "
            f"Integrated famous heritage eateries alongside hygiene-certified street food lanes."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Allocated mandatory 75-minute lunch breaks for leisurely dining and digestion."]
        )


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Weather Agent", role="Seasonality & Climate Risk Analyst")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        dest = context.get("destination", "")

        message = (
            f"Evaluated climate conditions for {dest}. "
            "Assigned outdoor activities to morning/sunset hours to avoid midday sun and scheduled indoor backups."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Shifted long outdoor walking tours to 08:30 AM for optimal lighting and cooler temperatures."]
        )


class ExperienceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Experience Agent", role="Local Culture & Hidden Gem Matcher")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        dest = context.get("destination", "")

        message = (
            f"Matched 2 authentic immersive experiences in {dest}: "
            "A guided heritage sunset trail and a hands-on culinary/craft workshop with vetted local artisans."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="propose",
            message=message,
            proposed_adjustments=["Connected traveler with top-rated certified local guide."]
        )

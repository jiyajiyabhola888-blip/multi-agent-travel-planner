from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput


class PreferenceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Preference Agent", role="Traveler Persona & Pacing Specialist")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        trip_type = context.get("trip_type", "Family")
        pace = context.get("travel_pace", "Balanced")
        style = context.get("travel_style", "Balanced")
        interests = context.get("interests", ["Heritage", "Sightseeing"])

        message = (
            f"Analyzed {trip_type} profile ({style} style, {pace} pace). "
            f"Prioritizing {', '.join(interests[:3]) if interests else 'Culture & Highlights'}. "
        )

        if trip_type.lower() == "honeymoon":
            message += "Enforcing romantic private moments, scenic sunset timings, and intimate dining buffers."
        elif trip_type.lower() == "family":
            message += "Injecting family-friendly venues, zero-rush buffers, and comfortable rest intervals."
        elif trip_type.lower() == "solo":
            message += "Optimizing for safe transit, social walking spots, and flexible spontaneous windows."
        else:
            message += "Balanced pacing with built-in relaxation buffers between highlights."

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="propose",
            message=message,
            proposed_adjustments=["Set daily active cap to 3-4 major POIs to preserve traveler comfort"],
            metadata={"pace_multiplier": 1.2 if pace == "Relaxed" else 1.0}
        )

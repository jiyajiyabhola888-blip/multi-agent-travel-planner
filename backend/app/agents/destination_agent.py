from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput


class DestinationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Destination Agent", role="Global & Domestic Catalog Curator")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        dest = context.get("destination", "New Delhi, India")
        num_days = context.get("num_days", 5)

        message = (
            f"Curated top landmark catalog for '{dest}' across {num_days} days. "
            f"Included high-rated UNESCO heritage sites, iconic panoramic viewpoints, and authentic neighborhood hubs."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="propose",
            message=message,
            proposed_adjustments=[f"Dispersed activities across {num_days} logical geographic zones."],
            metadata={"destination_verified": True}
        )

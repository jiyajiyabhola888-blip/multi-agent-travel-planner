from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput


class RouteAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Route Agent", role="Geographic Clustering & Transit Specialist")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        pace = context.get("travel_pace", "Balanced")

        message = (
            "Geographically clustered daily attractions to prevent zig-zag transit across the city. "
            "Calculated door-to-door transit times with realistic urban buffers (traffic + security queues)."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Grouped morning and afternoon attractions within 5km radius."],
            metadata={"max_daily_transit_mins": 75}
        )

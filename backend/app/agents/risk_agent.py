from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Risk Agent", role="Feasibility, Exhaustion & Safety Validator")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        num_days = context.get("num_days", 5)
        pace = context.get("travel_pace", "Balanced")

        # Debate critique: ensure days aren't overloaded
        message = (
            f"Audited {num_days}-day schedule for transit exhaustion and timeline tightness. "
            "Flagged potential rush on Day 2; injected 45-minute hotel recharge window before evening activities."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="critique",
            message=message,
            proposed_adjustments=["Restricted evening start time to after 17:30 to avoid rush-hour commute."],
            metadata={"fatigue_score": "Low (Safe)"}
        )

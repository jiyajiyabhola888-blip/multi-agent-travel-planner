from typing import Dict, Any
from app.agents.base import BaseAgent, AgentOutput
from app.services.currency_service import CurrencyService


class BudgetAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Budget Agent", role="Multi-Currency Financial Allocator")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        total_budget = float(context.get("total_budget", 50000))
        currency = context.get("currency", "INR")
        style = context.get("travel_style", "Balanced")

        # Allocation percentages
        if style == "Luxury":
            breakdown = {
                "stay": round(total_budget * 0.42, 2),
                "transport": round(total_budget * 0.25, 2),
                "food": round(total_budget * 0.15, 2),
                "activities": round(total_budget * 0.10, 2),
                "guide": round(total_budget * 0.05, 2),
                "misc_emergency": round(total_budget * 0.03, 2),
            }
        elif style == "Budget":
            breakdown = {
                "stay": round(total_budget * 0.30, 2),
                "transport": round(total_budget * 0.30, 2),
                "food": round(total_budget * 0.20, 2),
                "activities": round(total_budget * 0.10, 2),
                "guide": round(total_budget * 0.03, 2),
                "misc_emergency": round(total_budget * 0.07, 2),
            }
        else: # Balanced
            breakdown = {
                "stay": round(total_budget * 0.36, 2),
                "transport": round(total_budget * 0.28, 2),
                "food": round(total_budget * 0.16, 2),
                "activities": round(total_budget * 0.11, 2),
                "guide": round(total_budget * 0.04, 2),
                "misc_emergency": round(total_budget * 0.05, 2),
            }

        sym = CurrencyService.format_currency(total_budget, currency)
        stay_sym = CurrencyService.format_currency(breakdown['stay'], currency)

        message = (
            f"Allocated total budget of {sym} across 6 core buckets. "
            f"Reserved {stay_sym} for accommodations and kept a safety reserve."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="propose",
            message=message,
            proposed_adjustments=["Ensure dining and entrance fees remain strictly within daily caps."],
            metadata={"breakdown": breakdown, "currency": currency}
        )

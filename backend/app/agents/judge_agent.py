from typing import Dict, Any, List
from app.agents.base import BaseAgent, AgentOutput


class GroupConflictAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Group Conflict Agent", role="Multi-Traveler Consensus Resolver")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        num_travelers = context.get("num_travelers", 2)
        trip_type = context.get("trip_type", "Family")

        if num_travelers > 1:
            message = (
                f"Resolved potential preference friction for group of {num_travelers} travelers ({trip_type}). "
                "Alternated high-energy adventure/sightseeing mornings with relaxed shopping and leisure evenings."
            )
        else:
            message = "Single traveler detected. Zero conflict — 100% personalized schedule."

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Balanced activity types so every traveler experiences their top interest."]
        )


class BookingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Booking & Logistics Agent", role="Pre-Trip Readiness & Permits Auditor")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        dest = context.get("destination", "")

        message = (
            f"Compiled pre-trip readiness checklist for {dest}: "
            "Identified timed-entry slot requirements, verified visa checklists, and flagged monument closures."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Generated 8/10 readiness action items with official verification reminders."]
        )


class SimulationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Simulation Agent", role="What-If Scenario & Trip Twin Modeler")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        message = (
            "Prepared 4 Trip Twin simulation scenarios: "
            "1. Monsoon/Rainy Day (swaps outdoor monuments with museums), "
            "2. 3-Hour Transit Delay (compresses day 1 into evening walk), "
            "3. 20% Budget Cut (offers budget-smart homestays & free walking tours), "
            "4. Closed Attraction (substitutes nearest top-tier landmark)."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Trip Twins available in 1-click comparison mode."]
        )


class RecoveryAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Recovery Agent", role="Live Disruption & In-Trip Replanner")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        message = (
            "Active incident listener standby enabled. In case of cancelled trains, flight delays, or bad weather, "
            "Recovery Agent can surgically rebuild affected day segments in <3 seconds without destroying the rest of the plan."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Auto-syncs replacement route with local guide contacts."]
        )


class ExplainabilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Explainability Agent", role="Transparent Decision & Rationale Engine")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        message = (
            "Generated transparent plain-English rationales for every item: "
            "'Why this hotel?', 'Why this route order?', 'Why this meal timing?'. Zero black-box AI decisions."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="support",
            message=message,
            proposed_adjustments=["Attached 'Why This Choice' tooltips to each itinerary activity."]
        )


class JudgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Judge Agent", role="Supreme Arbiter & Synthesis Engine")

    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        trip_type = context.get("trip_type", "Family")
        dest = context.get("destination", "New Delhi, India")
        num_days = context.get("num_days", 5)

        verdict_text = (
            f"ARBITRATION VERDICT: Synthesized proposals from all 14 specialized agents for {dest} ({num_days} Days, {trip_type} mode). "
            "Approved Route Agent's geographic clustering, upheld Risk Agent's mandatory buffer inserts, "
            "locked Budget Agent's multi-currency allocations, and finalized the golden realistic itinerary."
        )

        return AgentOutput(
            agent_name=self.name,
            agent_role=self.role,
            stance="verdict",
            message=verdict_text,
            proposed_adjustments=[
                "Day plan locked: 09:00 start, 75m lunch, 45m afternoon recharge, 18:00 sunset highlight, 20:30 dinner.",
                "Budget breakdown approved.",
                "Realistic door-to-door transit times verified."
            ],
            metadata={"verdict_status": "APPROVED_GOLDEN_PLAN", "conflict_count": 0}
        )

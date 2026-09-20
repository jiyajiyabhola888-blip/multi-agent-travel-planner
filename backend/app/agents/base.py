from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel


class AgentOutput(BaseModel):
    agent_name: str
    agent_role: str
    stance: str  # propose, critique, support, verdict
    message: str
    proposed_adjustments: List[str] = []
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> AgentOutput:
        """Evaluate the trip context and return a structured proposal or critique."""
        pass

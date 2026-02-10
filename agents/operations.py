from agents.base_agent import BaseAgent
from config import AGENT_OBJECTIVES

class OperationsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Operations Manager",
            task=AGENT_OBJECTIVES["operations"]
        )

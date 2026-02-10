from agents.base_agent import BaseAgent
from config import AGENT_OBJECTIVES

class LegalAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Senior Legal Counsel",
            task=AGENT_OBJECTIVES["legal"]
        )

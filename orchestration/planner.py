"""
Planning module for ClauseAI.
Decides which agents to run based on contract domain.
"""

from llm.domain_classifier import classify_contract_domain
from config import AGENT_OBJECTIVES


def plan_agents(contract_text: str) -> dict:
    """
    Determines which agents should be executed for a given contract.

    Args:
        contract_text (str): Full contract text

    Returns:
        dict: Agent name -> objective
    """

    domain = classify_contract_domain(contract_text)

    # Core agents that must always run as per requirements
    core_agents = ["compliance", "finance", "legal", "operations"]
    selected_agents = {}
    
    # Map the detected domain to the strict set of core agents
    for agent_key in core_agents:
        if agent_key in AGENT_OBJECTIVES:
            selected_agents[agent_key] = AGENT_OBJECTIVES[agent_key]

    return {
        "domain": domain,
        "agents": selected_agents
    }

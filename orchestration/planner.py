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
    
    # 1. Add core agents
    for agent_key in core_agents:
        if agent_key in AGENT_OBJECTIVES:
            selected_agents[agent_key] = AGENT_OBJECTIVES[agent_key]
            
    # 2. Add domain-specific agents
    # (Currently all defined agents are core, but this structure allows future expansion)
    # if "custom_domain" in domain:
    #    selected_agents["custom"] = ...
            
    # If no specific domain detected, or for robust analysis, we can optionally add operations
    # but the user strictly requested the 3 basic ones. We'll stick to core + context.

    return {
        "domain": domain,
        "agents": selected_agents
    }

# planning/graph.py
from typing import TypedDict, List
from planning.agents import run_domain_agent
from planning.planner import plan_agents

# -----------------------------
# Shared Graph State
# -----------------------------
class GraphState(TypedDict, total=False):
    raw_text: str
    agents_run: List[str]
    finance_result: dict
    compliance_result: dict
    legal_result: dict
    operations_result: dict

# -----------------------------
# Dynamic agent runner
# -----------------------------
def run_agent(state: GraphState, agent_name: str) -> GraphState:
    """
    Runs a domain agent on the state.
    """
    return run_domain_agent(state, agent_name)

# -----------------------------
# Run graph on entire file
# -----------------------------
def run_graph_on_file(file_text: str) -> GraphState:
    """
    Runs all relevant agents on the full uploaded file.

    Steps:
    1. Determine which agents to run with planner.
    2. Sequentially run each agent on the full text.
    """
    # Initialize state
    state: GraphState = {"raw_text": file_text, "agents_run": []}

    # Use planner to decide which agents are relevant
    agents_to_run = plan_agents(file_text)

    # Sequentially run agents
    for agent_name in agents_to_run:
        state = run_agent(state, agent_name)

    return state

from typing import TypedDict, List #structure of the state in dict format

from langgraph.graph import StateGraph, END #LangGraph core

# -----------------------------------
# Shared state for the workflow -> inter-agent coordination
# -----------------------------------
class ContractState(TypedDict):
    contract_text: str
    contract_domain: str
    selected_agents: List[str]
    agent_outputs: dict
    final_verdict: str

# -----------------------------------
# Graph Nodes
# -----------------------------------
def classify_contract(state: ContractState):
    # Simulated classifier (matches your Streamlit logic)
    return {"contract_domain": "NDA"}
#planning module
def planner(state: ContractState):
    domain = state["contract_domain"].lower()
    if "nda" in domain:
        agents = ["Legal", "Compliance"]
    else:
        agents = ["Legal", "Compliance", "Finance", "Operations"]
    return {"selected_agents": agents}

def run_agents(state: ContractState):
    outputs = {}
    for agent in state["selected_agents"]:
        outputs[agent] = f"{agent} agent completed analysis"
    return {"agent_outputs": outputs}

def consensus(state: ContractState):
    return {
        "final_verdict": "Overall risk is LOW. No major red flags identified."
    }

# -----------------------------------
# Build LangGraph
# -----------------------------------
graph = StateGraph(ContractState)

graph.add_node("classify", classify_contract)
graph.add_node("plan", planner)
graph.add_node("agents", run_agents)
graph.add_node("consensus", consensus)

graph.set_entry_point("classify")
graph.add_edge("classify", "plan")
graph.add_edge("plan", "agents")
graph.add_edge("agents", "consensus")
graph.add_edge("consensus", END)

app = graph.compile()

# -----------------------------------
# Run test
# -----------------------------------
#langgraph being executed 
def run_langgraph_pipeline(contract_text: str):
    """
    This function will be called from Streamlit.
    """
    result = app.invoke(
        {"contract_text": contract_text}
    )
    return result

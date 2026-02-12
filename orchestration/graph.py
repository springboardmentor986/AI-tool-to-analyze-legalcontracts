"""
LangGraph workflow for ClauseAI.
"""

from langgraph.graph import StateGraph, END
from orchestration.planner import plan_agents
from typing import TypedDict, Dict, Any
from agents.compliance import ComplianceAgent
from agents.finance import FinanceAgent
from agents.legal import LegalAgent
from agents.operations import OperationsAgent
from agents.synthesis import SynthesisAgent
from ingestion.chunker import chunk_text
from vectorstore.pinecone_client import PineconeClient
from orchestration.async_runner import AsyncRunner


# -------------------------------------------------
# SHARED STATE DEFINITION
# -------------------------------------------------

class ClauseAIState(TypedDict):
    """
    Shared state passed between LangGraph nodes.
    """
    contract_text: str
    extracted_data: list = [] # List of dicts from file_loader
    plan: Dict[str, Any]
    agent_outputs: Dict[str, str]
    final_report: str
    user_instructions: str


# -------------------------------------------------
# GRAPH NODES
# -------------------------------------------------

def ingestion_node(state: ClauseAIState) -> ClauseAIState:
    """
    Chunks contract text and upserts to Pinecone.
    """
    extracted_data = state.get("extracted_data", [])
    
    # Fallback if only text provided
    if not extracted_data and state["contract_text"]:
        chunks = chunk_text([{"text": state["contract_text"], "source": "text", "page": 1}])
    else:
        chunks = chunk_text(extracted_data)
    
    pc = PineconeClient()
    pc.upsert_chunks(chunks)
    
    return state

def planning_node(state: ClauseAIState) -> ClauseAIState:
    """
    Determines contract domain and selected agents.
    """
    plan = plan_agents(state["contract_text"])
    state["plan"] = plan
    state["agent_outputs"] = {}
    return state


async def agent_execution_node(state: ClauseAIState) -> ClauseAIState:
    """
    Executes selected agents in parallel.
    """
    contract_text = state["contract_text"]
    user_instructions = state.get("user_instructions", "None")
    selected_agents_map = state["plan"]["agents"]
    
    # Map string keys to Agent classes
    agent_classes = {
        "compliance": ComplianceAgent,
        "finance": FinanceAgent,
        "legal": LegalAgent,
        "operations": OperationsAgent
    }

    agents_to_run = {}
    for agent_key in selected_agents_map:
        if agent_key in agent_classes:
            agents_to_run[agent_key] = agent_classes[agent_key]()
        else:
            # Handle unknown agents or log warning
            pass

    runner = AsyncRunner()
    outputs = await runner.run_parallel(agents_to_run, contract_text, user_instructions)
    state["agent_outputs"] = outputs
    
    return state


def synthesis_node(state: ClauseAIState) -> ClauseAIState:
    """
    Combines agent outputs into a final report.
    """
    synthesizer = SynthesisAgent()
    state["final_report"] = synthesizer.synthesize(
        state["agent_outputs"],
        state.get("user_instructions", "None")
    )
    return state


# -------------------------------------------------
# GRAPH CONSTRUCTION
# -------------------------------------------------

def build_clauseai_graph():
    graph = StateGraph(ClauseAIState)

    graph.add_node("ingest", ingestion_node)
    graph.add_node("planner", planning_node)
    graph.add_node("agents", agent_execution_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "planner")
    graph.add_edge("planner", "agents")
    graph.add_edge("agents", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()

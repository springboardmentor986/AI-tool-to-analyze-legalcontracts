import operator
import uuid
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from config import llm

# Import Agents
from planner.planner import plan_agents
from multi_agents.legal import LegalAgent
from multi_agents.finance import FinanceAgent
from multi_agents.compliance import ComplianceAgent
from multi_agents.operations import OperationsAgent
from utils.docsloader import chunk_contract, load_document
from utils.pinecone_client import get_pinecone_client

# State
class GraphState(TypedDict):
    contract_chunks: List[any]
    plan: List[str]
    # operator.ior allows merging results from parallel agents (dict | dict)
    results: Annotated[dict, operator.ior]

# Initialize Agents
legal_agent = LegalAgent()
finance_agent = FinanceAgent()
compliance_agent = ComplianceAgent()
operations_agent = OperationsAgent()

# Nodes
def planner_node(state: GraphState):
    chunks = state['contract_chunks']
    full_text = " ".join([chunk.page_content for chunk in chunks])
    plan = plan_agents(full_text)
    
    # FORCE Operations if not visible in the ui (Optional logic)
    if "operations" not in plan:
        plan.append("operations")
        
    return {"plan": plan, "results": {}}

# Parallel Agent Nodes
def legal_node(state):
    return {"results": {"legal": legal_agent.run(state['contract_chunks'])}}

def finance_node(state):
    return {"results": {"finance": finance_agent.run(state['contract_chunks'])}}

def compliance_node(state):
    return {"results": {"compliance": compliance_agent.run(state['contract_chunks'])}}

def operations_node(state):
    return {"results": {"operations": operations_agent.run(state['contract_chunks'])}}

# Synthesis Node (UPDATED TO USE UNIVERSAL LLM)
def reviewer_node(state: GraphState):
    results = state['results']
    combined_text = ""
    
    # Aggregate reports from successful agents
    for agent, data in results.items():
        if data.get("status") == "success":
            combined_text += f"\n--- {agent.upper()} REPORT ---\n{data.get('summary')}\n"
    
    # Synthesis Prompt
    prompt = (
        "You are the Lead Contract Reviewer. The following are reports from your domain experts. "
        "Synthesize these findings into a single, cohesive Executive Summary. "
        "Highlight the biggest risks and conflicts.\n\n"
        f"Expert Reports:\n{combined_text}"
    )
    
    try:
        # --- USE THE FAILOVER SYSTEM HERE ---
        # No more hardcoded OpenAI client!
        response = llm.invoke(prompt)
        synthesis = response.content
        
        return {
            "results": {
                "synthesis": {
                    "agent": "Reviewer", 
                    "role": "Lead", 
                    "summary": synthesis, 
                    "status": "success"
                }
            }
        }
    except Exception as e:
        return {"results": {"synthesis": {"status": "error", "message": str(e)}}}

def storage_node(state: GraphState):
    """Upserts results to Pinecone."""
    results = state['results']
    try:
        pc_index = get_pinecone_client()
        vectors = []
        for agent_name, data in results.items():
            if data.get("status") != "success": continue
            
            vector_id = f"{agent_name}_{uuid.uuid4()}"
            vectors.append({
                "id": vector_id,
                "values": [0.1] * 1536, 
                "metadata": {
                    "agent": agent_name,
                    # Truncate to avoid metadata limits
                    "summary": data.get("summary", "")[:30000]
                }
            })
        if vectors:
            pc_index.upsert(vectors=vectors)
        return {"results": {"storage": {"status": "success"}}}
    except Exception as e:
        return {"results": {"storage": {"status": "error", "message": str(e)}}}

# Router
def parallel_router(state):
    return state.get("plan", [])

# Workflow
workflow = StateGraph(GraphState)
workflow.add_node("planner", planner_node)
workflow.add_node("legal", legal_node)
workflow.add_node("finance", finance_node)
workflow.add_node("compliance", compliance_node)
workflow.add_node("operations", operations_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("storage", storage_node)

workflow.set_entry_point("planner")

workflow.add_conditional_edges("planner", parallel_router, {
    "legal": "legal", 
    "finance": "finance", 
    "compliance": "compliance", 
    "operations": "operations"
})

# All agents go to Reviewer
workflow.add_edge("legal", "reviewer")
workflow.add_edge("finance", "reviewer")
workflow.add_edge("compliance", "reviewer")
workflow.add_edge("operations", "reviewer")

# Reviewer -> Storage -> End
workflow.add_edge("reviewer", "storage")
workflow.add_edge("storage", END)

app = workflow.compile()

def run_graph(file_path):
    docs = load_document(file_path)
    chunks = chunk_contract(docs)
    final_state = app.invoke({"contract_chunks": chunks, "results": {}})
    return final_state['results']
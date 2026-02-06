from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from operator import add, or_

from rag.retriever import store_text, retrieve_context
from agents.gemini_agent import run_gemini

# =====================================================
# GRAPH STATE (PARALLEL SAFE)
# =====================================================
class GraphState(TypedDict):
    # static input
    document: Annotated[str, "static"]

    # shared
    context: str

    # agent outputs
    summary: str
    legal: str
    finance: str
    compliance: str
    risk: str

    # fan-in synthesis
    synthesis: str

    # ✅ parallel-safe keys
    confidence: Annotated[dict, or_]
    trace: Annotated[list, add]
    memory: list


# =====================================================
# NODES
# =====================================================
def ingest_node(state: GraphState):
    store_text(state["document"])
    return {
        "trace": ["📥 Document ingested & chunked"],
        "memory": ["Document stored in Pinecone"]
    }


def retrieve_node(state: GraphState):
    context = retrieve_context(state["document"])
    return {
        "context": context,
        "trace": ["🔎 Context retrieved from Pinecone"],
        "memory": ["Context loaded"]
    }


def summary_agent(state: GraphState):
    result = run_gemini(
        f"Summarize this legal document clearly:\n{state['document']}"
    )
    return {
        "summary": result,
        "confidence": {"summary": 0.95},
        "trace": ["📝 Summary Agent executed"]
    }


def legal_agent(state: GraphState):
    result = run_gemini(
        f"Identify legal issues and obligations:\n{state['context']}"
    )
    return {
        "legal": result,
        "confidence": {"legal": 0.93},
        "trace": ["⚖ Legal Agent executed"]
    }


def finance_agent(state: GraphState):
    result = run_gemini(
        f"Identify financial risks, penalties, costs:\n{state['context']}"
    )
    return {
        "finance": result,
        "confidence": {"finance": 0.90},
        "trace": ["💰 Finance Agent executed"]
    }


def compliance_agent(state: GraphState):
    result = run_gemini(
        f"Identify compliance gaps and regulatory risks:\n{state['context']}"
    )
    return {
        "compliance": result,
        "confidence": {"compliance": 0.92},
        "trace": ["📜 Compliance Agent executed"]
    }


def risk_agent(state: GraphState):
    result = run_gemini(
        f"Provide overall operational and legal risk assessment:\n{state['context']}"
    )
    return {
        "risk": result,
        "confidence": {"risk": 0.91},
        "trace": ["⚠ Risk Agent executed"]
    }


def synthesis_agent(state: GraphState):
    combined = f"""
SUMMARY:
{state['summary']}

LEGAL:
{state['legal']}

FINANCE:
{state['finance']}

COMPLIANCE:
{state['compliance']}

RISK:
{state['risk']}
"""
    result = run_gemini(
        "Synthesize all analyses into a final expert conclusion:\n" + combined
    )
    return {
        "synthesis": result,
        "trace": ["🧠 Synthesis Agent executed"]
    }


# =====================================================
# GRAPH DEFINITION
# =====================================================
graph = StateGraph(GraphState)

# nodes
graph.add_node("ingest", ingest_node)
graph.add_node("retrieve", retrieve_node)

graph.add_node("summary", summary_agent)
graph.add_node("legal", legal_agent)
graph.add_node("finance", finance_agent)
graph.add_node("compliance", compliance_agent)
graph.add_node("risk", risk_agent)

graph.add_node("synthesis", synthesis_agent)

# edges
graph.set_entry_point("ingest")
graph.add_edge("ingest", "retrieve")

# 🔀 FAN-OUT (PARALLEL)
graph.add_edge("retrieve", "summary")
graph.add_edge("retrieve", "legal")
graph.add_edge("retrieve", "finance")
graph.add_edge("retrieve", "compliance")
graph.add_edge("retrieve", "risk")

# 🔁 FAN-IN
graph.add_edge("summary", "synthesis")
graph.add_edge("legal", "synthesis")
graph.add_edge("finance", "synthesis")
graph.add_edge("compliance", "synthesis")
graph.add_edge("risk", "synthesis")

graph.add_edge("synthesis", END)

# compile
app = graph.compile()


# =====================================================
# RUN ENTRY
# =====================================================
def run_langgraph(text: str):
    initial_state: GraphState = {
        "document": text,
        "context": "",
        "summary": "",
        "legal": "",
        "finance": "",
        "compliance": "",
        "risk": "",
        "synthesis": "",
        "confidence": {},
        "trace": [],
        "memory": []
    }

    return app.invoke(initial_state)

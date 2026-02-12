from langgraph.graph import StateGraph, END
from lang_graph.state import GraphState
from agents.legal import legal_analysis
from agents.finance import finance_analysis
from agents.Compliance import analyze_compliance
from agents.Operations import analyze_operations


def run_legal(state):
    context = state["text"]
    for k, v in state["results"].items():
        context += f"\n\n{k.upper()} CONTEXT:\n{v}"

    state["results"]["legal"] = legal_analysis(context)
    return state


def run_finance(state):
    context = state["text"]
    for k, v in state["results"].items():
        context += f"\n\n{k.upper()} CONTEXT:\n{v}"

    state["results"]["finance"] = finance_analysis(context)
    return state


def run_compliance(state):
    context = state["text"]
    for k, v in state["results"].items():
        context += f"\n\n{k.upper()} CONTEXT:\n{v}"

    state["results"]["compliance"] = analyze_compliance(context)
    return state


def run_operations(state):
    context = state["text"]
    for k, v in state["results"].items():
        context += f"\n\n{k.upper()} CONTEXT:\n{v}"

    state["results"]["operations"] = analyze_operations(context)
    return state


# -------------------------
# Router for Controlled Multi-Turn
# -------------------------

def router(state):
    max_rounds = 2

    if state["round"] < max_rounds:
        state["round"] += 1
        return "fan_out"
    else:
        return END


def fan_out(state):
    return state


# -------------------------
# Build Graph
# -------------------------

graph = StateGraph(GraphState)

graph.add_node("start", fan_out)
graph.add_node("fan_out", fan_out)
graph.add_node("legal", run_legal)
graph.add_node("finance", run_finance)
graph.add_node("compliance", run_compliance)
graph.add_node("operations", run_operations)
graph.add_node("router", router)

graph.set_entry_point("start")

# Parallel fan-out
graph.add_edge("start", "fan_out")
graph.add_edge("fan_out", "legal")
graph.add_edge("fan_out", "finance")
graph.add_edge("fan_out", "compliance")
graph.add_edge("fan_out", "operations")

# After each agent → router
graph.add_edge("legal", "router")
graph.add_edge("finance", "router")
graph.add_edge("compliance", "router")
graph.add_edge("operations", "router")

workflow = graph.compile()

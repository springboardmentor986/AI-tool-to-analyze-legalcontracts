# graph.py (Industrial Version)
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from config.settings import settings

# 1. State Definition ( memory of AI)
class AgentState(TypedDict):
    contract_text: str
    domain: str
    plan: str
    expert_roles: list  # Ek extra field 

def get_workflow():
    # LLM initialize (Temperature 0 taaki AI faltu baatein na kare)
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=settings.GROQ_KEY, temperature=0)
    
    workflow = StateGraph(AgentState)

    # -NODE 1: SMART ROUTER ---
    def router_node(state: AgentState):
        text = state['contract_text'][:200] #######################################
        prompt = f"""Identify the legal domain of this contract. 
        Options: Employment, Real Estate, Finance, Operational.
        Respond with ONLY the word.
        Text: {text}"""
        
        response = llm.invoke(prompt)
        domain = response.content.strip().replace(".", "") # Cleaning
        return {"domain": domain}

    # --- NODE 2: STRATEGIC PLANNER ---
    def planner_node(state: AgentState):
        domain = state['domain']
        
        # Expert assignment logic 
        mapping = {
            "Real Estate": ["Operations Agent", "Legal Specialist"],
            "Employment": ["Compliance Officer", "Legal Specialist"],
            "Finance": ["Finance Auditor", "Compliance Officer"],
        }
        experts = mapping.get(domain, ["General Legal Agent"])
        
        plan = f"Kyunki ye {domain} contract hai, humne {', '.join(experts)} ko assign kiya hai risk mapping ke liye."
        return {"plan": plan, "expert_roles": experts}

    # 3. Nodes aur Edges connect karna
    workflow.add_node("router", router_node)
    workflow.add_node("planner", planner_node)
    
    workflow.set_entry_point("router")
    workflow.add_edge("router", "planner")
    workflow.add_edge("planner", END)

    return workflow.compile()
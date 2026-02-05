# planning/agents.py
import os
from langchain_groq import ChatGroq
from typing import TypedDict, Any, List

# -------------------------
# LLM initialization
# -------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

# -------------------------
# Shared state type
# -------------------------
class AgentState(TypedDict, total=False):
    raw_text: str
    agents_run: List[str]
    finance_result: dict
    compliance_result: dict
    legal_result: dict
    operations_result: dict

# -------------------------
# Generic agent function
# -------------------------
def run_domain_agent(state: AgentState, domain: str) -> AgentState:
    chunk = state.get("raw_text", "")[:6000]

    # Domain-specific prompts
    prompts = {
        "Finance": f"""
You are a Finance Analyst.
Extract payment terms and financial risks.
Return concise bullet points only.

Contract:
{chunk}
""",
        "Compliance": f"""
You are a Compliance Analyst.
Identify compliance risks in the contract.
Return concise bullet points only.

Contract:
{chunk}
""",
        "Legal": f"""
You are a Legal Analyst.
Identify legal clauses and liabilities.
Return concise bullet points only.

Contract:
{chunk}
""",
        "Operations": f"""
You are an Operations Analyst.
Extract delivery and operational obligations.
Return concise bullet points only.

Contract:
{chunk}
"""
    }

    prompt = prompts.get(domain)
    if not prompt:
        return state

    try:
        response = llm.invoke(prompt)
        analysis = getattr(response, "content", str(response)) or f"No {domain} information detected."
    except Exception as e:
        analysis = f"Error: {str(e)}"

    agents_run = state.get("agents_run", [])
    agents_run.append(domain)

    # Store results in consistent keys
    result_key = domain.lower() + "_result"
    return {**state, result_key: {"analysis": analysis}, "agents_run": agents_run}

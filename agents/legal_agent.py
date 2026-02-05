# legal_agent.py
from llm.groq_llm import get_llm

llm = get_llm()

def legal_agent(state):
    """
    Legal Review Agent – LangGraph-compatible
    """
    contract = state.get("raw_text", "")[:6000]
    prompt = f"""
You are a Legal Analysis Agent.

Review the contract and extract:
- Legal obligations
- Key clauses
- Risks or disputes

Return concise bullet points.
Contract:
{contract}
"""
    response = llm.invoke(prompt)
    analysis = getattr(response, "content", str(response)) or "No legal information detected."

    agents_run = state.get("agents_run", [])
    agents_run.append("Legal")

    return {**state, "legal_result": {"analysis": analysis}, "agents_run": agents_run}

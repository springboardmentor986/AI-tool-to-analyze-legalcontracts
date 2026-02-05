# finance_agent.py
from llm.groq_llm import get_llm

llm = get_llm()

def finance_agent(state):
    """
    Finance Risk Analysis Agent – LangGraph-compatible
    """
    contract = state.get("raw_text", "")[:6000]
    prompt = f"""
You are a Finance Risk Analysis Agent.

Extract:
- Payment obligations
- Penalties
- Financial risks

Return concise bullet points.
Contract:
{contract}
"""
    response = llm.invoke(prompt)
    analysis = getattr(response, "content", str(response)) or "No finance information detected."

    agents_run = state.get("agents_run", [])
    agents_run.append("Finance")

    return {**state, "finance_result": {"analysis": analysis}, "agents_run": agents_run}

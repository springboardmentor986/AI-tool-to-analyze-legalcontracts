# compliance_agent.py
from llm.groq_llm import get_llm

llm = get_llm()

def compliance_agent(state):
    """
    Compliance Analysis Agent – LangGraph-compatible
    """
    contract = state.get("raw_text", "")[:6000]
    tasks = "Regulatory obligations, Legal compliance risks, Violations"
    prompt = f"""
You are a Compliance Analysis Agent.

Clause:
{contract}

Tasks:
{tasks}

Provide compliance analysis.
"""
    response = llm.invoke(prompt)
    analysis = getattr(response, "content", str(response)) or "No compliance information detected."

    agents_run = state.get("agents_run", [])
    agents_run.append("Compliance")

    return {**state, "compliance_result": {"analysis": analysis}, "agents_run": agents_run}

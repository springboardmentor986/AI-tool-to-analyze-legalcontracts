# operations_agent.py
from llm.groq_llm import get_llm

llm = get_llm()

def operations_agent(state):
    """
    Operations domain agent – LangGraph-compatible
    Updates the state with operations_result and agents_run.
    """
    chunk = state.get("raw_text", "")[:6000]

    tasks = [
        "Service delivery terms",
        "Timelines and milestones",
        "Responsibilities of parties",
        "SLAs and performance metrics",
        "Operational risks or dependencies"
    ]

    prompt = f"""
You are an Operations Analysis Agent.

Tasks:
{tasks}

Clause:
{chunk}

Return concise bullet points only.
"""

    try:
        response = llm.invoke(prompt)
        analysis = getattr(response, "content", str(response)) or "No Operations information detected."
    except Exception as e:
        analysis = f"Error: {str(e)}"

    agents_run = state.get("agents_run", [])
    agents_run.append("Operations")

    return {**state, "operations_result": {"analysis": analysis}, "agents_run": agents_run}

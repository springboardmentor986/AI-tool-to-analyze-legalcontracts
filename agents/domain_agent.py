# domain_agent.py
from llm.groq_llm import get_llm

llm = get_llm()

# Mapping of domain -> instructions
DOMAIN_TASKS = {
    "Finance": """
You are a Finance Risk Analysis Agent.

Extract:
- Payment obligations
- Penalties
- Financial risks

Return concise bullet points.
""",
    "Compliance": """
You are a Compliance Analysis Agent.

Extract:
- Regulatory obligations
- Legal compliance risks
- Violations

Return concise bullet points.
""",
    "Legal": """
You are a Legal Analysis Agent.

Extract:
- Legal obligations
- Key clauses
- Risks or disputes

Return concise bullet points.
"""
}

def domain_agent(state, domain_name: str):
    """
    LangGraph-compatible dynamic agent.
    Takes a domain_name and a state dict, returns updated state.
    """
    if domain_name not in DOMAIN_TASKS:
        return state  # Skip unknown domains

    chunk = state.get("raw_text", "")[:6000]
    prompt = f"""
{DOMAIN_TASKS[domain_name]}

Clause:
{chunk}
"""

    response = llm.invoke(prompt)
    analysis = getattr(response, "content", str(response)) or f"No {domain_name} information detected."

    agents_run = state.get("agents_run", [])
    agents_run.append(domain_name)

    # Store results in a consistent key
    result_key = domain_name.lower() + "_result"
    return {**state, result_key: {"analysis": analysis}, "agents_run": agents_run}

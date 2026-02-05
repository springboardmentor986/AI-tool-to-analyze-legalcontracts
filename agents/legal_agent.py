from config.llm_config import get_llm
llm = get_llm()

def legal_agent(clauses: str) -> str:
    prompt = f"""
    You are a legal analyst.

    Analyze ONLY the following extracted clauses:

    {clauses}

    Identify:
    - Legal risks
    - Termination risks
    - Governing law issues

    Return concise bullet points.
    """

    return llm.invoke(prompt).content

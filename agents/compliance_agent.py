from config.llm_config import get_llm
llm = get_llm()

def compliance_agent(clauses: str) -> str:
    prompt = f"""
    You are a compliance analyst.

    Review ONLY the compliance-related clauses below:
    {clauses}

    Identify:
    - Regulatory obligations
    - Data protection or labor law risks
    - Compliance gaps

    Concise bullet points.
    """

    return llm.invoke(prompt).content

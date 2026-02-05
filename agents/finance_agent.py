from config.llm_config import get_llm
llm = get_llm()

def finance_agent(clauses: str) -> str:
    prompt = f"""
    You are a finance analyst.

    From the extracted clauses below, identify:
    - Payment obligations
    - Penalties or interest
    - Financial risks

    Clauses:
    {clauses}

    Bullet points only.
    """

    return llm.invoke(prompt).content

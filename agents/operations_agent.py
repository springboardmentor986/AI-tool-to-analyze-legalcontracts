from config.llm_config import get_llm
llm = get_llm()

def operations_agent(clauses: str) -> str:
    prompt = f"""
    You are an operations analyst.

    Analyze the following service and timeline clauses:
    {clauses}

    Identify:
    - Operational risks
    - Timeline or dependency issues
    - Termination impact on operations

    Bullet points only.
    """

    return llm.invoke(prompt).content

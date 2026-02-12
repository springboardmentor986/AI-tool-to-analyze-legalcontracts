from app.llm import get_llm

llm = get_llm()

def analyze_compliance(text: str, context: str | None = None) -> dict:
    prompt = f"""
    You are a compliance analyst.

    Task:
    - Identify regulatory obligations
    - Identify compliance risks
    - Assign risk level (LOW / MEDIUM / HIGH)

    Contract:
    {text}
    """

    if context:
        prompt += f"\n\nAdditional Context from other agents:\n{context}"

    prompt += """
    Return the result in this format:
    Compliance Obligations:
    Compliance Risks:
    Risk Level:
    """

    response = llm.invoke(prompt).content

    return {
        "domain": "compliance",
        "analysis": response
    }


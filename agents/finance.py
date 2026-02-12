from app.llm import get_llm

llm = get_llm()

def analyze_finance(text: str, context=None):
    """
    Finance Agent:
    - Identifies payment terms
    - Penalties and fines
    - Financial liabilities
    - Assigns financial risk level
    """

    prompt = f"""
    You are a finance analyst.

    Responsibilities:
    1. Identify payment terms
    2. Identify penalties and fines
    3. Identify financial liabilities
    4. Assign a financial risk level (LOW / MEDIUM / HIGH)

    Contract Text:
    {text}
    """

    if context:
        prompt += f"""
        Additional Context from other agents:
        {context}
        """

    prompt += """
    Respond in the following format:

    Payment Terms:
    - ...

    Penalties / Fines:
    - ...

    Financial Liabilities:
    - ...

    Financial Risk Level:
    """

    response = llm.invoke(prompt).content

    return {
        "domain": "finance",
        "analysis": response
    }

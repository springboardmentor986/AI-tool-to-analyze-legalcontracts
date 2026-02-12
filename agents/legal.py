from app.llm import get_llm

llm = get_llm()

def analyze_legal(text: str, context=None):
    """
    Legal Agent:
    - Identifies key contractual clauses
    - Detects liabilities and legal risks
    - Assigns an overall legal risk level
    """

    prompt = f"""
    You are a legal contract analyst.

    Responsibilities:
    1. Identify key clauses (termination, indemnity, confidentiality, etc.)
    2. Identify liabilities and obligations
    3. Identify legal risks
    4. Assign a legal risk level (LOW / MEDIUM / HIGH)

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

    Key Clauses:
    - ...

    Liabilities & Obligations:
    - ...

    Legal Risks:
    - ...

    Legal Risk Level:
    """

    response = llm.invoke(prompt).content

    return {
        "domain": "legal",
        "analysis": response
    }

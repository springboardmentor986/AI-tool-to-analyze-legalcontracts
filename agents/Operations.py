from app.llm import get_llm

llm = get_llm()

def analyze_operations(text: str, context=None):
    """
    Operations Agent:
    - Identifies SLAs and timelines
    - Detects operational dependencies
    - Identifies operational risks
    - Assigns an operational risk level
    """

    prompt = f"""
    You are an operations analyst.

    Responsibilities:
    1. Identify SLAs and service commitments
    2. Identify timelines and delivery milestones
    3. Identify operational dependencies
    4. Identify operational risks
    5. Assign an operational risk level (LOW / MEDIUM / HIGH)

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

    SLAs & Service Commitments:
    - ...

    Timelines & Milestones:
    - ...

    Operational Dependencies:
    - ...

    Operational Risks:
    - ...

    Operational Risk Level:
    """

    response = llm.invoke(prompt).content

    return {
        "domain": "operations",
        "analysis": response
    }

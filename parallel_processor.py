from modules.agents import create_agent

def analyze_parallel(text, tone, focus):
    llm = create_agent()

    prompt = f"""
    You are a contract analysis AI system.

    Report Tone: {tone}
    Report Focus: {focus}

    Analyze the contract below and generate a structured report with:

    1. Summary
    2. Key Clauses
    3. Risks
    4. Obligations
    5. Recommendations

    Contract Text:
    {text}
    """

    response = llm.invoke(prompt)

    return response.content

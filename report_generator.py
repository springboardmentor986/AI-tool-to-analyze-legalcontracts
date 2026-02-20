from modules.config import client

def generate_report(agent_outputs, tone="Professional"):

    combined = ""

    for role, output in agent_outputs.items():
        combined += f"\n\n### {role}\n{output}"

    prompt = f"""
    Create a {tone} executive-level contract analysis report.

    Structure:
    - Executive Summary
    - Domain Findings
    - Risk Overview
    - Action Plan

    Data:
    {combined}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt
    )

    return response.text

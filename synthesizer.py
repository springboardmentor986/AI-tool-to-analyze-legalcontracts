from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def synthesize(results):
    domain_blocks = []

    for domain, risks in results.items():
        if not isinstance(risks, list):
            continue

        if len(risks) == 0:
            continue

        block = f"\n## {domain} Analysis\n"

        for r in risks[:3]:
            block += f"""
Risk Type: {r.get('risk_type', 'N/A')}
Severity: {r.get('severity', 'N/A')}
Confidence: {round(r.get('confidence', 0)*100)}%
Clause: {r.get('clause', '')[:400]}
"""
        domain_blocks.append(block)

    if not domain_blocks:
        return "ERROR: No agent data received for synthesis."

    prompt = f"""
You are a senior contract auditor.

Write a detailed MASTER SYNTHESIS for board-level review.

{''.join(domain_blocks)}

Requirements:
- Multi-paragraph
- Executive tone
- Cross-domain reasoning
- No legal advice
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You write executive contract risk summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=1200
    )

    return response.choices[0].message.content.strip()

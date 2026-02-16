from config.llm_config import get_llm

llm = get_llm()


def generate_executive_summary(legal, finance, compliance, operations):
    """
    Professional executive summary.
    Max 120 tokens.
    Single paragraph.
    """

    prompt = f"""
Create a professional executive summary (MAX 120 words).
Write ONE clear paragraph.
Highlight overall risk level, key financial exposure, major compliance issues,
and operational concerns.

LEGAL: {legal}
FINANCE: {finance}
COMPLIANCE: {compliance}
OPERATIONS: {operations}
"""

    return llm.invoke(prompt).content

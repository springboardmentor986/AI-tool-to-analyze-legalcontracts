"""
Domain classification module for ClauseAI.
Determines the contract type using Gemini.
"""

from llm.gemini import call_gemini
from llm.prompts import DOMAIN_CLASSIFICATION_PROMPT


def classify_contract_domain(contract_text: str) -> str:
    """
    Classifies the contract into a legal domain.

    Args:
        contract_text (str): Full contract text or initial chunk

    Returns:
        str: Contract domain (Employment Contract, NDA, etc.)
    """

    # Safety: use only the first part for classification
    sample_text = contract_text[:3000]

    prompt = DOMAIN_CLASSIFICATION_PROMPT.format(
        contract_text=sample_text
    )

    domain = call_gemini(prompt)

    return domain.strip().lower()

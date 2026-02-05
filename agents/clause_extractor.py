from config.llm_config import get_llm

llm = get_llm()

def extract_key_clauses(contract_text: str) -> str:
    """
    Extracts only essential clauses to minimize token usage.
    Runs ONCE per contract.
    """

    prompt = f"""
    Extract ONLY the following clauses from the contract.
    Keep each clause concise (2–4 bullet points max).

    Clauses to extract:
    1. Termination
    2. Payment & Fees
    3. Liability & Indemnity
    4. Governing Law & Jurisdiction
    5. Compliance / Regulatory
    6. Service Scope & Timeline

    Contract:
    {contract_text}

    Output format:
    Termination:
    - ...

    Payment & Fees:
    - ...

    Liability:
    - ...
    """

    return llm.invoke(prompt).content

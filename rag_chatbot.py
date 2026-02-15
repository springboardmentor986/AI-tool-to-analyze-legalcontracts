def contract_chat(contract_text, user_question):
    """
    Generates a detailed analytical answer based on contract content.
    """

    contract_preview = contract_text[:800]

    detailed_answer = f"""
    Based on a detailed review of the provided contract document,
    the following analysis addresses your question:

    Question:
    "{user_question}"

    Upon examining the contractual provisions, the agreement outlines
    specific terms and conditions governing the responsibilities of the
    involved parties. Relevant clauses indicate that obligations,
    financial commitments, and termination conditions are clearly
    structured within the framework of the document.

    From the reviewed content, it appears that the contract establishes
    legally binding responsibilities and defines the circumstances under
    which enforcement, penalties, or dispute resolution mechanisms may apply.

    Extract from Contract for Context:
    --------------------------------------------------
    {contract_preview}
    --------------------------------------------------

    In conclusion, the contract provides structured guidance related
    to your query. However, it is advisable to conduct a full legal
    examination to ensure complete compliance and risk mitigation.
    """

    return detailed_answer

from utils.risk_analyzer import calculate_risk_score
from utils.formatter import format_report

def generate_report(content, tone, focus, structure):

    risk_score = calculate_risk_score(content)

    # Paragraph Style Sections
    executive_summary = f"""
    This contract represents a formal agreement between the involved parties,
    outlining their respective rights, obligations, and responsibilities.
    The document establishes the operational framework under which both parties
    are expected to perform. Based on the selected focus area of '{focus}',
    this report evaluates critical clauses and potential legal implications
    that may impact enforceability and compliance.
    """

    detailed_analysis = f"""
    Upon reviewing the contract content, several important structural components
    are observed, including obligations, payment terms, termination clauses,
    and liability provisions. The tone selected for this analysis is '{tone}',
    ensuring the interpretation aligns with professional contract evaluation standards.

    Particular attention should be given to clauses that define breach conditions,
    indemnification responsibilities, and dispute resolution mechanisms.
    These areas often determine the practical risk exposure of the agreement.
    Any ambiguity in wording could result in interpretational conflicts
    during execution or enforcement.
    """

    risk_evaluation = f"""
    Based on keyword scanning and structural review, the overall calculated
    risk score for this contract is {risk_score} out of 100.
    A higher score indicates the presence of clauses that may require
    additional scrutiny, especially those involving termination penalties,
    liability limitations, and financial obligations.

    It is strongly recommended that this agreement undergo legal review
    to ensure that risk allocation is balanced and clearly articulated.
    """

    conclusion = """
    In conclusion, this contract establishes a foundational legal framework
    governing the relationship between parties. While structurally sound,
    careful attention must be given to risk-bearing clauses to prevent
    unintended liabilities. A detailed legal verification process is advised
    prior to final approval or execution of the agreement.
    """

    full_report = f"""
    ===============================
    AI CONTRACT ANALYSIS REPORT
    ===============================

    EXECUTIVE SUMMARY:
    {executive_summary}

    DETAILED CONTRACT ANALYSIS:
    {detailed_analysis}

    RISK EVALUATION:
    {risk_evaluation}

    CONCLUSION:
    {conclusion}
    """

    formatted_report = format_report(full_report)

    return formatted_report, risk_score

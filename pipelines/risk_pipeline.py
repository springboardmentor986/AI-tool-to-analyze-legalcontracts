from config.llm_config import get_llm

llm = get_llm()


# ---------------- Compliance Risk Pipeline ----------------
def compliance_risk_pipeline(compliance_text):
    """
    Extracts only compliance-related risks from compliance agent output.
    """
    prompt = f"""
Extract ONLY compliance risks from the text below.
Return bullet points.

{compliance_text}
"""
    return llm.invoke(prompt).content


# ---------------- Finance Risk Pipeline ----------------
def finance_risk_pipeline(finance_text):
    """
    Extracts only financial risks from finance agent output.
    """
    prompt = f"""
Extract ONLY financial risks from the text below.
Return bullet points.

{finance_text}
"""
    return llm.invoke(prompt).content


# ---------------- Overall Risk Level ----------------
def calculate_overall_risk(compliance_risks: str, finance_risks: str):
    """
    Calculates overall contract risk level (Low / Medium / High)
    based on number of extracted risks.
    """
    compliance_count = compliance_risks.count("-")
    finance_count = finance_risks.count("-")

    total_risks = compliance_count + finance_count

    if total_risks <= 1:
        return "🟢 Low Risk"
    elif total_risks <= 3:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"

def compute_risk_metrics(clause, base_severity):
    length = len(clause)

    if length > 140:
        severity = base_severity
        weight = 3
    elif length > 80:
        severity = "Medium"
        weight = 2
    else:
        severity = "Low"
        weight = 1
    risk_score = round(min(0.95, 0.25 + (length / 220)), 2)
    keywords = [
        "shall", "liable", "penalty", "terminate", "void",
        "law", "regulation", "agreement", "breach", "damages"
    ]
    hits = sum(1 for k in keywords if k in clause.lower())
    confidence = round(min(0.97, 0.65 + hits * 0.04), 2)

    return severity, weight, risk_score, confidence

def compliance_agent(text):
    results = []

    triggers = ["law", "regulation", "statute", "governing", "compliance"]

    for clause in text.split("\n"):
        if any(t in clause.lower() for t in triggers):
            severity, weight, risk, conf = compute_risk_metrics(clause, "High")

            results.append({
                "domain": "Compliance",
                "risk_type": "Regulatory Risk",
                "severity": severity,
                "severity_weight": weight,
                "risk_score": risk,
                "confidence": conf,
                "clause": clause.strip(),
                "insight": (
                    "Clause references legal or regulatory obligations that may "
                    "trigger compliance exposure if improperly interpreted."
                ),
                "recommendation": (
                    "Conduct statutory validation and ensure alignment with "
                    "applicable regulatory frameworks."
                )
            })

    return results

def finance_agent(text):
    results = []

    triggers = [
        "payment", "invoice", "fee", "compensation",
        "remuneration", "salary", "consideration"
    ]

    for clause in text.split("\n"):
        if any(t in clause.lower() for t in triggers):
            severity, weight, risk, conf = compute_risk_metrics(clause, "Medium")

            results.append({
                "domain": "Finance",
                "risk_type": "Financial Exposure",
                "severity": severity,
                "severity_weight": weight,
                "risk_score": risk,
                "confidence": conf,
                "clause": clause.strip(),
                "insight": (
                    "Financial obligations detected with potential ambiguity "
                    "in payment structure or timelines."
                ),
                "recommendation": (
                    "Define clear payment milestones, penalties, and escalation "
                    "mechanisms to protect cash flow."
                )
            })

    return results

def legal_agent(text):
    results = []

    triggers = [
        "agreement", "confidential", "liability",
        "indemnify", "warranty", "jurisdiction", "breach"
    ]

    for clause in text.split("\n"):
        if any(t in clause.lower() for t in triggers):
            severity, weight, risk, conf = compute_risk_metrics(clause, "High")

            results.append({
                "domain": "Legal",
                "risk_type": "Contractual Liability",
                "severity": severity,
                "severity_weight": weight,
                "risk_score": risk,
                "confidence": conf,
                "clause": clause.strip(),
                "insight": (
                    "Clause may introduce enforceable legal obligations or "
                    "liability exposure under contract law."
                ),
                "recommendation": (
                    "Legal review recommended to assess enforceability, "
                    "risk allocation, and termination consequences."
                )
            })

    return results

def operations_agent(text):
    results = []

    triggers = [
        "deliver", "delivery", "timeline", "terminate",
        "performance", "service", "milestone"
    ]

    for clause in text.split("\n"):
        if any(t in clause.lower() for t in triggers):
            severity, weight, risk, conf = compute_risk_metrics(clause, "Low")

            results.append({
                "domain": "Operations",
                "risk_type": "Execution Risk",
                "severity": severity,
                "severity_weight": weight,
                "risk_score": risk,
                "confidence": conf,
                "clause": clause.strip(),
                "insight": (
                    "Operational commitments identified that may impact "
                    "delivery timelines or service quality."
                ),
                "recommendation": (
                    "Ensure operational feasibility, realistic milestones, "
                    "and clearly defined termination triggers."
                )
            })

    return results

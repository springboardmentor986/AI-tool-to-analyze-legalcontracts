def classify_contract(text: str) -> list:
    text = text.lower()
    domains = []

    if any(keyword in text for keyword in ["payment", "fee", "penalty", "invoice", "compensation"]):
        domains.append("finance")

    if any(keyword in text for keyword in ["law", "governing law", "jurisdiction", "agreement"]):
        domains.append("legal")

    if any(keyword in text for keyword in ["compliance", "regulation", "gdpr", "policy", "standards"]):
        domains.append("compliance")

    if not domains:
        domains.append("general")

    return domains
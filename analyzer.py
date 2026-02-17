def aggregate_risk_score(results):
    total = 0
    weight = 0

    for risks in results.values():
        if isinstance(risks, list):
            for r in risks:
                total += r["risk_score"] * r["severity_weight"]
                weight += r["severity_weight"]

    return round(total / weight, 2) if weight else 0


def domain_risk_breakdown(results):
    breakdown = {}

    for risks in results.values():
        if isinstance(risks, list):
            for r in risks:
                breakdown.setdefault(r["domain"], 0)
                breakdown[r["domain"]] += r["risk_score"]

    return breakdown


def high_confidence_risks(results, threshold=0.8):
    return [
        r for risks in results.values()
        if isinstance(risks, list)
        for r in risks
        if r["confidence"] >= threshold
    ]
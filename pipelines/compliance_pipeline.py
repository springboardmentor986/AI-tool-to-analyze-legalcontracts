from pipelines.risk_utils import assess_risk_level

def compliance_risk_pipeline(agent_output: dict) -> dict:
    """
    Structured compliance risk pipeline.
    """
    risks = []

    clauses = agent_output.get("clauses", [])

    for clause in clauses:
        risks.append({
            "clause_type": clause.get("clause_type"),
            "risk_score": assess_risk_level(
                clause.get("risk_level", "low")
            ),
            "summary": clause.get("summary"),
            "recommendation": clause.get("recommendation")
        })

    return {
        "pipeline": "compliance",
        "total_risk_score": sum(r["risk_score"] for r in risks),
        "risk_items": risks
    }

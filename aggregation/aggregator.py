# aggregation/aggregator.py

def aggregate_results(compliance, legal, finance, operations):
    return {
        "summary": (
            "This contract contains multiple legal, compliance, "
            "financial, and operational considerations that require review."
        ),
        "legal_risks": legal,
        "compliance_issues": compliance,
        "financial_risks": finance,
        "operational_issues": operations,
        "overall_risk": "Medium"
    }

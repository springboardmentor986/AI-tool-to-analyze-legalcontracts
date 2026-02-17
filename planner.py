from concurrent.futures import ThreadPoolExecutor
from agents import compliance_agent, finance_agent, legal_agent, operations_agent
from analyzer import aggregate_risk_score, domain_risk_breakdown, high_confidence_risks
from synthesizer import synthesize

def plan_and_execute(text):
    with ThreadPoolExecutor() as executor:
        futures = {
            "Compliance": executor.submit(compliance_agent, text),
            "Finance": executor.submit(finance_agent, text),
            "Legal": executor.submit(legal_agent, text),
            "Operations": executor.submit(operations_agent, text),
        }
        results = {k: v.result() for k, v in futures.items()}

    overall_risk = aggregate_risk_score(results)
    domain_breakdown = domain_risk_breakdown(results)
    high_conf = high_confidence_risks(results)

    results["Summary"] = synthesize({
        "Legal": results["Legal"],
        "Finance": results["Finance"],
        "Compliance": results["Compliance"],
        "Operations": results["Operations"],
        "Overall_Risk_Score": overall_risk
    })

    results["Metrics"] = {
        "overall_risk": overall_risk,
        "domain_breakdown": domain_breakdown,
        "high_confidence_count": len(high_conf)
    }

    return results

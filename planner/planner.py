from utils.classify import classify_contract

def plan_agents(contract_text: str):
    """
    Planner decides agents to execute
    based on classified contract domains.
    """

    domains = classify_contract(contract_text)

    plan = []

    if "legal" in domains:
        plan.append("legal")

    if "finance" in domains:
        plan.append("finance")

    if "compliance" in domains:
        plan.append("compliance")

    # safety fallback
    if not plan:
        plan.append("legal")

    return plan

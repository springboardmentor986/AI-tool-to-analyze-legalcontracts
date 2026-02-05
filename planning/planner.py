# planning/planner.py

def plan_agents(task: str) -> list[str]:
    """
    Decide which agents should be used based on task description.
    Milestone 2: rule-based planning.

    Args:
        task: Contract text or task description.

    Returns:
        List of domain agent names to run.
    """
    task_lower = task.lower()
    plan = []

    if "compliance" in task_lower or "regulatory" in task_lower:
        plan.append("Compliance")

    if "finance" in task_lower or "payment" in task_lower or "penalty" in task_lower:
        plan.append("Finance")

    if "legal" in task_lower or "law" in task_lower or "liability" in task_lower:
        plan.append("Legal")

    if "operation" in task_lower or "delivery" in task_lower or "service" in task_lower:
        plan.append("Operations")

    # Default: if no keywords found, run all agents
    if not plan:
        plan = ["Compliance", "Finance", "Legal", "Operations"]

    return plan

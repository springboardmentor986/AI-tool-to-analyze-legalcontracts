def format_agent_output(agent_result):
    domain = agent_result.get("domain", "unknown").upper()
    analysis = agent_result.get("analysis", "")

    return f"""
###  {domain}

{analysis}

---
"""


def format_full_report(agent_results):
    report = "#  Contract Analysis Report\n\n"

    for r in agent_results:
        domain = r.get("domain", "unknown").upper()
        analysis = r.get("analysis", "")

        report += f"##  {domain}\n\n"
        report += analysis + "\n\n---\n\n"

    return report

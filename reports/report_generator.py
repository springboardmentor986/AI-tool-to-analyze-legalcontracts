from pipelines.risk_pipeline import (
    compliance_risk_pipeline,
    finance_risk_pipeline
)
from pipelines.report_pipeline import generate_executive_summary
from multi_turn.agent_interaction import finance_reviews_legal


def generate_report(documents, tone, focus):

    report = f"""
ClauseAI – Contract Intelligence Report
Tone: {tone}
---------------------------------------
"""

    for doc in documents:

        report += f"""
====================================================
DOCUMENT: {doc['name']}
====================================================
"""

        # ---------- EXECUTIVE SUMMARY FIRST ----------
        if "Executive Summary" in focus:
            summary = generate_executive_summary(
                doc["legal"],
                doc["finance"],
                doc["compliance"],
                doc["operations"]
            )

            report += f"""

EXECUTIVE SUMMARY
{summary}
"""

        # ---------- RISK SUMMARY ----------
        if "Risks" in focus:
            compliance_risks = compliance_risk_pipeline(doc["compliance"])
            finance_risks = finance_risk_pipeline(doc["finance"])

            report += f"""

RISK OVERVIEW

Compliance Risks:
{compliance_risks}

Financial Risks:
{finance_risks}
"""

        # ---------- LEGAL ----------
        if "Legal" in focus:
            report += f"""

LEGAL HIGHLIGHTS
{doc['legal']}
"""

        # ---------- FINANCE ----------
        if "Finance" in focus:
            report += f"""

FINANCIAL HIGHLIGHTS
{doc['finance']}
"""

        # ---------- COMPLIANCE ----------
        if "Compliance" in focus:
            report += f"""

COMPLIANCE HIGHLIGHTS
{doc['compliance']}
"""

        # ---------- OPERATIONS ----------
        if "Operations" in focus:
            report += f"""

OPERATIONAL INSIGHTS
{doc['operations']}
"""

        # ---------- CROSS AGENT ----------
        if "Cross-Agent Reasoning" in focus:
            review = finance_reviews_legal(doc["legal"])

            report += f"""

CROSS-DOMAIN RISK ANALYSIS
{review}
"""

    report += "\n---------------------------------------\nEnd of Report\n"

    return report

from __future__ import annotations

from typing import Dict, Any, List
import json

EXPECTED_CLAUSES = [
    "payment_terms",
    "term_and_termination",
    "confidentiality",
    "liability",
    "indemnity",
    "governing_law",
    "deliverables_sla",
    "data_privacy",
    "dispute_resolution",
]


def _risk_from_clause_findings(find: Dict[str, Any]) -> str:
    risks = find.get("risks") or []
    if not isinstance(risks, list):
        return "Medium"
    if len(risks) == 0:
        return "Low"
    if len(risks) >= 3:
        return "High"
    return "Medium"


def _looks_like_json(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return False
    if (t.startswith("{") and t.endswith("}")) or (t.startswith("[") and t.endswith("]")):
        try:
            json.loads(t)
            return True
        except Exception:
            return False
    return False


def build_report_markdown(state: Dict[str, Any]) -> str:
    classification = state.get("classification", {}) or {}
    clauses = state.get("clauses", {}) or {}
    clause_findings = state.get("clause_findings", {}) or {}
    domain_reports = state.get("domain_reports", {}) or {}

    lines: List[str] = []
    lines.append("# Contract Review Report\n")

    # Overview
    lines.append("## Contract Overview")
    lines.append(f"- **Type:** {classification.get('contract_type', 'Unknown')}")
    lines.append(f"- **Parties:** {classification.get('parties', 'Not found')}")
    lines.append(f"- **Effective Date:** {classification.get('effective_date', 'Not found')}")
    lines.append(f"- **Jurisdiction:** {classification.get('jurisdiction', 'Not found')}")
    lines.append("")

    # Key Clause Summary (always print rows)
    lines.append("## Key Clause Summary")
    lines.append("| Clause | Status | Risk | Recommendation |")
    lines.append("|---|---|---|---|")

    for clause in EXPECTED_CLAUSES:
        extracted = ""
        if isinstance(clauses, dict):
            extracted = str(clauses.get(clause, "") or "").strip()

        find_val: Dict[str, Any] = {}
        if isinstance(clause_findings, dict):
            fv = clause_findings.get(clause, {})
            find_val = fv if isinstance(fv, dict) else {"raw": str(fv)}

        if not extracted:
            status = "Not found"
            risk = "High"
            rec = "Add/clarify this clause in the contract before signing."
        else:
            status = "Found"
            risk = _risk_from_clause_findings(find_val) if find_val else "Medium"
            rec = (find_val.get("suggested_revision") or "Review / negotiate").replace("\n", " ").strip()

        lines.append(f"| {clause} | {status} | {risk} | {rec[:180]} |")

    lines.append("")

    # Domain Reviews (NATURAL LANGUAGE ONLY)
    lines.append("## Domain Reviews")
    for domain in ["Compliance", "Finance", "Legal", "Operations"]:
        dr = domain_reports.get(domain, None)
        lines.append(f"### {domain}")

        if not dr:
            lines.append("- No output.\n")
            continue

        # dict output
        if isinstance(dr, dict):
            if dr.get("error"):
                lines.append(f"- **Error:** {dr['error']}\n")
                continue

            summary = str(dr.get("summary") or dr.get("raw") or "").strip()
            if not summary:
                lines.append("- No output.\n")
                continue

            if _looks_like_json(summary):
                lines.append("- Output came as JSON; fix DOMAIN_AGENT_PROMPT (must be natural language).\n")
                continue

            lines.append(summary)
            lines.append("")
            continue

        # string output
        if isinstance(dr, str):
            summary = dr.strip()
            if not summary:
                lines.append("- No output.\n")
                continue

            if _looks_like_json(summary):
                lines.append("- Output came as JSON; fix DOMAIN_AGENT_PROMPT (must be natural language).\n")
                continue

            lines.append(summary)
            lines.append("")
            continue

        lines.append("- No output.\n")

    return "\n".join(lines).strip()

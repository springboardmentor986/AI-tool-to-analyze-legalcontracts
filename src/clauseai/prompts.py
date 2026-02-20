from __future__ import annotations

CLASSIFY_PROMPT = """You are a contract analyst.
Given the contract text, classify the contract type and extract:
- Contract type (e.g., employment, service agreement, NDA, lease, purchase)
- Parties (if visible)
- Effective date (if visible)
- Jurisdiction/governing law (if visible)
Return JSON with keys: contract_type, parties, effective_date, jurisdiction.
"""

CLAUSE_EXTRACT_PROMPT = """You are extracting key clauses from a contract.
From the contract text, pull out the best matching sections for each clause type below.
If not found, return empty string.

Clause types:
- payment_terms
- term_and_termination
- confidentiality
- liability
- indemnity
- governing_law
- deliverables_sla
- data_privacy
- dispute_resolution

Return JSON mapping clause_type -> extracted_text.
"""

CLAUSE_ANALYSIS_PROMPT = """You are a contract clause interpreter.
Analyze the clause text and return JSON:
- summary: plain explanation
- risks: list of risks (short bullets)
- missing_or_ambiguous: list
- suggested_revision: short improved wording or negotiation suggestion
Keep it practical.
"""

PLAN_PROMPT = """You are the coordinator agent.
Using contract classification + clause findings, create a review plan for each domain:
Compliance, Finance, Legal, Operations.
Return JSON mapping domain -> plan bullets.
"""

DOMAIN_AGENT_PROMPT = """You are the {domain} domain contract reviewer.

Write a NATURAL LANGUAGE domain review (NOT JSON).
Use short headings + bullets so it reads clean in a report.

Follow exactly this structure:

Domain Overview:
- 2–4 bullets summarizing what matters in this contract for {domain}

Risk Level:
- Low / Medium / High (one line)
- 1 short reason why

Key Findings:
- 3–6 bullets (specific issues you saw)

Recommendations:
- 3–6 bullets (actionable fixes / negotiation points)

Questions to Clarify:
- 2–5 bullets (questions to ask the counterparty)

Rules:
- Do NOT output JSON.
- Do NOT wrap in code blocks.
- Be specific and avoid generic filler.
"""

FINAL_REPORT_PROMPT = """You are generating the final contract review report.
Create a structured Markdown report with:
1) Executive summary (3-6 bullets)
2) Key clause table (clause -> risk -> recommendation)
3) Domain reviews (Compliance, Finance, Legal, Operations)
4) Top action items (prioritized)
5) Questions to clarify with counterparty
Use the user's tone: {tone}
Focus areas: {focus_areas}
User feedback notes: {feedback}
"""

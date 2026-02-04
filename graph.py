from __future__ import annotations

from typing import TypedDict, Dict, Any, List
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

# ✅ Force load .env from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

from langgraph.graph import StateGraph, END

from .config import settings
from .chunking import chunk_text
from .vectorstore import upsert_contract_chunks, retrieve_relevant
from .prompts import (
    CLASSIFY_PROMPT,
    CLAUSE_EXTRACT_PROMPT,
    CLAUSE_ANALYSIS_PROMPT,
    PLAN_PROMPT,
    FINAL_REPORT_PROMPT,
)
from .agents import run_domain_agent
from .report import build_report_markdown


class ContractState(TypedDict, total=False):
    raw_text: str
    file_type: str
    namespace: str
    tone: str
    focus_areas: List[str]
    feedback: str

    classification: Dict[str, Any]
    clauses: Dict[str, str]
    clause_findings: Dict[str, Any]
    review_plan: Dict[str, Any]
    domain_reports: Dict[str, Any]
    final_report_md: str


def _llm(temp: float = 0.1):
    """✅ Groq-only LLM factory."""
    provider = (os.getenv("LLM_PROVIDER", "groq") or "groq").lower().strip()
    if provider != "groq":
        raise RuntimeError(f"LLM_PROVIDER must be 'groq'. Found: {provider}")

    groq_key = (os.getenv("GROQ_API_KEY", "") or "").strip()
    if not groq_key:
        raise RuntimeError("GROQ_API_KEY missing in .env")

    model = (os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") or "llama-3.3-70b-versatile").strip()

    from langchain_groq import ChatGroq
    return ChatGroq(
        api_key=groq_key,
        model=model,
        temperature=temp,
        timeout=60,
        max_retries=1,
    )


def classify_contract(state: ContractState) -> ContractState:
    llm = _llm()
    msg = llm.invoke([("system", CLASSIFY_PROMPT), ("user", state["raw_text"][:12000])])
    text = (msg.content or "").strip()
    try:
        state["classification"] = json.loads(text)
    except Exception:
        state["classification"] = {"raw": text}
    return state


def retrieve_clauses(state: ContractState) -> ContractState:
    ns = state["namespace"]
    text = state["raw_text"]

    chunks = chunk_text(text)
    upsert_contract_chunks(chunks, namespace=ns, metadata_base={"doc": "contract"})

    llm = _llm()
    relevant = retrieve_relevant(
        query="payment terms fees termination confidentiality liability indemnity governing law dispute resolution data privacy sla deliverables",
        namespace=ns,
        k=int(os.getenv("TOP_K", str(getattr(settings, "top_k", 4)))),
    )
    context = "\n\n---\n\n".join(relevant)[:14000]

    msg = llm.invoke([("system", CLAUSE_EXTRACT_PROMPT), ("user", context)])
    out = (msg.content or "").strip()
    try:
        state["clauses"] = json.loads(out)
    except Exception:
        state["clauses"] = {"raw": out}
    return state


def execute_step_clause(state: ContractState) -> ContractState:
    llm = _llm()
    clauses = state.get("clauses", {})
    findings: Dict[str, Any] = {}

    if "raw" in clauses:
        findings["raw"] = clauses["raw"]
        state["clause_findings"] = findings
        return state

    for clause_name, clause_text in clauses.items():
        clause_text = (clause_text or "").strip()
        if not clause_text:
            findings[clause_name] = {
                "summary": "Not found",
                "risks": [],
                "missing_or_ambiguous": [],
                "suggested_revision": "Add/clarify this clause.",
            }
            continue

        msg = llm.invoke(
            [
                ("system", CLAUSE_ANALYSIS_PROMPT),
                ("user", f"Clause type: {clause_name}\n\nClause text:\n{clause_text[:8000]}"),
            ]
        )
        text_out = (msg.content or "").strip()
        try:
            findings[clause_name] = json.loads(text_out)
        except Exception:
            findings[clause_name] = {"raw": text_out}

    state["clause_findings"] = findings
    return state


def create_review_plan(state: ContractState) -> ContractState:
    llm = _llm()
    payload = {
        "classification": state.get("classification", {}),
        "clause_findings": state.get("clause_findings", {}),
    }
    msg = llm.invoke([("system", PLAN_PROMPT), ("user", json.dumps(payload, ensure_ascii=False)[:14000])])
    text = (msg.content or "").strip()
    try:
        state["review_plan"] = json.loads(text)
    except Exception:
        state["review_plan"] = {"raw": text}
    return state


def execute_step(state: ContractState) -> ContractState:
    focus = state.get("focus_areas") or ["Compliance", "Finance", "Legal", "Operations"]

    context = {
        "classification": state.get("classification", {}),
        "clauses": state.get("clauses", {}),
        "clause_findings": state.get("clause_findings", {}),
        "review_plan": state.get("review_plan", {}),
        "feedback": state.get("feedback", ""),
    }

    reports: Dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=min(len(focus),(os.cpu_count() or 2))) as ex:
        futures = {ex.submit(run_domain_agent, d, context): d for d in focus}
        for fut in as_completed(futures):
            d = futures[fut]
            try:
                reports[d] = fut.result()
            except Exception as e:
                reports[d] = {"domain": d, "error": str(e)}

    state["domain_reports"] = reports
    return state


def generate_final_report(state: ContractState) -> ContractState:
    base_md = build_report_markdown(state)

    llm = _llm(temp=0.2)
    prompt = FINAL_REPORT_PROMPT.format(
        tone=state.get("tone", "Professional"),
        focus_areas=", ".join(state.get("focus_areas") or ["Compliance", "Finance", "Legal", "Operations"]),
        feedback=state.get("feedback", ""),
    )
    msg = llm.invoke([("system", prompt), ("user", base_md[:14000])])
    state["final_report_md"] = (msg.content or "").strip()
    return state


def build_graph():
    g = StateGraph(ContractState)

    g.add_node("classify_contract", classify_contract)
    g.add_node("retrieve_clauses", retrieve_clauses)
    g.add_node("execute_step_clause", execute_step_clause)
    g.add_node("create_review_plan", create_review_plan)
    g.add_node("execute_step", execute_step)
    g.add_node("generate_final_report", generate_final_report)

    g.set_entry_point("classify_contract")
    g.add_edge("classify_contract", "retrieve_clauses")
    g.add_edge("retrieve_clauses", "execute_step_clause")
    g.add_edge("execute_step_clause", "create_review_plan")
    g.add_edge("create_review_plan", "execute_step")
    g.add_edge("execute_step", "generate_final_report")
    g.add_edge("generate_final_report", END)

    return g.compile()

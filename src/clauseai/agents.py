from __future__ import annotations

from typing import Any, Dict
import json
import os
import re

from dotenv import load_dotenv

_AGENT_MEMORY: Dict[str, str] = {}
# Load .env from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

from .config import settings
from .prompts import DOMAIN_AGENT_PROMPT


def _llm(temperature: float = 0.2) -> Any:
    provider = (settings.llm_provider or "groq").lower().strip()

    if provider != "groq":
        raise RuntimeError(f"Only Groq is enabled. LLM_PROVIDER must be 'groq'. Found: {provider}")

    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY missing in .env")

    from langchain_groq import ChatGroq
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=temperature,
        timeout=60,
        max_retries=1,
    )


def _clean_text(t: str) -> str:
    t = (t or "").strip()

    # If model accidentally wraps in ``` blocks, remove them
    t = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", t)
    t = re.sub(r"\s*```$", "", t)

    # Remove leading/trailing quotes if any
    if (t.startswith('"') and t.endswith('"')) or (t.startswith("'") and t.endswith("'")):
        t = t[1:-1].strip()

    # Collapse triple newlines
    while "\n\n\n" in t:
        t = t.replace("\n\n\n", "\n\n")

    return t


def run_domain_agent(domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Runs a single domain agent and returns enhanced natural-language summary."""
    llm = _llm(temperature=0.2)

    previous_summary = _AGENT_MEMORY.get(domain, "")
    context["previous_summary"] = previous_summary

    payload = {"domain": domain, "context": context}

    msg = llm.invoke(
        [
            ("system", DOMAIN_AGENT_PROMPT.format(domain=domain)),
            ("user", json.dumps(payload, ensure_ascii=False)[:9000]),
        ]
    )

    summary = _clean_text(msg.content or "")
    return {"domain": domain, "summary": summary}

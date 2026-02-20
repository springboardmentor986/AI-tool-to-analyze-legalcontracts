from __future__ import annotations
import os
from .config import settings

def get_llm(temperature: float = 0.2):
    provider = (os.getenv("LLM_PROVIDER", "groq") or "groq").lower().strip()

    if provider != "groq":
        raise RuntimeError("Only Groq supported.")

    api_key = settings.groq_api_key
    model = settings.groq_model

    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing.")

    from langchain_groq import ChatGroq

    return ChatGroq(
        api_key=api_key,
        model=model,
        temperature=temperature,
        timeout=60,
        max_retries=1,
    )

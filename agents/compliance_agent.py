from rag.retriever import retrieve_context
from agents.gemini_agent import run_gemini

def compliance_agent(text):
    context = retrieve_context(text)
    prompt = f"""
You are a legal compliance expert.

Document:
{text}

Relevant context:
{context}

Give compliance issues, risks, and suggestions.
"""
    return run_gemini(prompt)

from rag.retriever import retrieve_context
from agents.gemini_agent import run_gemini

def legal_agent(text):
    context = retrieve_context(text)
    prompt = f"""
You are a legal expert.
Analyze the document for legal clauses, obligations, and liabilities.

Document:
{text}

Context:
{context}
"""
    return run_gemini(prompt)

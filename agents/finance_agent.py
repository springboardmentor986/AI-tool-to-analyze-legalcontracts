from rag.retriever import retrieve_context
from agents.gemini_agent import run_gemini


def finance_agent(text: str) -> str:
    """
    Finance Agent
    ----------------
    Analyzes financial risks, penalties, liabilities, and cost implications
    from a legal contract using RAG + LLM.
    """

    # Retrieve relevant chunks from Pinecone
    context = retrieve_context(text)

    # Finance-focused prompt
    prompt = f"""
You are a financial risk analyst specializing in legal contracts.

Your task is to identify:
- Financial risks
- Hidden costs
- Penalties and fines
- Payment obligations
- Liability exposure
- Termination-related costs

Document:
{text}

Relevant Context (from similar clauses):
{context}

Provide a clear, structured financial risk analysis.
"""

    # Run LLM
    return run_gemini(prompt)
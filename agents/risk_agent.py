from rag.retriever import retrieve_context
from agents.gemini_agent import run_gemini


def risk_agent(text: str) -> dict:
    """
    Risk Assessment Agent (Enhanced)

    Outputs:
    - Risk categories
    - Severity levels (Low / Medium / High)
    - Mitigation suggestions
    - Confidence score (0–100)
    """

    # 🔎 Retrieve relevant RAG context from Pinecone
    context = retrieve_context(text)

    # 🧠 Structured expert prompt
    prompt = f"""
You are a senior enterprise risk assessment expert.

Analyze the document and identify risks under the following categories:
1. Operational Risks
2. Legal Risks
3. Compliance Risks
4. Financial Risks
5. Reputational / Strategic Risks

For EACH risk:
- Brief description
- Severity level: Low / Medium / High
- Suggested mitigation

Finally:
- Provide an overall confidence score (0–100) indicating how confident you are
  in this risk assessment based on the document clarity and context quality.

Return the output in clear bullet points.

Document:
{text}

Retrieved Context (from knowledge base):
{context}
"""

    # 🤖 Run LLM
    response = run_gemini(prompt)

    # 📦 Standardized agent output (LangGraph-friendly)
    return {
        "agent": "risk",
        "analysis": response,
        "confidence_score": extract_confidence_score(response),
        "severity_summary": extract_severity_levels(response)
    }


# --------------------------------------------------
# 🔧 Helper functions (UI + Graph friendly)
# --------------------------------------------------

def extract_confidence_score(text: str) -> int:
    """
    Attempts to extract a confidence score from model output.
    Fallbacks safely if not found.
    """
    import re
    match = re.search(r'(\b\d{1,3}\b)\s*/\s*100|\b(\d{1,3})\b%', text)
    if match:
        score = int(match.group(1) or match.group(2))
        return min(max(score, 0), 100)
    return 75  # safe default


def extract_severity_levels(text: str) -> dict:
    """
    Counts severity mentions for UI / analytics.
    """
    text_lower = text.lower()
    return {
        "high": text_lower.count("high"),
        "medium": text_lower.count("medium"),
        "low": text_lower.count("low")
    }

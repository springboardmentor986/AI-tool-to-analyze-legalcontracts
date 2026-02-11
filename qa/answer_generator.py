import os
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, retrieved_clauses):
    """
    Generates answer using retrieved clauses as context (RAG).
    Uses Groq instead of Gemini.
    """
    if not retrieved_clauses:
        return "No relevant clauses found to answer this question."

    # Build context from retrieved clauses
    context = "\n".join(
        f"- [{c.get('clause_type', '?')}] ({c.get('risk_level', '?')}): {c.get('summary', '?')}"
        for c in retrieved_clauses
    )

    prompt = f"""
You are a legal contract assistant. Answer the question using ONLY the context below.
Do not guess or make up information. If the answer is not in the context, say so.

Context (retrieved clauses):
{context}

Question: {question}

Answer:
"""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating answer: {e}"

from embeddings.pinecone_client import retrieve_context_by_vector

from app.llm import get_llm

llm = get_llm()


def answer_question(question: str, namespace: str):

    # Retrieve relevant chunks
    context_chunks = retrieve_context(
        query=question,
        namespace=namespace,
        top_k=5
    )

    if not context_chunks:
        return {
            "answer": "No relevant information found in this contract.",
            "context": ""
        }

    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a legal contract assistant.

Rules:
1. Answer ONLY from the provided contract context.
2. Do NOT use outside knowledge.
3. If answer is not found, say:
   "Not mentioned in contract."
4. Be professional and concise.

Contract Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "context": context
    }

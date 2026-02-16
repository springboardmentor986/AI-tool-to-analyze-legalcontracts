from config.llm_config import get_llm

llm = get_llm()


def chat_with_contract(context: str, question: str) -> str:
    """
    Improved Contract Q&A Assistant

    - Uses ONLY analyzed agent outputs
    - Allows semantic understanding (not strict keyword match)
    - Still prevents hallucinations
    - Low token optimized
    """

    prompt = f"""
You are a contract analysis assistant.

Answer the question using ONLY the provided contract insights.
If relevant information exists, explain clearly.
If no related information exists at all, reply exactly:
Not found in analyzed contract.

Contract Insights:
{context}

Question:
{question}

Answer in clear professional language.
"""
    
    response = llm.invoke(prompt).content.strip()
    return response

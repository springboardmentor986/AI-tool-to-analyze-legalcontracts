from config.llm_config import get_llm

llm = get_llm()


def chat_with_contract(context: str, question: str) -> str:
    """
    AI Assistant for Contract Q&A (Low-token optimized)

    - Uses ONLY pre-analyzed agent outputs
    - No re-analysis of contract text
    - Strict grounding to avoid hallucinations
    """

    prompt = f"""
Answer the question using ONLY the information below.
If the answer is not present, reply exactly:
"Not found in analyzed contract."

INFO:
{context}

Q: {question}
A:
"""
    return llm.invoke(prompt).content

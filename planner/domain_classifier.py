from app.llm import get_llm

llm = get_llm()

def classify_domains(text: str) -> list[str]:
    prompt = f"""
    Identify relevant domains from:
    legal, finance, compliance, operations

    Return comma-separated values only.

    Contract:
    {text}
    """
    response = llm.invoke(prompt).content.lower()
    return [d.strip() for d in response.split(",")]

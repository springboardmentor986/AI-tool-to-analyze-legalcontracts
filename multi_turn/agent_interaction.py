from config.llm_config import get_llm

llm = get_llm()


def finance_reviews_legal(legal_output):
    prompt = f"""
You are a finance analyst.

Step 1: Read the legal analysis below.
Step 2: Identify any financial exposure, penalties, payment risks, or cost impact.
Step 3: Explain how legal clauses translate into financial risk.

Legal Analysis:
{legal_output}

Return bullet points only.
"""
    return llm.invoke(prompt).content

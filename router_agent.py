import os
from config.settings import settings
from langchain_groq import ChatGroq

# 1.Groq API Key  👇🏼
os.environ["GROQ_KEY"] = settings.GROQ_KEY

# 2. AI ka "Dimaag" setup ho raha hai
# Hum Llama 3 use kar rahe hain jo ki free aur fast hai

# 2. llm banate waqt api_key pass 
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile", 
    temperature=0,
    api_key=settings.GROQ_KEY  # Ye sabse zaroori hai!
)

def classify_contract(text_snippet):
    #  main kaam: Decision Making
    system_prompt = "Aap ek expert Contract Classifier hain. Sirf ek word mein batayein ki ye contract kis domain ka hai (e.g., Employment, Real Estate, Finance, ya Legal)."
    
    # AI se sawal puchna
    response = llm.invoke(f"{system_prompt}\n\nContract Text: {text_snippet}")
    return response.content

def assign_expert(domain):
    #  Planning Logic
    mapping = {
        "Real Estate": "Operations aur Legal Agent ko bhejo.",
        "Employment": "Compliance aur Legal Agent ko bhejo.",
        "Finance": "Finance aur Compliance Agent ko bhejo.",
    }

    # Agar domain unknown hai toh default expert
    return mapping.get(domain, "Legal Agent ko bhejo (Default).")

    
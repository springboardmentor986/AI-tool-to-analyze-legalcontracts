from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",  # ✅ Groq CURRENT Model
        temperature=0
    )

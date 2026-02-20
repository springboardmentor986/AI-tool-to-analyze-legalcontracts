from langchain_groq import ChatGroq
from modules.config import GROQ_API_KEY

def create_agent():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0
    )
    return llm

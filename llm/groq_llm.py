 
from langchain_groq import ChatGroq
import os

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",  # or any Groq-supported model
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

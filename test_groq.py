import os
from langchain_groq import ChatGroq

API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=API_KEY,
    model="llama-3.1-8b-instant",  # ✅ supported
    temperature=0
)

response = llm.invoke("Hello! Can you respond to this test message?")
print("✅ Groq API works!\n")
print(response.content)

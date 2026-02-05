from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()  # ⭐ THIS IS REQUIRED

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

print(llm.invoke("Say hello in one sentence").content)

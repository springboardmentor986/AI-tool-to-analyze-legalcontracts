import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_gemini(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ FIXED MODEL
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return completion.choices[0].message.content

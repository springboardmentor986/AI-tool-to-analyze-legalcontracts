import os
import time
from groq import Groq
from dotenv import load_dotenv

# ================= LOAD ENV =================
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================= MODELS =================
PRIMARY_MODEL = "llama-3.1-8b-instant"
FALLBACK_MODEL = "llama3-8b-8192"

# ================= LLM CALL =================
def run_gemini(prompt: str) -> str:
    """
    Lightweight LLM call with:
    - rate limit handling
    - overload (503) handling
    - model fallback
    - exponential backoff
    """

    for attempt in range(3):  # max 3 attempts
        try:
            completion = client.chat.completions.create(
                model=PRIMARY_MODEL if attempt < 2 else FALLBACK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are ClauseAI, a professional legal contract assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=350
            )

            return completion.choices[0].message.content

        except Exception as e:
            error_msg = str(e).lower()

            # ⏳ Rate limit / overload → retry
            if any(x in error_msg for x in ["429", "rate limit", "503", "over capacity"]):
                time.sleep(2 ** attempt)  # exponential backoff
                continue

            # ❌ Unknown error → stop
            return "⚠️ ClauseAI encountered a temporary issue. Please try again."

    # ❌ All retries failed
    return "⏳ ClauseAI is busy right now. Please try again in a minute."
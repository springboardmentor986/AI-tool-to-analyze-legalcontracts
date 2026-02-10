from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, LLM_TEMPERATURE
import time
import random
from google.api_core import exceptions


# -------------------------------------------------
# CLIENT INITIALIZATION
# -------------------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------------------------------
# PUBLIC FUNCTION
# -------------------------------------------------

def call_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns response text.
    """

    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": LLM_TEMPERATURE
                }
            )
            
            if response and hasattr(response, "text"):
                return response.text.strip()
                
            return ""

        except exceptions.ResourceExhausted:
            if attempt < max_retries - 1:
                sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
                continue
            else:
                return "Error: Quota exceeded. Please try again later."
                

        except Exception as e:
            return f"Error: {str(e)}"


# Circuit breaker for embedding API
_EMBEDDING_API_ACTIVE = True

def get_embedding(text: str) -> list:
    """
    Generates embedding for the given text using Gemini.
    """
    global _EMBEDDING_API_ACTIVE
    
    if _EMBEDDING_API_ACTIVE:
        try:
            response = client.models.embed_content(
                model="models/embedding-001",
                contents=text
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"[WARNING] Embedding API failed: {e}. Disabling API for future calls and using mock.")
            _EMBEDDING_API_ACTIVE = False
            
    # Fallback: Deterministic mock embedding (size 1024)
    # This runs if API is inactive or just failed
    random.seed(len(text)) 
    return [random.uniform(-0.1, 0.1) for _ in range(1024)]




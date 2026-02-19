from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, LLM_TEMPERATURE
import time
import random
from google.api_core import exceptions
import logging

# Suppress Google GenAI INFO logs (like AFC enabled)
logging.getLogger("google_genai").setLevel(logging.WARNING)


# -------------------------------------------------
# CLIENT INITIALIZATION
# -------------------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------------------------------
# PUBLIC FUNCTION
# -------------------------------------------------

from llm.openrouter import call_openrouter_deepseek

def call_gemini(prompt: str) -> str:
    """
    Orchestrates LLM calls with Primary (DeepSeek) -> Fallback (Gemini) strategy.
    Renamed internally but keeping function signature compatible.
    """
    # 1. Try Primary: DeepSeek R1 (Free)
    try:
        # print("Attempting DeepSeek R1...") 
        response = call_openrouter_deepseek(prompt)
        return response
    except Exception as e:
        # Log failure and proceed to fallback
        print(f"DeepSeek Failed ({e}). Falling back to Gemini...")
        
    # 2. Fallback: Gemini 1.5 Pro/Flash
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
                # UI Feedback (Point 17/24)
                import streamlit as st
                st.toast(f"⏳ Gemini Rate limit hit. Retrying in {sleep_time:.1f}s...", icon="⚠️")
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
                model="models/gemini-embedding-001",
                contents=text
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"[WARNING] Embedding API failed: {e}. Disabling API for future calls and using mock.")
            _EMBEDDING_API_ACTIVE = False
            
    # Fallback: Deterministic mock embedding (size 1024)
    # This runs if API is inactive or just failed
    random.seed(len(text)) 
    return [random.uniform(-0.1, 0.1) for _ in range(3072)]




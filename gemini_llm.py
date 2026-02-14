# gemini_llm.py
import os
from google import genai

# Read API key from environment variable
API_KEY = os.getenv("AIzaSyDoKvwOMx7yU2J-Oa744lQQDvfHdZARg4E")

client = genai.Client(api_key=API_KEY)

def embed_text(text: str):
    """
    Generate embeddings for given text using Gemini
    """
    response = client.models.embed_content(
        model="text-embedding-004",
        content=text
    )
    return response["embedding"]

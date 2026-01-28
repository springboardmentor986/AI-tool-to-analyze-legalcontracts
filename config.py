import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("gemini_api_key")
PINECONE_API_KEY = os.getenv("pinecone_clause_api")
INDEX_NAME = "clauseai-index"

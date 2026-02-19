from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

#llm details
GEMINI_MODEL_NAME = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2

# OpenRouter / DeepSeek
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL_NAME = "deepseek/deepseek-r1-0528:free" 

AGENT_OBJECTIVES = {
    "compliance": "Identify regulatory and compliance obligations.",
    "finance": "Analyze payment terms, penalties, and financial risks.",
    "legal": "Identify termination clauses, liabilities, and legal risks.",
    "operations": "Identify operational responsibilities and constraints."
}

#chunking
CHUNK_SIZE = 1000

# Pinecone settings
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "clauseai-index-v3")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
TOP_K_RESULTS = 5

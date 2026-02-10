from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

#llm details
GEMINI_MODEL_NAME = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2

AGENT_OBJECTIVES = {
    "compliance": "Identify regulatory and compliance obligations.",
    "finance": "Analyze payment terms, penalties, and financial risks.",
    "legal": "Identify termination clauses, liabilities, and legal risks.",
    "operations": "Identify operational responsibilities and constraints."
}

#chunking
CHUNK_SIZE = 1000

# Pinecone settings
PINECONE_INDEX_NAME = "clauseai-index"
PINECONE_CLOUD = "aws"
PINECONE_REGION = "us-east-1"
TOP_K_RESULTS = 5

import os
from dotenv import load_dotenv
# config.py
from utils.universal_llm import universal_llm
load_dotenv()
# This 'llm' variable is now your "Failover System"
llm = universal_llm
PINECONE_API_KEY = os.getenv("pinecone_clause_api")
INDEX_NAME = "clauseai-index"
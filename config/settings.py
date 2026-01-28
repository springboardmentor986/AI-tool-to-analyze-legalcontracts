import os
from dotenv import load_dotenv

# .env file se keys load karne ke liye
load_dotenv()

class Settings:
    GROQ_KEY = os.getenv("GROQ_KEY")
    PINECONE_KEY = os.getenv("PINECONE_KEY")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# object 
settings = Settings()
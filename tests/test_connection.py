import os
from pinecone import Pinecone
from config.settings import settings

# check the connection of pinecone
try:
    pc = Pinecone(api_key=settings.PINECONE_KEY)
    
    if settings.PINECONE_INDEX in pc.list_indexes().names():
        print(f"✅ Connection OK: {settings.PINECONE_INDEX} is ready!")
    else:
        print("❌ Index missing! Please check Pinecone dashboard.")

except Exception as e:
    print(f"Bhai, connectivity issue: {e}")
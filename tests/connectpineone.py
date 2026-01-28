from pinecone import Pinecone
from config.settings import settings

# 1. Pinecone Api Key Ko Yaha Likhna Hai
try:
    # Connection banana
    pc = Pinecone(api_key=settings.PINECONE_KEY)
    indexes = pc.list_indexes()
    
    if not indexes:
        print("Connection OK, INDEX NOT FOUND!")
    else:
        for index in indexes:
            print(f"📁 Active Index: {index.name}")
            
except Exception as e:
    print(f"Connection Error: {e}")
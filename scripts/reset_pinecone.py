import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "clauseai-index"

if INDEX_NAME in pc.list_indexes().names():
    pc.delete_index(INDEX_NAME)
    print(f"Deleted index: {INDEX_NAME}")
else:
    print("Index not found, nothing to delete")

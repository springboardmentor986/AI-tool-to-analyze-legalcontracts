from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv(override=True)

key = os.getenv("PINECONE_API_KEY")
print("Key starts with:", key[:10])

pc = Pinecone(api_key=key)
print(pc.list_indexes())

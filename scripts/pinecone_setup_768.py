import os
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone, ServerlessSpec

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX", "clauseai-gemini")

pc = Pinecone(api_key=api_key)

names = [i["name"] for i in pc.list_indexes()]
print("Existing:", names)

if index_name not in names:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print("✅ Created", index_name)
else:
    print("✅ Index already exists:", index_name)

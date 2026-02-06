from pinecone import Pinecone, ServerlessSpec
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "clauseai-index"

pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,   # ✅ MUST MATCH MiniLM
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"  # free-tier safe
        )
    )

index = pc.Index(INDEX_NAME)

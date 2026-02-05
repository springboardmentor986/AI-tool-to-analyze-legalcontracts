import os
from pinecone import Pinecone, ServerlessSpec

# Make sure your API key is in your environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not set in environment variables")

# Create Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# List existing indexes
indexes = pc.list_indexes().names()
print("Existing indexes:", indexes)
 
# Create an index if it doesn't exist
index_name = "my-index"  # lowercase letters and hyphen only
if index_name not in indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )
    print(f"Created index: {index_name}")

# Access the index
index = pc.Index(index_name)

# Test upsert
vector = [0.1] * 1536
index.upsert(items=[("vec1", vector)])

# Test query
result = index.query(queries=[[0.1]*1536], top_k=1)
print("Query result:", result)

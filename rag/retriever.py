import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# ENV
# --------------------------------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found")

# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------
MODEL_NAME = "all-MiniLM-L6-v2"
DIMENSION = 384
model = SentenceTransformer(MODEL_NAME)

# --------------------------------------------------
# PINECONE
# --------------------------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "clauseai-index"

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)

# --------------------------------------------------
# STORE TEXT
# --------------------------------------------------
def store_text(text: str):
    chunks = [text[i:i + 500] for i in range(0, len(text), 500)]

    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk)

        vectors.append((
            f"chunk-{i}",
            embedding.tolist(),
            {"text": chunk}
        ))

    index.upsert(vectors)

# --------------------------------------------------
# RETRIEVE CONTEXT (TOP-K LIVES HERE)
# --------------------------------------------------
def retrieve_context(query: str, top_k: int = 3):
    query_embedding = model.encode(query)

    res = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    chunks = [m["metadata"]["text"] for m in res["matches"]]

    return {
        "context": " ".join(chunks),
        "chunks": chunks
    }
import os
import uuid
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# ---------------- Pinecone Init ----------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "contract-ai"

# Create index if not exists
existing_indexes = [idx["name"] for idx in pc.list_indexes()]

if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # all-MiniLM-L6-v2 embedding size
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(INDEX_NAME)

# ---------------- Embedding Model ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- Store Function ----------------
def store_result(text: str, metadata: dict):
    """
    Stores text embeddings in Pinecone with safe unique IDs.
    Metadata example:
    {
        "agent": "legal",
        "document": "contract1.pdf"
    }
    """

    vector = model.encode(text).tolist()

    vector_id = str(uuid.uuid4())  # ✅ stable + unique

    index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": vector,
                "metadata": metadata
            }
        ]
    )

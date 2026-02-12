import os
from dotenv import load_dotenv
from pinecone import Pinecone
from embeddings.embedder import get_embedding_model

# ---------------- ENV SETUP ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY not found")

if not PINECONE_INDEX:
    raise RuntimeError("PINECONE_INDEX not found")

# ---------------- PINECONE INIT ----------------

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

embedder = get_embedding_model()

# =====================================================
#               UPSERT CHUNKS
# =====================================================

def upsert_chunks(chunks, namespace: str):
    """
    Stores contract chunks into Pinecone under a namespace.
    Namespace = unique contract ID
    """

    vectors = embedder.embed_documents(chunks)

    data = []

    for i in range(len(chunks)):
        item = (
            f"{namespace}-chunk-{i}",   # unique ID
            vectors[i],
            {"text": chunks[i]}
        )
        data.append(item)

    if data:
        index.upsert(
            vectors=data,
            namespace=namespace   # IMPORTANT
        )


# =====================================================
#               RETRIEVE CONTEXT (WITH NAMESPACE)
# =====================================================

def retrieve_context_by_vector(vector, namespace: str, top_k: int = 3):
    """
    Retrieve context using precomputed embedding
    """

    response = index.query(
        vector=vector,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True
    )

    context = []

    for match in response["matches"]:
        if "metadata" in match and "text" in match["metadata"]:
            context.append(match["metadata"]["text"])

    return context


# =====================================================
# FLOW OF SYSTEM
# =====================================================

"""
DOCUMENT TEXT
     ↓
Text Chunks
     ↓
Embeddings (Vectors)
     ↓
Pinecone (Store under Namespace)
     ↓
User Query
     ↓
Query Vector
     ↓
Pinecone Search (inside Namespace)
     ↓
Relevant Text (Context)
"""

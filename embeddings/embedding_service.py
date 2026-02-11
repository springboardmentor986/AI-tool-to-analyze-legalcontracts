from sentence_transformers import SentenceTransformer

# Load model once at startup (not on every call)
_model = SentenceTransformer("all-mpnet-base-v2")  # produces 768-dim vectors

def generate_embedding(text: str):
    """
    Generates embedding vector locally using sentence-transformers.
    No API call. No quota. Matches Pinecone index dimension (768).
    """
    return _model.encode(text).tolist()
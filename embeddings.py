 
from sentence_transformers import SentenceTransformer

# Load model once globally (fast + memory efficient)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    Generate embedding vector for given text.
    """
    embedding = model.encode(text)

    return embedding.tolist()

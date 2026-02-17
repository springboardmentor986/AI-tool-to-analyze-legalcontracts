from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("clauseai")

def store_risks(risks):
    vectors = []
    for i, risk in enumerate(risks):
        vectors.append((
            f"risk-{i}",
            [0.01] * 384,
            risk
        ))
    index.upsert(vectors)
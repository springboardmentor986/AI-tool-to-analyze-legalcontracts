from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("clauseai")

index.upsert([
    ("test1", [0.01] * 384, {"text": "Payment must be completed within 30 days"})
])

res = index.query(vector=[0.01] * 384, top_k=1)

print("Pinecone connection successful")
print(res)

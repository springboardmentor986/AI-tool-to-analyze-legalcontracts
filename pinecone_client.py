from pinecone import Pinecone as PC
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("pcsk_3ssktE_HpETtLXf9MPe8e8fhYRm8kUCmySywXfjopEpWQzxAfpig1B9GyXRZsyZeJjjGBy"))

index_name = os.getenv("clauseai")

if index_name not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine"
    )

print("Pinecone index ready")

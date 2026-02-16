"""
Vector Store Module for ClauseAI
Compatible with Pinecone v3+
"""

from pinecone import Pinecone, ServerlessSpec
import os
import uuid
import time
from typing import List

INDEX_NAME = "clauseai-contracts"

pc = None
index = None


def initialize_pinecone():
    global pc, index

    try:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not set")

        pc = Pinecone(api_key=api_key)

        existing_indexes = pc.list_indexes().names()

        if INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=INDEX_NAME,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

            while not pc.describe_index(INDEX_NAME).status["ready"]:
                time.sleep(1)

        index = pc.Index(INDEX_NAME)
        return True

    except Exception as e:
        print(f"Initialization error: {e}")
        return False


def store_chunks_in_vector_store(
    chunks: List[str],
    embeddings: List[List[float]],
    contract_id: str,
    filename: str
):
    global index

    if index is None:
        initialize_pinecone()

    vectors = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {
                "text": chunk,
                "chunk_index": i,
                "contract_id": contract_id,
                "filename": filename
            }
        })

    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i+batch_size])


def query_index(query_embedding, top_k=5, contract_id=None):
    global index

    if index is None:
        initialize_pinecone()

    filter_dict = None
    if contract_id:
        filter_dict = {"contract_id": {"$eq": contract_id}}

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_dict
    )

    formatted_results = []

    for match in results.matches:
        formatted_results.append({
            "id": match.id,
            "score": match.score,
            "text": match.metadata.get("text", ""),
            "metadata": match.metadata
        })

    return formatted_results

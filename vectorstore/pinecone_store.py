import os
from pinecone import Pinecone

# --------------------------------------------------
# Initialize Pinecone
# --------------------------------------------------
def init_pinecone():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME")

    existing_indexes = [idx["name"] for idx in pc.list_indexes()]
    if index_name not in existing_indexes:
        raise ValueError(f"Pinecone index '{index_name}' does not exist")

    return pc.Index(index_name)


# --------------------------------------------------
# Store clause vectors
# --------------------------------------------------
def store_clause_vectors(index, contract_id, agent, clauses):
    vectors = []

    for i, clause in enumerate(clauses):
        if "embedding" not in clause:
            continue

        vectors.append({
            "id": f"{contract_id}-{agent}-{i}",
            "values": clause["embedding"],
            "metadata": {
                "contract_id": contract_id,
                "agent": agent,
                "clause_type": clause["clause_type"],
                "risk_level": clause["risk_level"],
                "summary": clause["summary"],
                "recommendation": clause["recommendation"]
            }
        })

    if vectors:
        index.upsert(vectors=vectors)


# --------------------------------------------------
# Query clause vectors
# --------------------------------------------------
def query_clause_vectors(index, query_embedding, top_k=5, filters=None):
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filters
    )

    return [match["metadata"] for match in response.get("matches", [])]

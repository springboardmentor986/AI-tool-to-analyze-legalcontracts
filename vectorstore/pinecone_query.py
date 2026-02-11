import os
from pinecone import Pinecone
from embeddings.embedding_service import generate_embedding

# --------------------------------------------------
# Initialize Pinecone client
# --------------------------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# --------------------------------------------------
# Query Pinecone for relevant clauses
# --------------------------------------------------
def query_contract_clauses(user_question, top_k=5):
    """
    Given a user question, retrieve the most relevant
    contract clauses from Pinecone.
    """

    # 1️⃣ Convert question to embedding
    query_embedding = generate_embedding(user_question)

    # 2️⃣ Query Pinecone
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # 3️⃣ Extract clause text + metadata
    retrieved_clauses = []

    for match in result["matches"]:
        metadata = match.get("metadata", {})
        retrieved_clauses.append({
            "agent": metadata.get("agent"),
            "clause_type": metadata.get("clause_type"),
            "risk_level": metadata.get("risk_level"),
            "summary": metadata.get("summary"),
            "recommendation": metadata.get("recommendation"),
            "score": match.get("score")
        })

    return retrieved_clauses
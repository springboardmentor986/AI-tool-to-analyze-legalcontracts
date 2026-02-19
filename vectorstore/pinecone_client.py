from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_CLOUD, PINECONE_REGION
from llm.gemini import get_embedding
import uuid
import hashlib

class PineconeClient:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME
        
        # Check if index exists, if not create it
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            try:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=3072, # Dimension for gemini-embedding-001 (verified 3072)
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud=PINECONE_CLOUD,
                        region=PINECONE_REGION
                    )
                )
            except Exception as e:
                print(f"Index creation failed (might already exist or permission error): {e}")

        self.index = self.pc.Index(self.index_name)

    def upsert_chunks(self, chunks: list[dict]):
        """
        Embeds and upserts chunks to Pinecone.
        Args:
            chunks: List of dictionaries with 'text', 'source', 'page'
        """
        vectors = []
        for i, chunk_data in enumerate(chunks):
            text = chunk_data.get("text", "")
            if not text:
                continue
                
            embedding = get_embedding(text)
            if not embedding:
                continue
                
            # Use hash for deterministic ID
            chunk_id = hashlib.md5(text.encode('utf-8')).hexdigest()
            
            # Combine all metadata
            metadata = {
                "text": text,
                "chunk_index": i,
                "source": chunk_data.get("source", "unknown"),
                "page": chunk_data.get("page", 0)
            }
            
            vectors.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": metadata
            })
            
        if vectors:
            # Upsert in batches of 100 to avoid limits
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)

    def query_relevant_chunks(self, query: str, top_k: int = 5) -> list[str]:
        """
        Retrieves relevant chunks for a given query.
        Returns list of text strings.
        """
        embedding = get_embedding(query)
        if not embedding:
            return []

        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )

        matches = results.get("matches", [])
        # Return full metadata for citation support
        return [
            {
                "text": match["metadata"].get("text", ""),
                "page": match["metadata"].get("page", 0),
                "source": match["metadata"].get("source", "unknown")
            }
            for match in matches if "metadata" in match
        ]

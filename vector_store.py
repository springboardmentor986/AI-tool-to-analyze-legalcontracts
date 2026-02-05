"""
Vector Store Module for ClauseAI
Handles Pinecone vector database operations
Compatible with Pinecone v3.0+
"""

from pinecone import Pinecone, ServerlessSpec
import os
from typing import List, Dict
import uuid
import time

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "your-api-key-here")
INDEX_NAME = "clauseai-contracts"

# Global Pinecone client and index
pc = None
index = None


def initialize_pinecone():
    """Initialize Pinecone connection and create index if needed"""
    global pc, index
    
    try:
        # Initialize Pinecone client (v3.0+ syntax)
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Get list of existing indexes
        existing_indexes = pc.list_indexes().names()
        
        # Create index if it doesn't exist
        if INDEX_NAME not in existing_indexes:
            print(f"Creating new index: {INDEX_NAME}...")
            pc.create_index(
                name=INDEX_NAME,
                dimension=384,  # for all-MiniLM-L6-v2 model
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            print(f"✅ Created new index: {INDEX_NAME}")
            
            # Wait for index to be ready
            print("⏳ Waiting for index to be ready...")
            while not pc.describe_index(INDEX_NAME).status['ready']:
                time.sleep(1)
            print("✅ Index is ready!")
        
        # Connect to the index
        index = pc.Index(INDEX_NAME)
        print(f"✅ Connected to index: {INDEX_NAME}")
        
        # Get index stats
        stats = index.describe_index_stats()
        print(f"📊 Index stats: {stats.total_vector_count} vectors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing Pinecone: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def store_chunks_in_vector_store(chunks: List[str], embeddings: List[List[float]], metadata: Dict = None):
    """
    Store document chunks with their embeddings in Pinecone
    
    Args:
        chunks: List of text chunks
        embeddings: List of embedding vectors
        metadata: Optional metadata to attach to all chunks
    """
    global index
    
    if index is None:
        if not initialize_pinecone():
            raise Exception("Failed to initialize Pinecone. Please check your API key.")
    
    try:
        # Prepare vectors for upsert
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = str(uuid.uuid4())
            
            # Combine chunk-specific metadata with global metadata
            chunk_metadata = {
                "text": chunk,
                "chunk_index": i,
                **(metadata or {})
            }
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": chunk_metadata
            })
        
        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch)
            print(f"📤 Uploaded batch {i//batch_size + 1}/{(len(vectors)-1)//batch_size + 1}")
        
        print(f"✅ Successfully stored {len(chunks)} chunks in Pinecone")
        
    except Exception as e:
        print(f"❌ Error storing vectors: {str(e)}")
        raise


def query_index(query_embedding: List[float], top_k: int = 5, filter_dict: Dict = None):
    """
    Query the Pinecone index for similar chunks
    
    Args:
        query_embedding: Query vector
        top_k: Number of results to return
        filter_dict: Optional metadata filter
    
    Returns:
        List of matched results with scores and metadata
    """
    global index
    
    if index is None:
        if not initialize_pinecone():
            raise Exception("Failed to initialize Pinecone. Please check your API key.")
    
    try:
        # Query Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        # Format results
        formatted_results = []
        for match in results.matches:
            formatted_results.append({
                "id": match.id,
                "score": match.score,
                "text": match.metadata.get("text", ""),
                "metadata": match.metadata
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"❌ Error querying index: {str(e)}")
        raise


def delete_all_vectors():
    """Delete all vectors from the index (use with caution!)"""
    global index
    
    if index is None:
        if not initialize_pinecone():
            raise Exception("Failed to initialize Pinecone")
    
    try:
        index.delete(delete_all=True)
        print("✅ Deleted all vectors from index")
    except Exception as e:
        print(f"❌ Error deleting vectors: {str(e)}")
        raise


def get_index_stats():
    """Get statistics about the current index"""
    global index
    
    if index is None:
        if not initialize_pinecone():
            raise Exception("Failed to initialize Pinecone")
    
    try:
        stats = index.describe_index_stats()
        return {
            "total_vectors": stats.total_vector_count,
            "dimension": stats.dimension,
            "index_fullness": stats.index_fullness
        }
    except Exception as e:
        print(f"❌ Error getting stats: {str(e)}")
        raise
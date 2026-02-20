from __future__ import annotations
import time

from typing import List, Dict, Any

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from .config import settings
from .embeddings import get_embeddings


def _pinecone_client() -> Pinecone:
    if not settings.pinecone_api_key:
        raise RuntimeError("PINECONE_API_KEY missing in .env")
    return Pinecone(api_key=settings.pinecone_api_key)


def _vectorstore(namespace: str) -> PineconeVectorStore:
    embeddings = get_embeddings()
    pc = _pinecone_client()

    # Prefer host-based connection if provided
    if settings.pinecone_host:
        index = pc.Index(host=settings.pinecone_host)
        return PineconeVectorStore(index=index, embedding=embeddings, namespace=namespace)

    # Otherwise connect by index name
    return PineconeVectorStore(index_name=settings.pinecone_index, embedding=embeddings, namespace=namespace)


def upsert_contract_chunks(chunks: List[str], namespace: str, metadata_base: Dict[str, Any] | None = None) -> int:
    """
    Upsert text chunks into Pinecone under a namespace.
    """
    if not chunks:
        return 0

    vs = _vectorstore(namespace)
    base = metadata_base or {}

    meta_base = metadata_base or {}
    metadatas = [
        {**meta_base, "chunk_index": i, "type": "contract_chunk", "timestamp": time.time(), "domain": meta_base.get("domain","general")}
        for i in range(len(chunks))
    ]
    vs.add_texts(texts=chunks, metadatas=metadatas)
    return len(chunks)


def retrieve_relevant(query: str, namespace: str, k: int) -> List[str]:
    """
    Retrieve top-k similar chunks from Pinecone for a given query.
    """
    vs = _vectorstore(namespace)
    docs = vs.similarity_search(query, k=k)
    return [d.page_content for d in docs]

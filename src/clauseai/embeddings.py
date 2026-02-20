from __future__ import annotations

import os
from dotenv import load_dotenv

# ✅ Force load .env from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

from langchain_huggingface import HuggingFaceEmbeddings



def get_embeddings():
    """
    ✅ Local embeddings only (no OpenAI, no Gemini).
    Pinecone needs embeddings for vectors; Groq is only for LLM generation.
    """
    provider = (os.getenv("EMBEDDING_PROVIDER", "local") or "local").lower().strip()
    if provider != "local":
        raise RuntimeError(
            f"Only local embeddings are enabled. Set EMBEDDING_PROVIDER=local. Found: {provider}"
        )

    model_name = (os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2") or "").strip()
    if not model_name:
        model_name = "sentence-transformers/all-MiniLM-L6-v2"

    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True},
    )

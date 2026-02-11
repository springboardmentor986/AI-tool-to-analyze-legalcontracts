from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# ✅ Force load .env from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)


@dataclass(frozen=True)
class Settings:
    # ---- Providers ----
    llm_provider: str = (os.getenv("LLM_PROVIDER", "groq") or "groq").strip().lower()
    embedding_provider: str = (os.getenv("EMBEDDING_PROVIDER", "local") or "local").strip().lower()

    # ---- Groq ----
    groq_api_key: str = (os.getenv("GROQ_API_KEY", "") or "").strip()
    groq_model: str = (os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") or "llama-3.3-70b-versatile").strip()

    # ---- Pinecone ----
    pinecone_api_key: str = (os.getenv("PINECONE_API_KEY", "") or "").strip()
    pinecone_index: str = (os.getenv("PINECONE_INDEX", "") or "").strip()
    pinecone_host: str = (os.getenv("PINECONE_HOST", "") or "").strip()

    # ---- Chunking / retrieval ----
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    top_k: int = int(os.getenv("TOP_K", "4"))


settings = Settings()

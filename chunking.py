from __future__ import annotations
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import settings

def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_text(text)
    # keep MVP fast
    return chunks[:25]

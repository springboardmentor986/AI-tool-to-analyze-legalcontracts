from typing import List, Dict

def chunk_text(
    extracted_data: List[Dict],
    chunk_size: int = 1000,
    overlap: int = 100
) -> List[Dict]:
    """
    Splits contract text into overlapping chunks, preserving metadata.

    Args:
        extracted_data (List[Dict]): List of dicts with keys 'text', 'source', 'page'
        chunk_size (int): Number of words per chunk
        overlap (int): Number of words to overlap

    Returns:
        List[Dict]: List of chunks with metadata
    """

    if not extracted_data:
        return []

    chunks_with_metadata = []

    for item in extracted_data:
        text = item.get("text", "")
        metadata = {
            "source": item.get("source", "unknown"),
            "page": item.get("page", 0)
        }

        if not text or not text.strip():
            continue

        words = text.split()
        text_length = len(words)
        start = 0

        while start < text_length:
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():
                chunk_entry = {
                    "text": chunk_text,
                    **metadata
                }
                chunks_with_metadata.append(chunk_entry)

            start = end - overlap
            if start < 0:
                start = 0
            
            # Prevent infinite loop if chunk_size is somehow 0 or text is smaller than overlap
            if start >= text_length:
                break
                
            # If we just finished the last chunk efficiently
            if end >= text_length:
                break

    return chunks_with_metadata
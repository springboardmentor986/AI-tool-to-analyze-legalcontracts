# ingestion/clause_splitter.py

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks
    """
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

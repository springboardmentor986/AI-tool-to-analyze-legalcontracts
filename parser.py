from pypdf import PdfReader

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    # Extract text from PDF
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Manual chunking
    chunk_size = 500
    overlap = 50

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return text, chunks

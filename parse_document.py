from pypdf import PdfReader
reader = PdfReader("documents/sample_contract.pdf")

text = ""
for page in reader.pages:
    extracted = page.extract_text()
    if extracted:
        text += extracted

print("Document loaded successfully")
print("Total characters:", len(text))


chunk_size = 500
overlap = 50

chunks = []
start = 0

while start < len(text):
    end = start + chunk_size
    chunks.append(text[start:end])
    start = end - overlap

print("Total chunks created:", len(chunks))
print("Sample chunk:\n", chunks[0][:300])

from pypdf import PdfReader
from docx import Document
from ingestion.file_validator import validate_file
from io import BytesIO

def extract_text(file):
    ext = validate_file(file)

    # Read uploaded file as bytes
    file_bytes = file.read()

    # -------- PDF --------
    if ext == "pdf":
        reader = PdfReader(BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()

    # -------- DOCX --------
    if ext == "docx":
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs).strip()

    # -------- TXT --------
    if ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore").strip()

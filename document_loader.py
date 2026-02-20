from pypdf import PdfReader
import docx

def load_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def load_document(file):
    if file.name.endswith(".pdf"):
        return load_pdf(file)
    elif file.name.endswith(".docx"):
        return load_docx(file)
    else:
        return file.read().decode("utf-8")

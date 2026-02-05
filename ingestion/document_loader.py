from PyPDF2 import PdfReader
import docx

def load_document(uploaded_file):
    file_name = uploaded_file.name.lower()

    # -------- PDF --------
    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    # -------- DOCX --------
    elif file_name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs]).strip()

    # -------- TXT --------
    elif file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8").strip()

    else:
        raise ValueError("Unsupported file type")

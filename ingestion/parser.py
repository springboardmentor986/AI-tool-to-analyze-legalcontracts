from PyPDF2 import PdfReader
import docx

async def parse_file(uploaded_file) -> str:
    text = ""

    name = (
        uploaded_file.filename
        if hasattr(uploaded_file, "filename")
        else uploaded_file.name
    ).lower()

    file_obj = (
        uploaded_file.file
        if hasattr(uploaded_file, "file")
        else uploaded_file
    )

    if name.endswith(".pdf"):
        reader = PdfReader(file_obj)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    elif name.endswith(".docx"):
        doc = docx.Document(file_obj)
        for p in doc.paragraphs:
            text += p.text + "\n"

    elif name.endswith(".txt"):
        text = (await uploaded_file.read()).decode("utf-8", errors="ignore")

    return text

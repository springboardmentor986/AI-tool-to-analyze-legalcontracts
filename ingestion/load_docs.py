import os
import warnings
warnings.filterwarnings("ignore")

import pdfplumber
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



def load_docx(path):
    doc = Document(path)
    text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    return text


def load_pdf(path):
    full_text = ""

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    return full_text


def load_contract(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # PDF
    if path.lower().endswith(".pdf"):
        text = load_pdf(path)
        return splitter.create_documents([text])

    # DOCX
    elif path.lower().endswith(".docx"):
        text = load_docx(path)
        return splitter.create_documents([text])

    else:
        raise ValueError("Only PDF and DOCX files are supported")

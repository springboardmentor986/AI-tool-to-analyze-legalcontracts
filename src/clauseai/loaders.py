from __future__ import annotations
from typing import Tuple

from pypdf import PdfReader
from docx import Document


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def load_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def load_contract(file_path: str) -> Tuple[str, str]:
    """
    Returns: (file_type, extracted_text)
    file_type: 'pdf' or 'docx'
    """
    lower = file_path.lower()
    if lower.endswith(".pdf"):
        return "pdf", load_pdf(file_path)
    if lower.endswith(".docx"):
        return "docx", load_docx(file_path)
    raise ValueError("Unsupported file type. Upload PDF or DOCX.")




import os
import pdfplumber
from docx import Document # Word files ke liye
from pypdf import PdfReader


def get_document_text(file_path):
    full_text = ""
    # File ki extension check karo (.pdf ya .docx)
    extension = os.path.splitext(file_path)[1].lower()

    try:
        # --- AGAR PDF HAI ---
        if extension == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"

        # --- AGAR WORD (DOCX) HAI ---
        elif extension == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                full_text += para.text + "\n"
        
        else:
            return "Unsupported file format! Please upload PDF or DOCX."
    except Exception as e:
        return f"Error reading file: {str(e)}"
        
    return full_text
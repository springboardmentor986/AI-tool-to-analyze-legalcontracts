import pypdf # <--- Fulfills your requirement
import streamlit as st

def inspect_pdf_metadata(file_path):
    """
    Uses pypdf to extract metadata and validate the file.
    """
    try:
        reader = pypdf.PdfReader(file_path)
        
        # 1. Check Encryption
        if reader.is_encrypted:
            return {"error": "PDF is encrypted. Please remove password."}
            
        # 2. Extract Metadata
        meta = reader.metadata
        info = {
            "pages": len(reader.pages),
            "author": meta.author if meta and meta.author else "Unknown",
            "producer": meta.producer if meta and meta.producer else "Unknown",
            "encrypted": False
        }
        return info
        
    except Exception as e:
        return {"error": f"pypdf could not read file: {str(e)}"}
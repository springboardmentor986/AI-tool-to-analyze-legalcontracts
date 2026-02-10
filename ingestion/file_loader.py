from io import BytesIO
import pytesseract
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
from docx import Document
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def text_extractor(uploaded_file):
    """
    Handles PDF, DOCX, TXT uploads.
    Returns a LIST of dictionaries:
    [
        {"text": "...", "source": "text/ocr", "page": 1},
        ...
    ]
    """
    file_name = uploaded_file.name.lower()
    extracted_data = []

    try:
        # ---------- PDF ----------
        if file_name.endswith(".pdf"):
            file_bytes = uploaded_file.read()
            reader = PdfReader(BytesIO(file_bytes))
            
            # Helper to check if OCR is needed
            def needs_ocr(text):
                return len(text.strip()) < 50

            for i, page in enumerate(reader.pages):
                page_num = i + 1
                text = page.extract_text() or ""
                
                source_type = "text"

                # If text is minimal, try OCR
                if needs_ocr(text):
                    try:
                        # Convert specific page to image
                        images = convert_from_bytes(
                            file_bytes, 
                            first_page=page_num, 
                            last_page=page_num
                        )
                        if images:
                            ocr_text = pytesseract.image_to_string(images[0])
                            if len(ocr_text.strip()) > len(text.strip()):
                                text = ocr_text
                                source_type = "ocr"
                    except Exception as e:
                        logger.warning(f"OCR failed for page {page_num}: {e}")
                        # Fallback to whatever text we found (even if empty)
                
                if text.strip():
                    extracted_data.append({
                        "text": text.strip(),
                        "source": source_type,
                        "page": page_num
                    })

            return extracted_data
        
        # ---------- DOCX ----------
        elif file_name.endswith(".docx"):
            doc = Document(uploaded_file)
            full_text = ""
            for p in doc.paragraphs:
                full_text += p.text + "\n"
            
            if full_text.strip():
                extracted_data.append({
                    "text": full_text.strip(),
                    "source": "text",
                    "page": 1 # DOCX treated as single unit for now
                })
            return extracted_data
        
        # ---------- TXT ----------
        elif file_name.endswith(".txt"):
            text = uploaded_file.read().decode("UTF-8")
            if text.strip():
                extracted_data.append({
                    "text": text.strip(),
                    "source": "text",
                    "page": 1
                })
            return extracted_data
            
        else:
            raise ValueError("Unsupported file type")
            
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")
        return []
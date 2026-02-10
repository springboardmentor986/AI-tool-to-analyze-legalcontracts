from fpdf import FPDF
from docx import Document
import io

def generate_pdf(report_text: str) -> bytes:
    """
    Generates a PDF file from the given report text.
    """
    class PDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 15)
            self.cell(0, 10, 'ClauseAI Analysis Report', align='C')
            self.ln(20)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    
    # Simple encodig fix for unicode characters
    # FPDF2 handles unicode better but requires a font supporting it. 
    # For standard usage without external fonts, we replace common chars or use latin-1.
    # To be safe and quick, we'll try to encode/decode or use a compatible font if available, 
    # but strictly speaking fpdf2 default font is limited.
    # We will just write it and catch encoding errors by replacing.
    
    # A safer approach for "quick" text without external font files:
    safe_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 10, safe_text)
    
    return bytes(pdf.output())

def generate_word(report_text: str) -> bytes:
    """
    Generates a Word (DOCX) file from the given report text.
    """
    doc = Document()
    doc.add_heading('ClauseAI Analysis Report', 0)
    
    # Split by newlines to keep some structure
    for paragraph in report_text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

from fpdf import FPDF
from docx import Document
import io
import re

class ClauseAIPDF(FPDF):
    def header(self):
        # Only print header on pages > 1 to avoid title duplication on cover
        if self.page_no() > 1:
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, 'ClauseAI Analysis Report', align='R')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_body(self, text):
        self.set_font('helvetica', size=11)
        self.set_text_color(0, 0, 0)
        
        # Clean text
        replacements = {
            "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
            "…": "...", "₹": "Rs.", "€": "EUR", "£": "GBP",
            "✅": "[PASS]", "⚠️": "[RISK]", "❌": "[FAIL]",
            "●": "-", "•": "-"
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # Encode
        text = text.encode('latin-1', 'replace').decode('latin-1')
        
        lines = text.split('\n')
        
        # Title Handling: If the first line is a title, make it big
        first_line = True
        
        for line in lines:
            line = line.strip()
            if not line:
                self.ln(2)
                continue
                
            # Handle Headers
            if line.startswith('#'):
                level = len(line.split(' ')[0])
                clean_line = line.lstrip('#').strip()
                
                # Special case: Title detection (first line or #)
                if level == 1:
                    self.ln(5)
                    self.set_font('helvetica', 'B', 16)
                    self.set_fill_color(240, 240, 240)
                    self.cell(0, 10, clean_line, ln=True, fill=True)
                    self.set_font('helvetica', size=11)
                elif level == 2:
                    self.ln(4)
                    self.set_font('helvetica', 'B', 14)
                    self.cell(0, 8, clean_line, ln=True)
                    self.set_font('helvetica', size=11)
                elif level == 3:
                    self.ln(2)
                    self.set_font('helvetica', 'B', 12)
                    self.cell(0, 6, clean_line, ln=True)
                    self.set_font('helvetica', size=11)
                else:
                    self.set_font('helvetica', 'B', 11)
                    self.cell(0, 6, clean_line, ln=True)
                    self.set_font('helvetica', size=11)

            # Handle Bullet Points
            elif line.startswith('- ') or line.startswith('* '):
                self.set_x(self.l_margin + 5)
                bullet_text = line[2:]
                self._write_markdown_line(bullet_text)
                
            # Standard Text
            else:
                self._write_markdown_line(line)
                
    def _write_markdown_line(self, text):
        """Helpers to handle bold text (**text**) within a line"""
        if "**" not in text:
            self.multi_cell(0, 5, text)
            self.ln(1)
            return

        parts = text.split("**")
        for i, part in enumerate(parts):
            if i % 2 == 1: # Odd = Bold
                self.set_font('helvetica', 'B', 11)
                self.write(5, part)
            else:
                self.set_font('helvetica', '', 11)
                self.write(5, part)
        self.ln(6) # End of line

def generate_pdf(report_text: str) -> bytes:
    """
    Generates a professionally formatted PDF report.
    """
    pdf = ClauseAIPDF()
    pdf.add_page()
    pdf.chapter_body(report_text)
    return bytes(pdf.output())

def generate_word(report_text: str) -> bytes:
    """
    Generates a Word (DOCX) file from the given report text.
    """
    doc = Document()
    doc.add_heading('ClauseAI Analysis Report', 0)
    
    # Simple markdown parsing for Word
    for line in report_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('- ') or line.startswith('* '):
            p = doc.add_paragraph(line[2:], style='List Bullet')
        else:
            doc.add_paragraph(line)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

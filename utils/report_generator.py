from fpdf import FPDF
from docx import Document
import io
import re

class ClauseAIPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'ClauseAI Strategic Analysis Report', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, label):
        self.set_font('helvetica', 'B', 14)
        self.set_fill_color(230, 230, 230)  # Light gray background
        self.cell(0, 10, label, fill=True, ln=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('helvetica', size=11)
        
        # Clean text for Latin-1 compatibility
        # Replace common incompatible chars with safe equivalents
        replacements = {
            "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
            "…": "...", "₹": "Rs.", "€": "EUR", "£": "GBP",
            "✅": "[PASS]", "⚠️": "[RISK]", "❌": "[FAIL]",
            "●": "-", "•": "-"
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # Final safety net: strictly encode to latin-1, replacing errors
        text = text.encode('latin-1', 'replace').decode('latin-1')
        
        # Split into lines to handle formatting line-by-line
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                self.ln(2)
                continue
                
            # Handle Headers (### or ## or #)
            if line.startswith('#'):
                # Count hashes
                level = len(line.split(' ')[0])
                clean_line = line.lstrip('#').strip()
                
                if level == 1:
                    self.ln(5)
                    self.set_font('helvetica', 'B', 14)
                    self.cell(0, 10, clean_line, ln=True)
                    self.set_font('helvetica', size=11)
                elif level == 2:
                    self.ln(4)
                    self.set_font('helvetica', 'B', 12)
                    self.cell(0, 8, clean_line, ln=True)
                    self.set_font('helvetica', size=11)
                else:
                    self.ln(2)
                    self.set_font('helvetica', 'B', 11)
                    self.cell(0, 6, clean_line, ln=True)
                    self.set_font('helvetica', size=11)
                    
            # Handle Bullet Points (- or *)
            elif line.startswith('- ') or line.startswith('* '):
                self.set_x(self.l_margin + 5) # Indent
                bullet_text = line[2:]
                
                # Check for Bold within bullet (**text**)
                if "**" in bullet_text:
                    parts = bullet_text.split("**")
                    for i, part in enumerate(parts):
                        if i % 2 == 1: # Odd indices are bold
                            self.set_font('helvetica', 'B', 11)
                            self.write(6, part)
                        else:
                            self.set_font('helvetica', '', 11)
                            self.write(6, part)
                    self.ln(6)
                else:
                    self.multi_cell(0, 6, bullet_text)
                    
            # Handle Bold Text in normal lines
            elif "**" in line:
                parts = line.split("**")
                for i, part in enumerate(parts):
                    if i % 2 == 1: # Odd indices are bold
                        self.set_font('helvetica', 'B', 11)
                        self.write(6, part)
                    else:
                        self.set_font('helvetica', '', 11)
                        self.write(6, part)
                self.ln(6)
                
            # Standard Text
            else:
                self.multi_cell(0, 6, line)

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

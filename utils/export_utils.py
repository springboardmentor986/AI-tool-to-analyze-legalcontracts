from fpdf import FPDF
import ast
import re

# --- 1. CLEANING HELPER (Specific for PDF) ---
def clean_for_pdf(raw_data):
    """
    Cleans the raw AI output string for the PDF report.
    Removes JSON wrappers, signatures, and Markdown formatting.
    """
    text = str(raw_data).strip()
    
    # A. Parse Dictionary/JSON Structure
    try:
        # If it looks like a list or dict, parse it
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list) and len(parsed) > 0:
                text = parsed[0].get('text', str(parsed[0])) if isinstance(parsed[0], dict) else str(parsed[0])
            elif isinstance(parsed, dict):
                text = parsed.get('text', str(parsed))
    except:
        pass # Fallback to regex if parsing fails

    # B. Brute Force Cleanup (if parsing failed or left artifacts)
    if "{'type': 'text'" in text:
        start = text.find("'text': '")
        if start != -1: text = text[start + 9:]
    
    # Remove signatures/extras
    extras_markers = ["', 'extras':", '", "extras":', "', 'type':"]
    for marker in extras_markers:
        if marker in text: text = text.split(marker)[0]

    # C. Formatting Cleanup
    text = text.replace("\\n", "\n").replace("\\'", "'").replace('"', '"').replace("'", "'")
    
    # Remove Markdown symbols for cleaner PDF look
    text = text.replace('**', '').replace('###', '').replace('##', '')
    
    # Remove trailing syntax
    text = text.rstrip("'\"}]")
    
    return text.strip()

# --- 2. PDF CLASS DEFINITION ---
class ClauseReport(FPDF):
    def header(self):
        # Logo or Brand Name
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 51, 102) # Dark Blue
        self.cell(0, 10, 'ClauseAI - Intelligent Contract Audit', 0, 1, 'C')
        
        # Line break
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(10, 20, 200, 20)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128) # Grey
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102) # Dark Blue
        self.cell(0, 10, label, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0) # Black
        
        # FPDF doesn't support UTF-8 perfectly, so we sanitize
        safe_body = body.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, safe_body)
        self.ln(5)

# --- 3. GENERATOR FUNCTION ---
def generate_pdf(results):
    pdf = ClauseReport()
    pdf.add_page()
    
    # Define the sections to include
    sections = [
        ("Executive Synthesis", "synthesis"),
        ("Legal Analysis", "legal"),
        ("Financial Review", "finance"),
        ("Compliance Check", "compliance"),
        ("Operational Risks", "operations")
    ]
    
    for title, key in sections:
        # Get data safely
        data = results.get(key, {})
        raw_text = data.get("summary", "No analysis available.")
        
        # CLEAN THE TEXT
        clean_content = clean_for_pdf(raw_text)
        
        # Add to PDF
        pdf.chapter_title(title)
        pdf.chapter_body(clean_content)
        
    return pdf.output(dest='S').encode('latin-1')
from fpdf import FPDF
import io

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'ClauseAI - Intelligent Contract Audit', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(220, 220, 220)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_pdf(results):
    pdf = PDFReport()
    pdf.add_page()
    
    sections = [
        ("Executive Synthesis", "synthesis"),
        ("Legal Analysis", "legal"),
        ("Financial Review", "finance"),
        ("Compliance Check", "compliance"),
        ("Operational Risks", "operations")
    ]
    
    for title, key in sections:
        data = results.get(key, {})
        summary = data.get("summary", "No data available.")
        
        # Simple clean logic
        if isinstance(summary, dict): summary = summary.get('text', str(summary))
        if isinstance(summary, list): summary = "\n".join([str(x) for x in summary])
        
        # Replace non-latin characters for FPDF
        clean_summary = str(summary).encode('latin-1', 'replace').decode('latin-1')
        
        pdf.chapter_title(title)
        pdf.chapter_body(clean_summary)
        
    return pdf.output(dest='S').encode('latin-1', 'replace')
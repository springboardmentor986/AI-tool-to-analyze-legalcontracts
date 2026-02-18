from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import ast
import re

# --- 1. CLEANING HELPER ---
def clean_for_pdf(raw_data):
    """
    Parses raw AI output to get clean text, then formats it for ReportLab.
    """
    text = str(raw_data).strip()
    
    # A. Parse Dictionary/JSON Structure
    try:
        if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list) and len(parsed) > 0:
                text = parsed[0].get('text', str(parsed[0])) if isinstance(parsed[0], dict) else str(parsed[0])
            elif isinstance(parsed, dict):
                text = parsed.get('text', str(parsed))
    except:
        pass 

    # B. Brute Force Cleanup
    if "{'type': 'text'" in text:
        start = text.find("'text': '")
        if start != -1: text = text[start + 9:]
    
    extras_markers = ["', 'extras':", '", "extras":', "', 'type':"]
    for marker in extras_markers:
        if marker in text: text = text.split(marker)[0]

    # C. Cleanup Formatting
    text = text.replace("\\n", "\n").replace("\\'", "'").replace('"', '"').replace("'", "'")
    text = text.rstrip("'\"}]")
    
    # --- REPORTLAB SPECIFIC FORMATTING ---
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text) # Bold
    text = re.sub(r'#{2,}\s?(.*)', r'<b>\1</b><br/>', text) # Headers
    text = text.replace("\n", "<br/>") # Line breaks
    
    return text.strip()

# --- 2. FONT REGISTRATION ---
def register_custom_fonts():
    font_path = os.path.join("fonts", "NotoSansTamil-Regular.ttf")
    try:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('NotoSans', font_path))
            return 'NotoSans'
        else:
            return 'Helvetica'
    except:
        return 'Helvetica'

# --- 3. GENERATOR FUNCTION ---
def generate_pdf(results):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    body_font = register_custom_fonts()
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading1'], fontName=body_font, 
        fontSize=24, textColor=colors.HexColor("#003366"), 
        spaceAfter=20, alignment=1
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle', parent=styles['Heading2'], fontName=body_font,
        textColor=colors.white, backColor=colors.HexColor("#003366"),
        borderPadding=5, spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'BodyStyle', parent=styles['Normal'], fontName=body_font,
        fontSize=11, leading=14, spaceAfter=10
    )

    # --- CONTENT ---
    story.append(Paragraph("CLAUSE.AI AUDIT REPORT", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>CONFIDENTIAL LEGAL ANALYSIS</b>", styles["Normal"]))
    story.append(Spacer(1, 20))

    # EXECUTIVE SYNTHESIS
    if "synthesis" in results:
        story.append(Paragraph("EXECUTIVE SYNTHESIS", header_style))
        raw_text = results["synthesis"].get("summary", "No summary.")
        clean_text = clean_for_pdf(raw_text)
        story.append(Paragraph(clean_text, body_style))
        story.append(Spacer(1, 10))
        story.append(PageBreak())

    # AGENTS LOOP
    agents = [
        ("LEGAL RISK ANALYSIS", "legal"),
        ("FINANCIAL AUDIT", "finance"),
        ("COMPLIANCE CHECK", "compliance"),
        ("OPERATIONAL REVIEW", "operations")
    ]

    for title, key in agents:
        if key in results:
            # 1. Section Header (With Background Color)
            story.append(Paragraph(title, header_style))
            
            # 2. Content (Standard Paragraph - CRASH PROOF)
            # We removed the 'Table' wrapper here. 
            # Paragraphs can naturally split across pages.
            raw_text = results[key].get("summary", "No data.")
            clean_text = clean_for_pdf(raw_text)
            
            story.append(Paragraph(clean_text, body_style))
            story.append(Spacer(1, 15))

    doc.build(story)
    buffer.seek(0)
    return buffer
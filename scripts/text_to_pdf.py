# Plain text to visually designed PDF generator
# Requires: reportlab
# Usage: python text_to_pdf.py input.txt output.pdf

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer
import sys


def create_beautiful_pdf(text, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=LETTER)
    width, height = LETTER

    # Background gradient (simple two-tone)
    c.setFillColor(HexColor('#f5f0e6'))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(HexColor('#e0d6c3'))
    c.rect(0, 0, width, height * 0.15, fill=1, stroke=0)

    # Decorative border
    c.setStrokeColor(HexColor('#bfae8e'))
    c.setLineWidth(6)
    c.roundRect(0.4*inch, 0.4*inch, width-0.8*inch, height-0.8*inch, 24, stroke=1, fill=0)

    # Title styling
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=HexColor('#6d4c1e'),
        alignment=1,
        spaceAfter=24,
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Times-Roman',
        fontSize=13,
        leading=18,
        textColor=HexColor('#2d1e0f'),
        alignment=4,
        spaceAfter=12,
    )

    # Split text into paragraphs
    paragraphs = text.strip().split('\n\n')
    story = []
    if paragraphs:
        story.append(Paragraph(paragraphs[0], title_style))
        for para in paragraphs[1:]:
            story.append(Paragraph(para, body_style))
            story.append(Spacer(1, 8))

    # Frame for text
    frame = Frame(0.8*inch, 0.8*inch, width-1.6*inch, height-1.6*inch, showBoundary=0)
    frame.addFromList(story, c)

    c.showPage()
    c.save()


def main():
    if len(sys.argv) != 3:
        print("Usage: python text_to_pdf.py input.txt output.pdf")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()
    create_beautiful_pdf(text, sys.argv[2])

if __name__ == "__main__":
    main()

# utils/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(title, author_name, affiliation, address, date, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    text = c.beginText(50, height - 50)
    text.setFont("Times-Roman", 12)

    lines = [
        "Copyright Transfer Agreement",
        "",
        f"Manuscript Title: {title}",
        "",
        "The undersigned hereby transfers to the publisher the copyright",
        "to the above-titled manuscript. This transfer includes all rights",
        "to publish, reproduce, and distribute the work in any medium,",
        "now and in the future.",
        "",
        f"Author Name: {author_name}",
        f"Affiliation: {affiliation}",
        f"Address: {address}",
        f"Date: {date}"
    ]

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

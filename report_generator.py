from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.units import inch
import os


def create_pdf_report(report_text, filename="research_report.pdf"):
    """
    Convert the final AI research report text into a PDF.
    """

    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=26,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading1"],
        fontSize=15,
        leading=20,
        spaceBefore=15,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "BodyCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8
    )

    story = []

    # Report title
    story.append(
        Paragraph(
            "AI Research Assistant",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Research Report",
            heading_style
        )
    )

    story.append(Spacer(1, 0.2 * inch))

    # Process report line by line
    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        # Main Markdown headings
        if line.startswith("# "):
            text = line[2:]
            story.append(
                Paragraph(text, heading_style)
            )

        elif line.startswith("## "):
            text = line[3:]
            story.append(
                Paragraph(text, heading_style)
            )

        # Bullet points
        elif line.startswith("* "):
            text = "• " + line[2:]
            story.append(
                Paragraph(text, body_style)
            )

        elif line.startswith("- "):
            text = "• " + line[2:]
            story.append(
                Paragraph(text, body_style)
            )

        else:
            # Basic Markdown bold conversion
            text = line.replace("**", "")

            story.append(
                Paragraph(text, body_style)
            )

    doc.build(story)

    return filepath
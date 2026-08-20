from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os


def add_title(slide, title, subtitle=None):
    """Add a professional title to a slide."""

    title_box = slide.shapes.add_textbox(
        Inches(0.7),
        Inches(0.45),
        Inches(11.8),
        Inches(0.7)
    )

    tf = title_box.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True

    if subtitle:
        sub_box = slide.shapes.add_textbox(
            Inches(0.72),
            Inches(1.15),
            Inches(11),
            Inches(0.45)
        )

        p = sub_box.text_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(14)


def add_bullets(slide, bullets, x=0.9, y=1.7, width=11, height=4.8):
    """Add bullet points."""

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(width),
        Inches(height)
    )

    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()

    for i, bullet in enumerate(bullets):

        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()

        p.text = bullet
        p.font.size = Pt(20)
        p.space_after = Pt(14)


def add_footer(slide, slide_number):
    """Add footer."""

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0),
        Inches(7.15),
        Inches(13.33),
        Inches(0.35)
    )

    line.text = "ResearchX-AI"

    p = line.text_frame.paragraphs[0]
    p.font.size = Pt(10)
    p.alignment = PP_ALIGN.CENTER


def create_professional_ppt(report_text, topic,
                            filename="research_presentation.pptx"):

    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join("outputs", filename)

    prs = Presentation()

    # ---------------------------------------------------------
    # Slide 1 — Title
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title = slide.shapes.add_textbox(
        Inches(1),
        Inches(2),
        Inches(11.3),
        Inches(1.2)
    )

    p = title.text_frame.paragraphs[0]
    p.text = topic
    p.font.size = Pt(34)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER

    subtitle = slide.shapes.add_textbox(
        Inches(2),
        Inches(3.4),
        Inches(9.3),
        Inches(0.8)
    )

    p = subtitle.text_frame.paragraphs[0]
    p.text = "ResearchX-AI | AI-Powered Research Report"
    p.font.size = Pt(20)
    p.alignment = PP_ALIGN.CENTER

    # ---------------------------------------------------------
    # Slide 2 — Executive Summary
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Executive Summary")

    add_bullets(slide, [
        "Generative AI is transforming data science rather than eliminating the profession.",
        "Repetitive tasks such as boilerplate coding and basic data cleaning are increasingly automated.",
        "Data scientists are shifting toward strategy, system design and business problem-solving.",
        "GenAI expertise is becoming an important differentiator for future data professionals."
    ])

    add_footer(slide, 2)

    # ---------------------------------------------------------
    # Slide 3 — Research Workflow
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "ResearchX-AI Workflow")

    add_bullets(slide, [
        "1. Researcher Agent — searches and analyzes relevant information.",
        "2. Fact Checker Agent — verifies claims and evaluates evidence.",
        "3. Synthesis Agent — combines verified findings into a structured report.",
        "4. Report Generator — produces professional PDF and PowerPoint outputs."
    ])

    add_footer(slide, 3)

    # ---------------------------------------------------------
    # Slide 4 — Key Findings
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Key Findings")

    add_bullets(slide, [
        "Job Evolution — GenAI is changing the responsibilities of data scientists.",
        "Workflow Automation — repetitive coding, cleaning and reporting can be accelerated.",
        "Synthetic Creation — AI can generate synthetic data and assist with feature creation.",
        "New Roles — GenAI Engineer, AI Data Scientist and Decision Intelligence roles are emerging.",
        "Human Judgment — business understanding, ethics and communication remain critical."
    ])

    add_footer(slide, 4)

    # ---------------------------------------------------------
    # Slide 5 — Evidence & Statistics
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Evidence & Statistics")

    add_bullets(slide, [
        "33.5% projected employment growth for data scientists from 2024–2034.",
        "402+ million terabytes of data are estimated to be produced globally each day.",
        "Traditional Data Scientist: ₹8–25 LPA.",
        "AI Data Scientist: ₹15–40 LPA.",
        "GenAI Specialist: ₹20–50+ LPA.",
        "Python, SQL and Machine Learning remain important foundational skills."
    ])

    add_footer(slide, 5)

    # ---------------------------------------------------------
    # Slide 6 — Before vs After
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Data Scientist: Before vs. AI-Augmented")

    add_bullets(slide, [
        "BEFORE: Manual data cleaning → AFTER: AI-assisted anomaly detection",
        "BEFORE: Boilerplate coding → AFTER: AI-assisted code generation",
        "BEFORE: Static reports → AFTER: Automated natural-language insights",
        "BEFORE: Manual experimentation → AFTER: AI-assisted feature exploration",
        "BEFORE: Technical execution → AFTER: Strategy + human oversight"
    ])

    add_footer(slide, 6)

    # ---------------------------------------------------------
    # Slide 7 — Industry Impact
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Industry Impact")

    add_bullets(slide, [
        "Technology — faster software development and automated data pipelines.",
        "Finance — synthetic data, fraud detection and automated reporting.",
        "Healthcare — synthetic patient data and analysis of clinical information.",
        "Retail — automated recommendations, pricing and consumer insights."
    ])

    add_footer(slide, 7)

    # ---------------------------------------------------------
    # Slide 8 — Skills
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Skills for the Future Data Scientist")

    add_bullets(slide, [
        "Python",
        "SQL",
        "Machine Learning",
        "Generative AI & LLMs",
        "MLOps & deployment",
        "Business understanding",
        "Communication and problem framing",
        "Responsible AI and ethics"
    ])

    add_footer(slide, 8)

    # ---------------------------------------------------------
    # Slide 9 — Risks
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Risks & Challenges")

    add_bullets(slide, [
        "Hallucinations and inaccurate AI-generated information.",
        "Bias in AI-generated outputs and decision systems.",
        "Privacy and security risks when handling sensitive data.",
        "Over-reliance on AI without understanding underlying models.",
        "Need for human oversight and responsible AI governance."
    ])

    add_footer(slide, 9)

    # ---------------------------------------------------------
    # Slide 10 — Research Gaps
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Research Gaps")

    add_bullets(slide, [
        "Limited quantitative evidence on net job creation versus displacement.",
        "Salary evidence is geographically limited in the available sources.",
        "More research is needed on which human skills remain most resilient.",
        "Long-term risks of synthetic-data generation require further study."
    ])

    add_footer(slide, 10)

    # ---------------------------------------------------------
    # Slide 11 — Recommendations
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Strategic Recommendations")

    add_bullets(slide, [
        "Companies: establish AI governance and human-in-the-loop processes.",
        "Data teams: integrate GenAI and AutoML while maintaining model oversight.",
        "Universities: combine Python, SQL and ML with GenAI and responsible AI.",
        "Students: build both technical expertise and business communication skills."
    ])

    add_footer(slide, 11)

    # ---------------------------------------------------------
    # Slide 12 — Conclusion
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Conclusion")

    add_bullets(slide, [
        "Generative AI is transforming data science rather than making it obsolete.",
        "Routine technical tasks are increasingly becoming automated.",
        "The value of data scientists is moving toward strategy, judgment and system design.",
        "Future professionals should combine Python, SQL, ML and GenAI with business and communication skills.",
        "The strongest data scientists will be those who know how to work WITH AI."
    ])

    add_footer(slide, 12)

    # ---------------------------------------------------------
    # Slide 13 — Sources
    # ---------------------------------------------------------

    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_title(slide, "Research Sources")

    add_bullets(slide, [
        "U.S. Bureau of Labor Statistics — Data Scientist Employment Outlook",
        "Syracuse University iSchool — AI in Data Science",
        "NYIT — Will AI Replace Data Science?",
        "IE University — Global Demand for Data Science Professionals",
        "Making Science — Impact of Generative AI on Data Analytics",
        "SP Jain — Generative AI and Data Science",
        "Additional sources identified and evaluated by ResearchX-AI"
    ])

    add_footer(slide, 13)

    # Save
    prs.save(filepath)

    return filepath
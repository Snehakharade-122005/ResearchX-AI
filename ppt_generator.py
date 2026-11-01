# ============================================================
# ResearchX-AI - Professional PowerPoint Generator
# 13-Slide Research Presentation
# ============================================================

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
import os
import re
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

FONT = "Aptos"

NAVY = RGBColor(15, 23, 42)
DARK = RGBColor(30, 41, 59)
BLUE = RGBColor(37, 99, 235)
CYAN = RGBColor(14, 165, 233)

WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(15, 23, 42)
GRAY = RGBColor(100, 116, 139)
LIGHT_GRAY = RGBColor(241, 245, 249)
MID_GRAY = RGBColor(203, 213, 225)

GREEN = RGBColor(22, 163, 74)
PURPLE = RGBColor(124, 58, 237)
ORANGE = RGBColor(234, 88, 12)
RED = RGBColor(220, 38, 38)


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = str(text)

    replacements = {
        "**": "",
        "__": "",
        "###": "",
        "##": "",
        "#": "",
        "→": "->",
        "–": "-",
        "—": "-",
        "```markdown": "",
        "```text": "",
        "```": ""
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def shorten_text(text, max_length=180):
    text = clean_text(text)

    if len(text) <= max_length:
        return text

    return text[:max_length - 3].rstrip() + "..."


# ============================================================
# REPORT PARSER
# ============================================================

def extract_sections(report_text):
    sections = {}

    if not report_text:
        return sections

    current_title = "Overview"
    current_content = []

    for line in str(report_text).splitlines():

        line = line.strip()

        if not line:
            continue

        heading = re.match(r"^#{1,3}\s+(.+)$", line)

        if heading:

            if current_content:
                sections[current_title] = "\n".join(
                    current_content
                )

            current_title = clean_text(
                heading.group(1)
            )

            current_content = []

        else:
            current_content.append(line)

    if current_content:
        sections[current_title] = "\n".join(
            current_content
        )

    return sections


def find_section(sections, keywords):

    for title, content in sections.items():

        title_lower = title.lower()

        for keyword in keywords:

            if keyword.lower() in title_lower:
                return content

    return ""


def extract_bullets(text, max_items=6):

    if not text:
        return []

    bullets = []

    for line in str(text).splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("```"):
            continue

        if re.match(r"^[|\-:\s]+$", line):
            continue

        if any(
            symbol in line
            for symbol in [
                "┌", "┐", "└", "┘",
                "│", "─", "▼",
                "╔", "╗", "╚", "╝",
                "═", "║"
            ]
        ):
            continue

        line = re.sub(
            r"^[-*•]\s*",
            "",
            line
        )

        line = re.sub(
            r"^\d+[\.\)]\s*",
            "",
            line
        )

        line = clean_text(line)

        if len(line) > 10:
            bullets.append(
                shorten_text(line, 170)
            )

    return bullets[:max_items]


# ============================================================
# BASIC SLIDE HELPERS
# ============================================================

def add_background(slide, color=WHITE):

    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_WIDTH,
        SLIDE_HEIGHT
    )

    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

    # Move to back
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_top_bar(slide):

    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0,
        0,
        SLIDE_WIDTH,
        Inches(0.12)
    )

    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()


def add_text(
    slide,
    text,
    x,
    y,
    width,
    height,
    font_size=18,
    color=BLACK,
    bold=False,
    align=PP_ALIGN.LEFT
):

    box = slide.shapes.add_textbox(
        Inches(x),
        Inches(y),
        Inches(width),
        Inches(height)
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True

    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)

    p = tf.paragraphs[0]

    p.text = clean_text(text)
    p.alignment = align

    p.font.name = FONT
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color

    return box


def add_title(slide, title, subtitle=None):

    add_text(
        slide,
        title,
        0.65,
        0.42,
        11.8,
        0.55,
        28,
        NAVY,
        True
    )

    if subtitle:

        add_text(
            slide,
            subtitle,
            0.68,
            1.02,
            11.5,
            0.4,
            12,
            GRAY
        )


def add_footer(slide, number):

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.65),
        Inches(7.08),
        Inches(12),
        Inches(0.01)
    )

    line.fill.solid()
    line.fill.fore_color.rgb = MID_GRAY
    line.line.fill.background()

    add_text(
        slide,
        "ResearchX-AI",
        0.68,
        7.12,
        2,
        0.2,
        8,
        GRAY
    )

    add_text(
        slide,
        str(number),
        11.8,
        7.12,
        0.7,
        0.2,
        8,
        GRAY,
        False,
        PP_ALIGN.RIGHT
    )


# ============================================================
# CARD HELPERS
# ============================================================

def add_card(
    slide,
    x,
    y,
    width,
    height,
    title,
    body,
    accent=BLUE
):

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(width),
        Inches(height)
    )

    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = MID_GRAY

    accent_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(0.08),
        Inches(height)
    )

    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = accent
    accent_bar.line.fill.background()

    add_text(
        slide,
        title,
        x + 0.25,
        y + 0.18,
        width - 0.45,
        0.4,
        15,
        NAVY,
        True
    )

    add_text(
        slide,
        body,
        x + 0.25,
        y + 0.65,
        width - 0.45,
        height - 0.8,
        12,
        GRAY
    )


def add_bullet_card(
    slide,
    x,
    y,
    width,
    height,
    title,
    bullets,
    accent=BLUE
):

    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(width),
        Inches(height)
    )

    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = MID_GRAY

    accent_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(0.07),
        Inches(height)
    )

    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = accent
    accent_bar.line.fill.background()

    add_text(
        slide,
        title,
        x + 0.25,
        y + 0.18,
        width - 0.45,
        0.35,
        15,
        NAVY,
        True
    )

    box = slide.shapes.add_textbox(
        Inches(x + 0.25),
        Inches(y + 0.62),
        Inches(width - 0.45),
        Inches(height - 0.75)
    )

    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):

        p = (
            tf.paragraphs[0]
            if i == 0
            else tf.add_paragraph()
        )

        p.text = "• " + clean_text(bullet)
        p.font.name = FONT
        p.font.size = Pt(12)
        p.font.color.rgb = DARK
        p.space_after = Pt(7)


def add_pipeline_step(
    slide,
    x,
    number,
    title,
    description,
    accent
):

    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(x),
        Inches(2.15),
        Inches(0.65),
        Inches(0.65)
    )

    circle.fill.solid()
    circle.fill.fore_color.rgb = accent
    circle.line.fill.background()

    add_text(
        slide,
        str(number),
        x,
        2.23,
        0.65,
        0.3,
        16,
        WHITE,
        True,
        PP_ALIGN.CENTER
    )

    add_text(
        slide,
        title,
        x - 0.35,
        2.95,
        1.35,
        0.45,
        12,
        NAVY,
        True,
        PP_ALIGN.CENTER
    )

    add_text(
        slide,
        description,
        x - 0.5,
        3.4,
        1.65,
        1.25,
        9,
        GRAY,
        False,
        PP_ALIGN.CENTER
    )


# ============================================================
# SLIDE 1 - COVER
# ============================================================

def create_cover_slide(prs, topic):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide, NAVY)

    # Decorative elements
    for i in range(5):

        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(10.8 + i * 0.35),
            Inches(0.8 + i * 0.25),
            Inches(0.15),
            Inches(5.3 - i * 0.35)
        )

        shape.fill.solid()
        shape.fill.fore_color.rgb = BLUE
        shape.fill.transparency = 20
        shape.line.fill.background()

    add_text(
        slide,
        "RESEARCHX-AI",
        0.9,
        1.15,
        6,
        0.5,
        17,
        CYAN,
        True
    )

    add_text(
        slide,
        shorten_text(topic, 110),
        0.9,
        2.0,
        8.8,
        1.8,
        36,
        WHITE,
        True
    )

    add_text(
        slide,
        "AI-Powered Research Intelligence Platform",
        0.95,
        4.15,
        7.5,
        0.5,
        18,
        RGBColor(203, 213, 225)
    )

    add_text(
        slide,
        datetime.now().strftime("%d %B %Y"),
        0.95,
        5.25,
        3.5,
        0.35,
        11,
        GRAY
    )

    add_text(
        slide,
        "PLAN  •  RESEARCH  •  VERIFY  •  SYNTHESIZE",
        0.95,
        6.35,
        7,
        0.35,
        10,
        CYAN,
        True
    )


# ============================================================
# SLIDE 2 - EXECUTIVE SUMMARY
# ============================================================

def create_summary_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Executive Summary",
        "The most important conclusions from the research"
    )

    content = find_section(
        sections,
        ["executive summary", "summary", "overview"]
    )

    bullets = extract_bullets(content, 4)

    if not bullets:
        bullets = [
            "Research findings have been synthesized from available evidence.",
            "The analysis highlights major trends, opportunities and risks.",
            "The research identifies practical implications for decision-makers.",
            "Recommendations are based on the analyzed evidence."
        ]

    positions = [
        (0.8, 1.7),
        (6.7, 1.7),
        (0.8, 4.0),
        (6.7, 4.0)
    ]

    accents = [
        BLUE,
        GREEN,
        PURPLE,
        ORANGE
    ]

    for i, bullet in enumerate(bullets[:4]):

        x, y = positions[i]

        add_card(
            slide,
            x,
            y,
            5.7,
            1.75,
            f"Key Insight {i + 1}",
            bullet,
            accents[i]
        )

    add_footer(slide, 2)


# ============================================================
# SLIDE 3 - METHODOLOGY
# ============================================================

def create_methodology_slide(prs):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "AI Research Methodology",
        "A multi-agent workflow designed for structured research"
    )

    steps = [
        (
            "Research Plan",
            "Break the topic into objectives and research questions.",
            BLUE
        ),
        (
            "Web Research",
            "Collect relevant information from external sources.",
            CYAN
        ),
        (
            "Fact Check",
            "Evaluate claims and supporting evidence.",
            GREEN
        ),
        (
            "Synthesis",
            "Combine verified findings into a coherent analysis.",
            PURPLE
        ),
        (
            "Deliverables",
            "Generate professional report and presentation outputs.",
            ORANGE
        )
    ]

    start_x = 1.0
    gap = 2.45

    for i, (title, description, accent) in enumerate(steps):

        x = start_x + i * gap

        add_pipeline_step(
            slide,
            x,
            i + 1,
            title,
            description,
            accent
        )

        if i < len(steps) - 1:

            connector = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                Inches(x + 0.7),
                Inches(2.48),
                Inches(x + gap),
                Inches(2.48)
            )

            connector.line.color.rgb = MID_GRAY
            connector.line.width = Pt(2)

    add_footer(slide, 3)


# ============================================================
# SLIDE 4 - KEY FINDINGS
# ============================================================

def create_findings_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Key Findings",
        "What the research indicates"
    )

    content = find_section(
        sections,
        ["key findings", "findings"]
    )

    bullets = extract_bullets(content, 6)

    if not bullets:
        bullets = [
            "The research identifies important developments related to the topic.",
            "Multiple trends are shaping the current landscape.",
            "Organizations can benefit from emerging opportunities.",
            "Successful adoption requires appropriate skills and infrastructure.",
            "Risks and implementation challenges must be actively managed.",
            "Further evidence may be required for long-term conclusions."
        ]

    positions = [
        (0.7, 1.6),
        (4.5, 1.6),
        (8.3, 1.6),
        (0.7, 4.0),
        (4.5, 4.0),
        (8.3, 4.0)
    ]

    accents = [
        BLUE,
        CYAN,
        GREEN,
        PURPLE,
        ORANGE,
        RED
    ]

    for i, bullet in enumerate(bullets):

        x, y = positions[i]

        add_card(
            slide,
            x,
            y,
            3.55,
            1.9,
            f"Finding {i + 1}",
            bullet,
            accents[i]
        )

    add_footer(slide, 4)


# ============================================================
# SLIDE 5 - EVIDENCE
# ============================================================

def create_evidence_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Evidence & Research Signals",
        "Important evidence identified during source analysis"
    )

    content = find_section(
        sections,
        [
            "evidence",
            "statistics",
            "research signals",
            "facts"
        ]
    )

    bullets = extract_bullets(content, 5)

    if not bullets:
        bullets = [
            "Evidence was collected from the available research sources.",
            "Important claims were compared against supporting source material.",
            "Statistics are presented only when supported by the source set.",
            "Source quality influences the confidence assigned to findings.",
            "Areas with limited evidence are treated cautiously."
        ]

    # Large evidence panel
    add_bullet_card(
        slide,
        0.8,
        1.55,
        7.3,
        4.95,
        "Research Evidence",
        bullets,
        BLUE
    )

    add_card(
        slide,
        8.5,
        1.55,
        3.9,
        1.45,
        "Evidence Quality",
        "Claims should be interpreted according to the strength and relevance of their supporting sources.",
        GREEN
    )

    add_card(
        slide,
        8.5,
        3.25,
        3.9,
        1.45,
        "Source Validation",
        "The Fact Checker evaluates claims and assigns confidence based on available evidence.",
        PURPLE
    )

    add_card(
        slide,
        8.5,
        4.95,
        3.9,
        1.55,
        "Research Discipline",
        "Unsupported information should not be presented as an established fact.",
        ORANGE
    )

    add_footer(slide, 5)


# ============================================================
# SLIDE 6 - BEFORE VS AFTER
# ============================================================

def create_comparison_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Before vs After",
        "How structured AI-assisted research improves the workflow"
    )

    add_bullet_card(
        slide,
        0.8,
        1.65,
        5.6,
        4.7,
        "Traditional Research Workflow",
        [
            "Manual topic breakdown",
            "Repeated web searching",
            "Manual source comparison",
            "Time-consuming fact verification",
            "Manual report preparation",
            "Limited consistency across research tasks"
        ],
        GRAY
    )

    add_text(
        slide,
        "VS",
        6.2,
        3.45,
        0.9,
        0.5,
        20,
        BLUE,
        True,
        PP_ALIGN.CENTER
    )

    add_bullet_card(
        slide,
        6.9,
        1.65,
        5.6,
        4.7,
        "ResearchX-AI Workflow",
        [
            "Structured research planning",
            "Focused web search queries",
            "Automated source collection",
            "Dedicated fact-checking stage",
            "AI-assisted evidence synthesis",
            "Professional PDF and PPT outputs"
        ],
        BLUE
    )

    add_footer(slide, 6)


# ============================================================
# SLIDE 7 - INDUSTRY IMPACT
# ============================================================

def create_impact_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Business & Industry Impact",
        "Potential implications for organizations and decision-makers"
    )

    content = find_section(
        sections,
        [
            "industry impact",
            "business impact",
            "industry",
            "impact"
        ]
    )

    bullets = extract_bullets(content, 6)

    if not bullets:
        bullets = [
            "Improved access to structured research intelligence.",
            "Faster identification of important market and technology trends.",
            "Better visibility into opportunities and risks.",
            "More consistent evidence-based decision support.",
            "Potential reduction in repetitive research work.",
            "Human review remains important for high-impact decisions."
        ]

    add_bullet_card(
        slide,
        0.8,
        1.55,
        7.0,
        4.95,
        "Industry Implications",
        bullets,
        BLUE
    )

    add_card(
        slide,
        8.2,
        1.55,
        4.1,
        1.45,
        "Decision Support",
        "Structured research can help decision-makers understand complex topics more efficiently.",
        GREEN
    )

    add_card(
        slide,
        8.2,
        3.25,
        4.1,
        1.45,
        "Efficiency",
        "Automating repetitive research tasks can reduce manual effort and improve consistency.",
        CYAN
    )

    add_card(
        slide,
        8.2,
        4.95,
        4.1,
        1.55,
        "Governance",
        "Evidence quality, privacy, security and human oversight remain important.",
        ORANGE
    )

    add_footer(slide, 7)


# ============================================================
# SLIDE 8 - SKILLS
# ============================================================

def create_skills_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Capabilities & Skills",
        "Capabilities needed to work effectively with AI-driven research"
    )

    content = find_section(
        sections,
        [
            "workforce",
            "skills",
            "capabilities",
            "talent"
        ]
    )

    bullets = extract_bullets(content, 6)

    if not bullets:
        bullets = [
            "Data analysis and interpretation",
            "AI and machine learning fundamentals",
            "Research and source evaluation",
            "Prompting and AI-assisted workflows",
            "Critical thinking and fact verification",
            "Communication and domain expertise"
        ]

    positions = [
        (0.8, 1.65),
        (4.45, 1.65),
        (8.1, 1.65),
        (0.8, 4.0),
        (4.45, 4.0),
        (8.1, 4.0)
    ]

    accents = [
        BLUE,
        CYAN,
        GREEN,
        PURPLE,
        ORANGE,
        RED
    ]

    for i, bullet in enumerate(bullets):

        x, y = positions[i]

        add_card(
            slide,
            x,
            y,
            3.45,
            1.85,
            "Capability",
            bullet,
            accents[i]
        )

    add_footer(slide, 8)


# ============================================================
# SLIDE 9 - RISKS
# ============================================================

def create_risks_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Risks & Challenges",
        "Key issues that should be considered during adoption"
    )

    content = find_section(
        sections,
        [
            "risks",
            "challenges",
            "limitations"
        ]
    )

    bullets = extract_bullets(content, 6)

    if not bullets:
        bullets = [
            "Data quality and incomplete evidence",
            "Integration and implementation complexity",
            "Privacy and cybersecurity concerns",
            "Potential model errors or hallucinations",
            "Workforce adoption and trust",
            "Need for human validation of important decisions"
        ]

    positions = [
        (0.8, 1.6),
        (4.45, 1.6),
        (8.1, 1.6),
        (0.8, 4.0),
        (4.45, 4.0),
        (8.1, 4.0)
    ]

    for i, bullet in enumerate(bullets):

        x, y = positions[i]

        add_card(
            slide,
            x,
            y,
            3.45,
            1.9,
            f"Risk {i + 1}",
            bullet,
            RED
        )

    add_footer(slide, 9)


# ============================================================
# SLIDE 10 - RESEARCH GAPS
# ============================================================

def create_gaps_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Research Gaps",
        "Areas where additional evidence or investigation may be required"
    )

    content = find_section(
        sections,
        [
            "research gaps",
            "gaps",
            "limitations"
        ]
    )

    bullets = extract_bullets(content, 6)

    if not bullets:
        bullets = [
            "Additional quantitative evidence may be required.",
            "Long-term effects require continued monitoring.",
            "Regional and industry-specific evidence may be limited.",
            "Emerging trends need further validation.",
            "Different scenarios should be compared.",
            "More longitudinal research may improve confidence."
        ]

    add_bullet_card(
        slide,
        1.0,
        1.65,
        11.3,
        4.9,
        "Areas for Further Research",
        bullets,
        PURPLE
    )

    add_footer(slide, 10)


# ============================================================
# SLIDE 11 - RECOMMENDATIONS
# ============================================================

def create_recommendations_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Strategic Recommendations",
        "Practical actions based on the research findings"
    )

    content = find_section(
        sections,
        [
            "strategic recommendations",
            "recommendations",
            "strategy"
        ]
    )

    bullets = extract_bullets(content, 8)

    if not bullets:
        bullets = [
            "Organizations should define clear objectives before adopting AI.",
            "Build strong data and governance foundations.",
            "Use human oversight for high-impact decisions.",
            "Invest in workforce AI and data skills.",
            "Evaluate systems using measurable outcomes.",
            "Monitor risks, security and privacy continuously.",
            "Use reliable sources and validate important claims.",
            "Scale successful AI workflows gradually."
        ]

    groups = [
        bullets[0:2],
        bullets[2:4],
        bullets[4:6],
        bullets[6:8]
    ]

    titles = [
        "For Organizations",
        "For Data Teams",
        "For Education",
        "For Professionals"
    ]

    accents = [
        BLUE,
        GREEN,
        PURPLE,
        ORANGE
    ]

    positions = [
        (0.8, 1.6),
        (6.7, 1.6),
        (0.8, 4.0),
        (6.7, 4.0)
    ]

    for i in range(4):

        x, y = positions[i]

        group = groups[i]

        if not group:
            group = [
                "Continue evidence-based evaluation and improvement."
            ]

        add_bullet_card(
            slide,
            x,
            y,
            5.7,
            1.95,
            titles[i],
            group,
            accents[i]
        )

    add_footer(slide, 11)


# ============================================================
# SLIDE 12 - CONCLUSION
# ============================================================

def create_conclusion_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide, NAVY)

    content = find_section(
        sections,
        [
            "conclusion",
            "evidence-based conclusion"
        ]
    )

    if not content:
        content = (
            "The research highlights important opportunities, "
            "risks and future directions. Evidence quality and "
            "human judgment remain essential when using AI-assisted "
            "research for decision-making."
        )

    add_text(
        slide,
        "CONCLUSION",
        0.9,
        1.0,
        4,
        0.5,
        17,
        CYAN,
        True
    )

    add_text(
        slide,
        shorten_text(content, 600),
        0.9,
        2.0,
        10.8,
        2.8,
        25,
        WHITE,
        True
    )

    add_text(
        slide,
        "ResearchX-AI",
        0.9,
        5.8,
        3,
        0.4,
        14,
        CYAN,
        True
    )

    add_text(
        slide,
        "PLAN  •  RESEARCH  •  VERIFY  •  SYNTHESIZE",
        0.9,
        6.35,
        6,
        0.35,
        10,
        RGBColor(203, 213, 225)
    )


# ============================================================
# SLIDE 13 - SOURCES
# ============================================================

def create_sources_slide(prs, sections):

    slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    add_background(slide)
    add_top_bar(slide)

    add_title(
        slide,
        "Sources",
        "Research sources referenced during analysis"
    )

    content = find_section(
        sections,
        [
            "sources",
            "references"
        ]
    )

    bullets = extract_bullets(content, 12)

    if not bullets:

        bullets = [
            "Sources collected through the ResearchX-AI web research workflow.",
            "Important claims should be reviewed against the original source URLs.",
            "Source quality and relevance were considered during fact checking."
        ]

    # Large source box
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8),
        Inches(1.55),
        Inches(11.7),
        Inches(5.25)
    )

    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = MID_GRAY

    text_box = slide.shapes.add_textbox(
        Inches(1.05),
        Inches(1.85),
        Inches(11.2),
        Inches(4.65)
    )

    tf = text_box.text_frame
    tf.clear()
    tf.word_wrap = True

    for i, item in enumerate(bullets):

        p = (
            tf.paragraphs[0]
            if i == 0
            else tf.add_paragraph()
        )

        p.text = f"[Source {i + 1}] {clean_text(item)}"

        p.font.name = FONT
        p.font.size = Pt(11)
        p.font.color.rgb = DARK
        p.space_after = Pt(9)

    add_footer(slide, 13)


# ============================================================
# MAIN POWERPOINT GENERATOR
# ============================================================

def create_professional_ppt(
    report_text,
    topic,
    filename="research_presentation.pptx"
):

    os.makedirs("outputs", exist_ok=True)

    filepath = os.path.join(
        "outputs",
        filename
    )

    prs = Presentation()

    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    # Parse final report
    sections = extract_sections(report_text)

    # --------------------------------------------------------
    # Create all 13 slides
    # --------------------------------------------------------

    create_cover_slide(
        prs,
        topic
    )

    create_summary_slide(
        prs,
        sections
    )

    create_methodology_slide(
        prs
    )

    create_findings_slide(
        prs,
        sections
    )

    create_evidence_slide(
        prs,
        sections
    )

    create_comparison_slide(
        prs,
        sections
    )

    create_impact_slide(
        prs,
        sections
    )

    create_skills_slide(
        prs,
        sections
    )

    create_risks_slide(
        prs,
        sections
    )

    create_gaps_slide(
        prs,
        sections
    )

    create_recommendations_slide(
        prs,
        sections
    )

    create_conclusion_slide(
        prs,
        sections
    )

    create_sources_slide(
        prs,
        sections
    )

    # Save
    prs.save(filepath)

    print(
        f"\nProfessional PowerPoint created: {filepath}"
    )

    return filepath
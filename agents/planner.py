import re


# ============================================================
# RESEARCH PLANNER AGENT
# ============================================================

def create_research_plan(topic: str):

    print("\n" + "=" * 60)
    print("RESEARCH PLANNER AGENT")
    print("=" * 60)

    topic = topic.strip()

    # --------------------------------------------------------
    # Detect broad research areas
    # --------------------------------------------------------

    topic_lower = topic.lower()

    areas = []

    if any(word in topic_lower for word in [
        "ai", "artificial intelligence", "machine learning",
        "generative ai", "deep learning", "automation"
    ]):
        areas.extend([
            "Technology and AI developments",
            "Applications and use cases",
            "Automation and productivity impact"
        ])

    if any(word in topic_lower for word in [
        "business", "company", "industry", "market",
        "manufacturing", "finance", "healthcare", "retail"
    ]):
        areas.extend([
            "Industry impact",
            "Business opportunities",
            "Implementation challenges"
        ])

    if any(word in topic_lower for word in [
        "job", "jobs", "employment", "workforce",
        "career", "skills"
    ]):
        areas.extend([
            "Workforce impact",
            "Skills and job-market changes",
            "Future career implications"
        ])

    if any(word in topic_lower for word in [
        "security", "privacy", "risk", "risks",
        "bias", "ethical", "ethics"
    ]):
        areas.extend([
            "Security and privacy",
            "Risks and challenges",
            "Ethical considerations"
        ])

    if any(word in topic_lower for word in [
        "future", "trend", "trends", "forecast",
        "growth", "development"
    ]):
        areas.extend([
            "Current trends",
            "Future outlook",
            "Potential developments"
        ])

    # --------------------------------------------------------
    # Default areas
    # --------------------------------------------------------

    if not areas:

        areas = [
            "Current state and developments",
            "Major trends",
            "Industry impact",
            "Opportunities",
            "Risks and challenges",
            "Future outlook"
        ]

    # Remove duplicates while preserving order

    unique_areas = []

    for area in areas:

        if area not in unique_areas:
            unique_areas.append(area)

    areas = unique_areas

    # --------------------------------------------------------
    # Create research questions
    # --------------------------------------------------------

    questions = [
        f"What is the current state of {topic}?",
        f"What are the major developments and trends related to {topic}?",
        f"What evidence and statistics are available?",
        f"What are the major benefits and opportunities?",
        f"What are the major risks and challenges?",
        f"How could {topic} develop in the future?"
    ]

    # --------------------------------------------------------
    # Create professional research plan
    # --------------------------------------------------------

    plan = f"""
RESEARCH PLAN

============================================================
RESEARCH TOPIC
============================================================

{topic}


============================================================
1. RESEARCH OBJECTIVE
============================================================

Investigate {topic} using reliable and recent web sources
to produce an evidence-based research report.

The research should identify important developments,
supporting evidence, industry implications, opportunities,
risks, challenges, and future directions.


============================================================
2. KEY RESEARCH QUESTIONS
============================================================

"""

    for index, question in enumerate(questions, start=1):

        plan += f"{index}. {question}\n"

    plan += """

============================================================
3. IMPORTANT SUBTOPICS
============================================================

"""

    for area in areas:

        plan += f"- {area}\n"

    plan += """

============================================================
4. RESEARCH METHODOLOGY
============================================================

The research should follow a structured evidence-based
workflow:

1. Search for relevant information using web research.
2. Collect multiple independent sources.
3. Prefer authoritative and reliable sources.
4. Compare information across sources.
5. Identify supporting evidence and statistics.
6. Identify conflicting viewpoints where available.
7. Separate confirmed facts from interpretation.
8. Identify research gaps and limitations.
9. Produce a balanced conclusion.


============================================================
5. SOURCE EVALUATION
============================================================

Sources should be evaluated based on:

- Authority
- Relevance
- Recency
- Evidence quality
- Consistency with other sources
- Transparency of information


============================================================
6. EXPECTED DELIVERABLES
============================================================

The final ResearchX-AI output should contain:

- Executive Summary
- Key Findings
- Evidence and Statistics
- Major Trends
- Different Viewpoints
- Industry Impact
- Opportunities
- Risks and Challenges
- Research Gaps
- Strategic Recommendations
- Conclusion
- Research Sources


============================================================
7. QUALITY REQUIREMENTS
============================================================

- Do not invent statistics.
- Do not create fake sources.
- Do not present unsupported claims as facts.
- Clearly distinguish evidence from interpretation.
- Identify uncertainty where evidence is insufficient.
- Prefer primary and authoritative sources.
- Maintain a professional consulting-company research style.
"""

    print("\nResearch plan created successfully.")
    print("Planner used: LOCAL RULE-BASED PLANNING")
    print("Gemini API call saved: 1")

    return plan
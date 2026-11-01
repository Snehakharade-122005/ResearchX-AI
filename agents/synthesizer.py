import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


# ============================================================
# GEMINI
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def limit_text(text, max_chars):
    """
    Prevent extremely large prompts from causing
    Gemini request/context failures.
    """

    if not text:
        return ""

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + (
        "\n\n[Additional content omitted because "
        "the input exceeded the safe context limit.]"
    )


# ============================================================
# SYNTHESIS AGENT
# ============================================================

def synthesize_research(research, fact_check):

    print("\n" + "=" * 60)
    print("SYNTHESIS AGENT")
    print("=" * 60)

    # --------------------------------------------------------
    # GET RESEARCH DATA
    # --------------------------------------------------------

    topic = research.get(
        "topic",
        "Unknown Topic"
    )

    research_analysis = research.get(
        "analysis",
        ""
    )

    research_plan = research.get(
        "research_plan",
        ""
    )

    sources = research.get(
        "sources",
        []
    )

    # --------------------------------------------------------
    # SAFELY LIMIT LARGE INPUTS
    # --------------------------------------------------------

    research_plan = limit_text(
        research_plan,
        12000
    )

    research_analysis = limit_text(
        research_analysis,
        30000
    )

    fact_check = limit_text(
        fact_check,
        30000
    )

    # --------------------------------------------------------
    # PREPARE SOURCE LIST
    # --------------------------------------------------------

    source_list = []

    for index, source in enumerate(
        sources,
        start=1
    ):

        title = source.get(
            "title",
            "Unknown Source"
        )

        url = source.get(
            "url",
            ""
        )

        source_list.append(
            f"{index}. {title}\n   {url}"
        )

    sources_text = "\n\n".join(
        source_list
    )

    # --------------------------------------------------------
    # LIMIT SOURCE LIST IF NECESSARY
    # --------------------------------------------------------

    sources_text = limit_text(
        sources_text,
        12000
    )

    # --------------------------------------------------------
    # FINAL REPORT PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are a senior research consultant working
for a professional technology consulting company.

Your task is to create a DETAILED, PROFESSIONAL,
EVIDENCE-BASED research report.

The report will be presented to students,
professionals, researchers, and business decision
makers.

Do NOT produce a short summary.

The final report should provide substantial
analysis while remaining clear and readable.

==================================================
RESEARCH TOPIC
==================================================

{topic}


==================================================
RESEARCH PLAN
==================================================

{research_plan}


==================================================
RESEARCH ANALYSIS
==================================================

{research_analysis}


==================================================
FACT CHECK REPORT
==================================================

{fact_check}


==================================================
AVAILABLE SOURCES
==================================================

{sources_text}


==================================================
IMPORTANT EVIDENCE RULE
==================================================

The Research Analysis contains information collected
from web sources.

The Fact Check Report evaluates the reliability
of important claims.

Use the Fact Check Report as a quality-control layer.

HIGH-confidence claims:
- Can be presented as supported findings.

MEDIUM-confidence claims:
- Present carefully using language such as
  "available evidence suggests".

LOW-confidence or unsupported claims:
- Do not present them as established facts.
- Remove them or clearly identify the uncertainty.

Never invent:
- statistics
- percentages
- market sizes
- dates
- research findings
- organizations
- URLs
- citations

If evidence is insufficient, explicitly say:

"Evidence is insufficient in the provided sources."


==================================================
SOURCE CITATIONS
==================================================

When presenting an important factual claim,
include the relevant source number.

Example:

AI adoption is increasing across healthcare
organizations. [Source 2]

Do not invent source numbers.

Use only the available source list.

==================================================
REPORT STRUCTURE
==================================================

Create the final report using the following
structure.

# Executive Summary

Write 4–6 substantial paragraphs.

Explain:

- What the research investigated
- The most important findings
- Major opportunities
- Major risks
- Overall conclusion

The executive summary should be useful to
a senior decision maker.

# Research Objective

Explain:

- Why the topic matters
- What the research investigates
- The main questions addressed
- The scope of the research

# Key Findings

Provide 8–12 important findings.

For each finding:

- Explain the finding
- Provide supporting evidence
- Add [Source X] when appropriate
- Clearly distinguish fact from interpretation

# Evidence & Statistics

Provide a detailed evidence section.

Include:

- Important statistics
- Market or adoption evidence when available
- Research findings
- Quantitative evidence
- Important factual observations

For each important item:

Evidence:
...

Source:
[Source X]

Confidence:
HIGH / MEDIUM / LOW

Do NOT invent statistics.

If the available sources contain no reliable
statistic for an area, say so.

# Major Trends

Explain 6–10 major trends.

For each trend:

1. Trend
2. Current evidence
3. Industry significance
4. Possible future direction

Clearly distinguish:

FACT
INTERPRETATION
PREDICTION

# Industry Impact

Analyze the impact on relevant industries.

Consider:

## Technology

Discuss technology adoption, AI systems,
automation, infrastructure, data, and software.

## Healthcare

Discuss healthcare applications only when
supported by the evidence.

## Finance

Discuss financial applications only when
supported by the evidence.

## Retail

Discuss retail applications only when
supported by the evidence.

## Other Relevant Industries

Include other industries only when relevant
to the research topic.

For each industry explain:

- Current impact
- Benefits
- Challenges
- Future implications

Do not force unrelated industries into the report.

# Workforce & Skills Impact

Provide detailed analysis of:

## Tasks likely to be automated

## Tasks likely to be augmented

## Skills becoming more important

## Changes in job roles

## Emerging roles

## Future workforce requirements

Clearly label predictions as predictions.

# Opportunities

Discuss opportunities for:

## Companies

## Technology Teams

## Data Science Teams

## Students

## Professionals

Explain practical opportunities rather than
only listing them.

# Risks & Challenges

Provide a detailed analysis of relevant risks.

Consider:

- AI hallucinations
- Data privacy
- Cybersecurity
- Algorithmic bias
- Intellectual property
- Model reliability
- Explainability
- Over-reliance on AI
- Regulatory concerns
- Data quality
- Integration challenges
- Human oversight

Only include risks relevant to the topic.

For each major risk explain:

Risk:
...

Why it matters:
...

Potential impact:
...

Possible mitigation:
...

# Research Gaps

Identify 6–10 important research gaps.

For each gap explain:

- What is currently unknown
- Why the gap matters
- What future research should investigate

# Strategic Recommendations

Provide practical recommendations.

## Companies

Give 6–8 recommendations.

## Data Science Teams

Give 6–8 technical and operational
recommendations.

## Universities

Give 5–7 education and curriculum
recommendations where relevant.

## Students and Professionals

Give 6–8 practical skill-development
recommendations.

Recommendations must be clearly identified as
recommendations, not facts.

# Conclusion

Write a balanced conclusion.

Summarize:

- Main findings
- Opportunities
- Risks
- Workforce implications
- Future direction

The conclusion must be based on available
evidence.

# Sources

List ALL available research sources.

Use exactly this format:

1. Source Title
   URL

2. Source Title
   URL

Continue for all available sources.

Do not remove sources merely because they were
not directly referenced in every section.

==================================================
WRITING REQUIREMENTS
==================================================

The final report should be:

- Detailed
- Professional
- Evidence-based
- Easy to understand
- Suitable for an academic project
- Suitable for a consulting report
- Useful for business decision making
- Useful for technical readers

Avoid:

- Repeating the same point
- Very short paragraphs
- Generic filler
- Unsupported claims
- Fake statistics
- Fake citations
- Fake URLs

Use:

- Clear headings
- Subheadings
- Bullet points
- Numbered recommendations
- Evidence labels
- Source references

==================================================
FINAL QUALITY CHECK
==================================================

Before returning the report verify:

1. The report is detailed enough to be useful.

2. Every important factual claim is supported
   by the provided research.

3. Statistics are not invented.

4. LOW-confidence claims are not presented
   as confirmed facts.

5. Predictions are clearly identified.

6. Recommendations are clearly identified.

7. Sources are included.

8. The report follows the requested structure.

9. The report contains substantial analysis.

10. The conclusion is consistent with the evidence.

Return ONLY the final research report.
"""


    # ========================================================
    # GENERATE REPORT
    # ========================================================

    print(
        "\nGenerating detailed final research report..."
    )

    try:

        response = llm.invoke(
            prompt
        )

        final_report = response.text

        print(
            "\nFinal report generated successfully."
        )

        return final_report

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "\nSynthesis Agent API Error:"
        )

        print(
            str(e)
        )

        print(
            "\nUsing fallback report."
        )

        # ----------------------------------------------------
        # FALLBACK REPORT
        # ----------------------------------------------------

        fallback_report = f"""
# Executive Summary

The research pipeline successfully collected
information about:

{topic}

However, the final AI synthesis could not be
completed because the Gemini API request failed.

The available research and fact-checking data
should therefore be reviewed before using the
findings for important decisions.

# Research Objective

The objective of this research was to investigate:

{topic}

The research pipeline collected information from
multiple web sources and passed the findings
through a fact-checking stage.

# Key Findings

The Research Agent successfully collected research
information.

However, the Synthesizer Agent was unable to
generate the final evidence-based analysis.

Therefore, the collected research should not
be treated as a finalized report.

# Evidence & Statistics

A complete evidence synthesis could not be
generated because the final Gemini request failed.

Statistics should be verified directly against
the original research sources.

# Major Trends

The research sources contain information about
current developments and trends related to:

{topic}

However, detailed synthesis was unavailable
because the final synthesis request failed.

# Industry Impact

Detailed industry impact analysis was not
completed.

# Workforce & Skills Impact

Detailed workforce analysis was not completed.

# Opportunities

Detailed opportunity analysis was not completed.

# Risks & Challenges

Detailed risk analysis was not completed.

# Research Gaps

A complete research-gap analysis could not be
generated.

# Strategic Recommendations

Recommendations should be developed after reviewing
the research findings and fact-check results.

# Conclusion

The research collection and fact-checking stages
completed, but the final synthesis stage failed.

The findings should therefore be considered
preliminary until the synthesis is successfully
generated.

# Sources

{sources_text}
"""

        return fallback_report
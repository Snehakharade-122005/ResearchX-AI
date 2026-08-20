import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)


def synthesize_research(research, fact_check):

    prompt = f"""
You are a senior research synthesis agent.

Your job is to create a professional, evidence-based research report
using the research findings and fact-check report below.

================ RESEARCH FINDINGS ================

{research["analysis"]}

================ FACT CHECK REPORT ================

{fact_check}

====================================================

Create a structured final research analysis.

Use this structure:

# Executive Summary

Give a concise overview of the most important findings.

# Key Findings

List the major findings and explain them clearly.

# Evidence & Statistics

Include only statistics and factual claims that have HIGH or MEDIUM
confidence from the fact-check report.

For every important statistic, mention its source.

# Major Trends

Explain the major trends identified by the research.

# Industry Impact

Discuss potential effects on:
- Technology
- Finance
- Healthcare
- Retail

Clearly distinguish evidence from interpretation.

# Workforce & Skills Impact

Explain:
- Which tasks are likely to be automated
- Which tasks will be augmented
- Which human skills become more important
- How data science roles may evolve

# Risks & Challenges

Discuss:
- Hallucinations
- Data privacy
- Security
- Bias
- Intellectual property
- Over-reliance on AI

# Research Gaps

Identify questions that cannot be answered using the current sources.

# Strategic Recommendations

Give practical recommendations for:
- Companies
- Data science teams
- Universities
- Students and professionals

# Conclusion

Provide a concise evidence-based conclusion.

IMPORTANT RULES:

1. Do not invent statistics.
2. Do not use unsupported claims.
3. Do not treat LOW-confidence claims as facts.
4. Clearly identify predictions and interpretations.
5. Prefer primary and authoritative sources when available.
6. Maintain a professional research-report style.
"""

    response = llm.invoke(prompt)

    return response.text
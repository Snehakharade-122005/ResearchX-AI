import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)


def fact_check_research(research_data):

    sources_text = ""

    for source in research_data["sources"]:
        sources_text += f"""
TITLE: {source['title']}
URL: {source['url']}
CONTENT:
{source['content']}

--------------------------------
"""

    prompt = f"""
You are a senior research fact-checking agent.

Research Topic:
{research_data['topic']}

Research Sources:
{sources_text}

Your task is to evaluate the research sources.

For each important claim:

1. Identify the claim.
2. Determine whether the source directly supports it.
3. Rate confidence as HIGH, MEDIUM, or LOW.
4. Identify the source supporting the claim.
5. Flag claims that appear unsupported or potentially misleading.

Return the result in this format:

FACT CHECK REPORT

Claim 1:
Claim:
Evidence:
Source:
Confidence:
Reason:

Claim 2:
Claim:
Evidence:
Source:
Confidence:
Reason:

Then provide:

OVERALL SOURCE QUALITY:
- Strongly Supported Claims:
- Partially Supported Claims:
- Unsupported Claims:
- Potential Issues:

IMPORTANT:
Do not invent evidence.
If the provided sources do not support a claim, explicitly say:
"Insufficient evidence in provided sources."
"""

    try:
        response = llm.invoke(prompt)
        return response.text

    except Exception as e:
        print("\n⚠️ Fact Checker API Error")
        print("Gemini API quota may have been exceeded.")
        print("Using a fallback fact-check result so the pipeline can continue.")

        return """
FACT CHECK REPORT

Overall Status:
Fact checking could not be completed because the Gemini API quota
was exceeded.

IMPORTANT:
The research claims have NOT been independently verified by the
Fact Checker Agent.

OVERALL SOURCE QUALITY:
- Strongly Supported Claims: Not evaluated
- Partially Supported Claims: Not evaluated
- Unsupported Claims: Not evaluated
- Potential Issues: API quota exceeded

The next Synthesis Agent should treat the research findings as
unverified and avoid presenting unsupported claims as confirmed facts.
"""
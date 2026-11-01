import os
import time

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI
# ============================================================

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.1
)


# ============================================================
# GEMINI CALL WITH RETRY
# ============================================================

def call_gemini(prompt, max_retries=3):

    for attempt in range(max_retries):

        try:

            response = llm.invoke(prompt)

            return response.text

        except Exception as e:

            error_message = str(e)

            print(
                f"\nGemini request failed "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            print(error_message)

            # Retry temporary API problems
            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                if attempt < max_retries - 1:

                    wait_time = 3 * (attempt + 1)

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    print(
                        "\nGemini could not be reached "
                        "after multiple attempts."
                    )

            else:

                # Do not retry unrelated errors
                break

    return None


# ============================================================
# FACT CHECKER AGENT
# ============================================================

def fact_check_research(research_data):

    print("\n" + "=" * 60)
    print("FACT CHECKER AGENT")
    print("=" * 60)


    # ========================================================
    # GET RESEARCH INFORMATION
    # ========================================================

    topic = research_data.get(
        "topic",
        "Unknown Topic"
    )

    analysis = research_data.get(
        "analysis",
        ""
    )

    sources = research_data.get(
        "sources",
        []
    )


    # ========================================================
    # LIMIT ANALYSIS SIZE
    # ========================================================

    analysis = analysis[:25000]


    # ========================================================
    # PREPARE SOURCE INFORMATION
    # ========================================================

    source_sections = []

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

        content = source.get(
            "content",
            ""
        )

        # Prevent unnecessarily large prompts
        content = content[:4000]

        source_sections.append(
            f"""
SOURCE {index}

TITLE:
{title}

URL:
{url}

CONTENT:
{content}
"""
        )


    sources_text = "\n\n".join(
        source_sections
    )


    # ========================================================
    # HANDLE NO SOURCES
    # ========================================================

    if not sources:

        return """
FACT CHECK REPORT

Overall Status:
No web sources were available for fact checking.

Strongly Supported Claims:
None.

Partially Supported Claims:
None.

Unsupported Claims:
The research could not be verified because
no sources were collected.

Potential Issues:
Insufficient source evidence.
"""


    # ========================================================
    # FACT CHECK PROMPT
    # ========================================================

    prompt = f"""
You are a senior fact-checking analyst working
for a professional technology consulting company.

Your task is to evaluate the research findings
against the provided web sources.

==================================================
RESEARCH TOPIC
==================================================

{topic}

==================================================
RESEARCH ANALYSIS
==================================================

{analysis}

==================================================
WEB SOURCES
==================================================

{sources_text}

==================================================
FACT CHECKING TASK
==================================================

Identify the most important factual claims in
the research analysis.

For each important claim:

1. State the claim.
2. Identify the evidence supporting it.
3. Identify the source supporting the evidence.
4. Give a confidence level:
   HIGH
   MEDIUM
   LOW
5. Explain why you assigned that confidence.

Use this format:

FACT CHECK REPORT

Claim 1:

Claim:
...

Evidence:
...

Source:
Source X

Confidence:
HIGH / MEDIUM / LOW

Reason:
...


Claim 2:

Claim:
...

Evidence:
...

Source:
Source X

Confidence:
HIGH / MEDIUM / LOW

Reason:
...


==================================================
OVERALL SOURCE QUALITY
==================================================

Provide:

Strongly Supported Claims:
- ...

Partially Supported Claims:
- ...

Unsupported Claims:
- ...

Potential Issues:
- ...


==================================================
IMPORTANT RULES
==================================================

1. Do not invent evidence.

2. Do not invent sources.

3. Do not create statistics that are not
   present in the provided sources.

4. HIGH confidence should only be used when
   the provided source directly supports the claim.

5. MEDIUM confidence should be used when
   evidence is relevant but incomplete or indirect.

6. LOW confidence should be used when evidence
   is weak, unclear, contradictory, or unsupported.

7. If the sources do not support a claim, write:

"Insufficient evidence in provided sources."

8. Clearly distinguish factual evidence from
   interpretation or prediction.

9. Prefer authoritative and primary sources.

10. Be conservative when assigning confidence.

11. Do not treat predictions as established facts.

12. Do not add information from outside the
    provided sources.

Return only the professional fact-check report.
"""


    # ========================================================
    # RUN GEMINI
    # ========================================================

    print("\nChecking research claims...")


    result = call_gemini(
        prompt,
        max_retries=3
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    if result:

        print(
            "\nFact checking completed successfully."
        )

        return result


    # ========================================================
    # FALLBACK
    # ========================================================

    print(
        "\nFact checking could not be completed "
        "because Gemini was temporarily unavailable."
    )

    print(
        "\nUsing fallback fact-check result."
    )


    return """
FACT CHECK REPORT

Overall Status:

Fact checking could not be completed because
the Gemini API was temporarily unavailable.

The research findings have NOT been independently
verified by the Fact Checker Agent.

==================================================
OVERALL SOURCE QUALITY
==================================================

Strongly Supported Claims:

Not evaluated.


Partially Supported Claims:

Not evaluated.


Unsupported Claims:

Not evaluated.


Potential Issues:

The Fact Checker Agent could not complete its
verification because the Gemini API request failed.

The available research should therefore be treated
as unverified.

IMPORTANT:

The Synthesizer Agent must not present unsupported
claims as confirmed facts.
"""
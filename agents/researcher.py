import os
import time
import random

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# TAVILY
# ==================================================

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    print("WARNING: TAVILY_API_KEY is not configured.")

tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ==================================================
# GEMINI CONFIGURATION
# ==================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

# Optional fallback model.
# You can add this to .env later if needed.
GEMINI_FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    ""
)


# ==================================================
# CREATE GEMINI MODEL
# ==================================================

def create_gemini_model(model_name):

    if not GOOGLE_API_KEY:
        print("WARNING: GOOGLE_API_KEY is not configured.")
        return None

    try:

        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2
        )

    except Exception as e:

        print(
            f"Could not initialize Gemini model "
            f"{model_name}: {e}"
        )

        return None


# ==================================================
# CREATE SEARCH QUERIES
# ==================================================

def create_search_queries(topic: str):

    topic = topic.strip()

    queries = [

        f"{topic} current trends and recent developments",

        f"{topic} industry impact and business effects",

        f"{topic} opportunities risks and challenges",

        f"{topic} future outlook research statistics"

    ]

    return queries


# ==================================================
# CHECK WHETHER ERROR IS TEMPORARY
# ==================================================

def is_temporary_gemini_error(error_message):

    error_message = error_message.lower()

    temporary_errors = [

        "503",
        "unavailable",
        "429",
        "resource_exhausted",
        "rate limit",
        "too many requests",
        "overloaded",
        "temporarily unavailable",
        "service unavailable",
        "deadline exceeded",
        "timeout"

    ]

    return any(
        error in error_message
        for error in temporary_errors
    )


# ==================================================
# GEMINI CALL WITH ROBUST RETRY
# ==================================================

def call_gemini(prompt, model_name, max_retries=4):

    print(
        f"\nTrying Gemini model: {model_name}"
    )

    llm = create_gemini_model(model_name)

    if llm is None:
        return None

    for attempt in range(max_retries):

        try:

            print(
                f"Gemini attempt "
                f"{attempt + 1}/{max_retries}"
            )

            response = llm.invoke(prompt)

            if response and response.text:

                print(
                    "\nGemini analysis completed successfully."
                )

                return response.text

            print(
                "Gemini returned an empty response."
            )

        except Exception as e:

            error_message = str(e)

            print(
                f"\nGemini request failed "
                f"(attempt {attempt + 1}/{max_retries})"
            )

            print(error_message)

            # Only retry temporary errors
            if not is_temporary_gemini_error(
                error_message
            ):

                print(
                    "\nThis does not look like a temporary "
                    "Gemini error. Stopping retries."
                )

                break

            if attempt < max_retries - 1:

                # Exponential backoff
                wait_time = min(
                    20,
                    (2 ** attempt) * 3
                )

                # Small random delay
                wait_time += random.uniform(
                    0.5,
                    1.5
                )

                print(
                    f"Temporary Gemini error."
                )

                print(
                    f"Waiting approximately "
                    f"{wait_time:.1f} seconds before retry..."
                )

                time.sleep(wait_time)

            else:

                print(
                    "\nGemini could not be reached "
                    "after multiple attempts."
                )

    return None


# ==================================================
# RUN GEMINI WITH OPTIONAL FALLBACK MODEL
# ==================================================

def run_gemini_analysis(prompt):

    # --------------------------------------------------
    # FIRST MODEL
    # --------------------------------------------------

    analysis = call_gemini(
        prompt,
        GEMINI_MODEL,
        max_retries=4
    )

    if analysis:

        return analysis, GEMINI_MODEL


    # --------------------------------------------------
    # OPTIONAL FALLBACK MODEL
    # --------------------------------------------------

    if (
        GEMINI_FALLBACK_MODEL
        and GEMINI_FALLBACK_MODEL != GEMINI_MODEL
    ):

        print(
            "\nPrimary Gemini model failed."
        )

        print(
            f"Trying fallback model: "
            f"{GEMINI_FALLBACK_MODEL}"
        )

        analysis = call_gemini(
            prompt,
            GEMINI_FALLBACK_MODEL,
            max_retries=3
        )

        if analysis:

            return (
                analysis,
                GEMINI_FALLBACK_MODEL
            )


    return None, None


# ==================================================
# RESEARCH AGENT
# ==================================================

def research_topic(
    topic: str,
    research_plan: str = ""
):

    print("\n")
    print("=" * 60)
    print("RESEARCHER AGENT")
    print("=" * 60)

    print(
        "\nCreating focused research queries...\n"
    )


    # ==================================================
    # CREATE SEARCH QUERIES LOCALLY
    # ==================================================

    queries = create_search_queries(topic)

    print("Search queries:")

    for query in queries:

        print(
            "-",
            query
        )


    # ==================================================
    # SEARCH WEB USING TAVILY
    # ==================================================

    sources = []

    for query in queries:

        print(
            f"\nSearching: {query}"
        )

        try:

            search_results = tavily.search(
                query=query[:1400],
                search_depth="advanced",
                max_results=5
            )

            results = search_results.get(
                "results",
                []
            )

            for result in results:

                source = {

                    "title": result.get(
                        "title",
                        "Unknown Source"
                    ),

                    "url": result.get(
                        "url",
                        ""
                    ),

                    "content": result.get(
                        "content",
                        ""
                    )

                }

                if source["url"]:

                    sources.append(
                        source
                    )

        except Exception as e:

            print(
                f"Tavily search failed: {e}"
            )


    # ==================================================
    # REMOVE DUPLICATE SOURCES
    # ==================================================

    unique_sources = {}

    for source in sources:

        url = source.get(
            "url"
        )

        if (
            url
            and url not in unique_sources
        ):

            unique_sources[url] = source


    sources = list(
        unique_sources.values()
    )


    print(
        f"\nCollected "
        f"{len(sources)} unique research sources."
    )


    # ==================================================
    # HANDLE NO SOURCES
    # ==================================================

    if not sources:

        print(
            "\nNo research sources were collected."
        )

        return {

            "topic": topic,

            "research_plan": research_plan,

            "analysis": (
                "No web sources were available "
                "for this research topic."
            ),

            "sources": []

        }


    # ==================================================
    # LIMIT SOURCE CONTENT
    # ==================================================

    source_sections = []

    for index, source in enumerate(
        sources,
        start=1
    ):

        content = source.get(
            "content",
            ""
        )

        # Keep prompts within a reasonable size
        content = content[:4500]

        source_sections.append(

            f"""
==================================================
SOURCE {index}
==================================================

TITLE:
{source.get("title", "Unknown Source")}

URL:
{source.get("url", "")}

CONTENT:
{content}
"""

        )


    research_text = "\n\n".join(
        source_sections
    )


    # ==================================================
    # GEMINI RESEARCH ANALYSIS PROMPT
    # ==================================================

    prompt = f"""

You are a senior research analyst working for a
professional technology consulting company.

==================================================
RESEARCH TOPIC
==================================================

{topic}


==================================================
RESEARCH PLAN
==================================================

{research_plan}


==================================================
WEB SOURCES
==================================================

{research_text}


==================================================
TASK
==================================================

Analyze the provided web sources according to
the research topic and research plan.

Create a structured research analysis containing:

1. Key Findings

2. Important Statistics and Facts

3. Major Trends

4. Different or Conflicting Viewpoints

5. Industry Impact

6. Opportunities

7. Risks and Challenges

8. Research Gaps

9. Evidence-Based Conclusion


==================================================
IMPORTANT EVIDENCE RULES
==================================================

- Use ONLY information supported by the provided sources.

- Do NOT invent statistics.

- Do NOT create fake sources.

- Do NOT assume information that is not present
  in the sources.

- Clearly distinguish facts from interpretation.

- If sources disagree, explain the disagreement.

- If evidence is insufficient, explicitly say so.

- Do not present predictions as confirmed facts.

- Prioritize reliable and authoritative sources.

- Give greater weight to government sources,
  academic research, peer-reviewed studies,
  universities, and established research organizations.

- Treat blogs and commercial websites as secondary
  sources unless their information is supported
  by stronger evidence.

- Mention the source number when reporting an
  important fact or statistic.

Example:

According to Source 14, employment of data scientists
is projected to increase by ...

- Do not include unsupported claims.

- Keep the analysis professional, clear and concise.

==================================================
OUTPUT REQUIREMENT
==================================================

The final analysis will be passed to a Fact Checker
Agent.

Therefore, clearly identify:

FACTS
EVIDENCE
INTERPRETATIONS
UNCERTAINTIES
CONFLICTING CLAIMS

Do not hide uncertainty.
"""


    # ==================================================
    # CALL GEMINI
    # ==================================================

    print(
        "\nAnalyzing research with Gemini..."
    )

    analysis, used_model = run_gemini_analysis(
        prompt
    )


    # ==================================================
    # SUCCESS
    # ==================================================

    if analysis:

        print(
            "\nResearch analysis successfully "
            "generated by Gemini."
        )

        print(
            f"Gemini model used: {used_model}"
        )

        final_analysis = f"""

RESEARCH ANALYSIS

Status:
Completed successfully using Gemini.

Gemini Model:
{used_model}

The analysis below was generated from the
web sources collected by the Researcher Agent.

--------------------------------------------------

{analysis}

--------------------------------------------------

Source verification will be performed by the
Fact Checker Agent.
"""


        return {

            "topic": topic,

            "research_plan": research_plan,

            "analysis": final_analysis,

            "sources": sources

        }


    # ==================================================
    # FALLBACK IF GEMINI FAILS
    # ==================================================

    print(
        "\nGemini analysis could not be generated."
    )

    print(
        "Returning collected sources without "
        "AI synthesis."
    )


    fallback_sections = []

    for index, source in enumerate(
        sources,
        start=1
    ):

        fallback_sections.append(

            f"""
SOURCE {index}

Title:
{source.get("title", "Unknown Source")}

URL:
{source.get("url", "")}

Source Summary:
{source.get("content", "")[:1500]}
"""

        )


    analysis = f"""

RESEARCH ANALYSIS

Status:
Gemini research analysis could not be completed.

Reason:
The Gemini API was temporarily unavailable
or the configured Gemini model could not complete
the request.

IMPORTANT:
The sources below were successfully collected
using Tavily, but they have NOT been synthesized
or independently fact-checked by Gemini.

Therefore, these source summaries must NOT be
treated as verified conclusions.

Collected Sources:

{chr(10).join(fallback_sections)}

The Fact Checker Agent should treat all findings
as requiring verification before they are presented
as confirmed conclusions.
"""


    # ==================================================
    # RETURN RESEARCH DATA
    # ==================================================

    print(
        "\nResearch Agent completed."
    )

    return {

        "topic": topic,

        "research_plan": research_plan,

        "analysis": analysis,

        "sources": sources

    }
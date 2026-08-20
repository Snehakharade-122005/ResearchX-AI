import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Tavily Web Search
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)


def research_topic(topic: str):

    print("\n🔎 Searching the web...\n")

    search_results = tavily.search(
        query=topic,
        search_depth="advanced",
        max_results=5
    )

    sources = []

    for result in search_results["results"]:
        sources.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content")
        })

    research_text = "\n\n".join(
        f"""
SOURCE: {source['title']}
URL: {source['url']}

CONTENT:
{source['content']}
"""
        for source in sources
    )

    prompt = f"""
You are an expert research analyst.

Research topic:
{topic}

Below are real web search results:

{research_text}

Analyze the sources and provide:

1. Key findings
2. Important statistics or facts
3. Major trends
4. Conflicting viewpoints
5. Research gaps
6. Evidence-based conclusion

IMPORTANT:
- Do not invent information.
- Only use information supported by the provided sources.
- Clearly distinguish facts from interpretation.
"""

    print("🧠 Analyzing research...\n")

    response = llm.invoke(prompt)

    return {
        "topic": topic,
        "analysis": response.text,
        "sources": sources
    }
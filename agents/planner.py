import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

def create_research_plan(topic: str):
    prompt = f"""
You are a senior AI research strategist working for a technology consulting company.

Create a detailed research plan for this topic:

{topic}

Return:
1. Research objective
2. Key questions to investigate
3. Important subtopics
4. Recommended research methodology
5. Expected final deliverables

Make the plan professional and suitable for a business research report.
"""

    response = llm.invoke(prompt)
    return response.text
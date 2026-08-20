from agents.researcher import research_topic
from agents.fact_checker import fact_check_research


topic = input("Enter research topic: ")

print("\n🔎 Running Researcher Agent...\n")

research = research_topic(topic)

print("\n✅ Research completed.")

print("\n🔍 Running Fact Checker Agent...\n")

fact_check = fact_check_research(research)

print("\n" + "=" * 60)
print("FACT CHECK REPORT")
print("=" * 60)

print(fact_check)
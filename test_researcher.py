from agents.researcher import research_topic

topic = input("Enter research topic: ")

result = research_topic(topic)

print("\n" + "=" * 60)
print("RESEARCH FINDINGS")
print("=" * 60)

print(result["analysis"])

print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)

for source in result["sources"]:
    print(f"\nTitle: {source['title']}")
    print(f"URL: {source['url']}")
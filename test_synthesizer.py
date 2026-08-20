from agents.researcher import research_topic
from agents.fact_checker import fact_check_research
from agents.synthesizer import synthesize_research
from report_generator import create_pdf_report
from ppt_generator import create_professional_ppt


topic = input("Enter research topic: ")

print("\n🔎 STEP 1: Researcher Agent")
research = research_topic(topic)

print("\n🛡️ STEP 2: Fact Checker Agent")
fact_check = fact_check_research(research)

print("\n🧠 STEP 3: Synthesis Agent")
final_report = synthesize_research(research, fact_check)

print("\n" + "=" * 70)
print("FINAL SYNTHESIZED RESEARCH REPORT")
print("=" * 70)

print(final_report)

print("\n📄 STEP 4: Generating PDF report...")
pdf_path = create_pdf_report(final_report)

print("\n✅ PDF REPORT CREATED!")
print(f"📁 Location: {pdf_path}")

print("\n📊 STEP 5: Generating Professional PowerPoint presentation...")

ppt_path = create_professional_ppt(
    final_report,
    topic
)

print("\n✅ PROFESSIONAL POWERPOINT CREATED!")
print(f"📁 Location: {ppt_path}")

from flask import Flask, request, jsonify
from flask_cors import CORS

from agents.researcher import research_topic
from agents.fact_checker import fact_check_research
from agents.synthesizer import synthesize_research

from report_generator import create_pdf_report
from ppt_generator import create_professional_ppt


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)

# Allow requests from frontend
CORS(app)


# --------------------------------------------------
# HOME / HEALTH CHECK
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "ResearchX-AI backend is running"
    })


# --------------------------------------------------
# RESEARCH API
# --------------------------------------------------

@app.route("/research", methods=["POST"])
def research():

    data = request.get_json(silent=True)

    if not data or "topic" not in data:
        return jsonify({
            "success": False,
            "error": "Research topic is required"
        }), 400

    topic = data["topic"].strip()

    if not topic:
        return jsonify({
            "success": False,
            "error": "Research topic cannot be empty"
        }), 400

    try:

        # ------------------------------------------
        # STEP 1 — RESEARCHER
        # ------------------------------------------

        print("\n STEP 1: Researcher Agent")

        research_data = research_topic(topic)

        print(" Research completed")


        # ------------------------------------------
        # STEP 2 — FACT CHECKER
        # ------------------------------------------

        print("\n STEP 2: Fact Checker Agent")

        fact_check = fact_check_research(research_data)

        print(" Fact checking completed")


        # ------------------------------------------
        # STEP 3 — SYNTHESIS
        # ------------------------------------------

        print("\n STEP 3: Synthesis Agent")

        final_report = synthesize_research(
            research_data,
            fact_check
        )

        print(" Research synthesis completed")


        # ------------------------------------------
        # STEP 4 — PDF
        # ------------------------------------------

        print("\n STEP 4: Generating PDF")

        pdf_path = create_pdf_report(
            final_report
        )

        print(f" PDF created: {pdf_path}")


        # ------------------------------------------
        # STEP 5 — POWERPOINT
        # ------------------------------------------

        print("\n STEP 5: Generating PowerPoint")

        ppt_path = create_professional_ppt(
            final_report,
            topic
        )

        print(f" PowerPoint created: {ppt_path}")


        # ------------------------------------------
        # FINAL RESPONSE
        # ------------------------------------------

        print("\n Research completed successfully!")

        return jsonify({
            "success": True,
            "topic": topic,
            "report": final_report,
            "pdf": pdf_path,
            "ppt": ppt_path
        })


    except Exception as e:

        print("\n ERROR:")
        print(str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


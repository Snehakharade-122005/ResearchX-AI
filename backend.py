
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

from agents.planner import create_research_plan
from agents.researcher import research_topic
from agents.fact_checker import fact_check_research
from agents.synthesizer import synthesize_research

from report_generator import create_pdf_report
from ppt_generator import create_professional_ppt


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

# Allow frontend to communicate with Flask backend
CORS(app)


# ============================================================
# HOME / HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "ResearchX-AI backend is running"
    })


# ============================================================
# RESEARCH API
# ============================================================

@app.route("/research", methods=["POST"])
def research():

    data = request.get_json(silent=True)

    # --------------------------------------------------------
    # Validate request
    # --------------------------------------------------------

    if not data or "topic" not in data:

        return jsonify({
            "success": False,
            "error": "Research topic is required"
        }), 400


    topic = str(data["topic"]).strip()


    if not topic:

        return jsonify({
            "success": False,
            "error": "Research topic cannot be empty"
        }), 400


    try:

        # ====================================================
        # STEP 1 — RESEARCH PLANNER
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 1: RESEARCH PLANNER")
        print("=" * 60)

        research_plan = create_research_plan(topic)

        print("Research plan created successfully.")


        # ====================================================
        # STEP 2 — RESEARCHER AGENT
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 2: RESEARCHER AGENT")
        print("=" * 60)

        research_data = research_topic(
            topic,
            research_plan
        )

        print("Research completed successfully.")


        # ====================================================
        # STEP 3 — FACT CHECKER
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 3: FACT CHECKER AGENT")
        print("=" * 60)

        fact_check = fact_check_research(
            research_data
        )

        print("Fact checking completed successfully.")


        # ====================================================
        # STEP 4 — SYNTHESIS
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 4: SYNTHESIS AGENT")
        print("=" * 60)

        final_report = synthesize_research(
            research_data,
            fact_check
        )

        print("Research synthesis completed successfully.")


        # ====================================================
        # STEP 5 — PDF
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 5: PDF GENERATION")
        print("=" * 60)

        pdf_path = create_pdf_report(
            final_report
        )

        print(f"PDF created: {pdf_path}")


        # ====================================================
        # STEP 6 — POWERPOINT
        # ====================================================

        print("\n" + "=" * 60)
        print("STEP 6: POWERPOINT GENERATION")
        print("=" * 60)

        ppt_path = create_professional_ppt(
            final_report,
            topic
        )

        print(f"PowerPoint created: {ppt_path}")


        # ====================================================
        # VERIFY GENERATED FILES
        # ====================================================

        if not os.path.exists(pdf_path):

            raise FileNotFoundError(
                f"PDF file was not found: {pdf_path}"
            )


        if not os.path.exists(ppt_path):

            raise FileNotFoundError(
                f"PowerPoint file was not found: {ppt_path}"
            )


        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        print("\n" + "=" * 60)
        print("RESEARCH COMPLETED SUCCESSFULLY")
        print("=" * 60)


        return jsonify({

            "success": True,

            "topic": topic,

            "research_plan": research_plan,

            "report": final_report,

            "pdf": pdf_path,

            "ppt": ppt_path

        })


    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)

        print(str(e))


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# PDF DOWNLOAD
# ============================================================

@app.route("/download/pdf", methods=["GET"])
def download_pdf():

    try:

        path = request.args.get("path")


        if not path:

            return jsonify({
                "success": False,
                "error": "PDF path is required"
            }), 400


        if not os.path.exists(path):

            return jsonify({
                "success": False,
                "error": f"PDF file not found: {path}"
            }), 404


        return send_file(

            path,

            as_attachment=True,

            download_name="ResearchX_AI_Report.pdf",

            mimetype="application/pdf"

        )


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# POWERPOINT DOWNLOAD
# ============================================================

@app.route("/download/ppt", methods=["GET"])
def download_ppt():

    try:

        path = request.args.get("path")


        if not path:

            return jsonify({
                "success": False,
                "error": "PowerPoint path is required"
            }), 400


        if not os.path.exists(path):

            return jsonify({
                "success": False,
                "error": f"PowerPoint file not found: {path}"
            }), 404


        return send_file(

            path,

            as_attachment=True,

            download_name="ResearchX_AI_Presentation.pptx",

            mimetype=(
                "application/vnd.openxmlformats-"
                "officedocument.presentationml.presentation"
            )

        )


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )


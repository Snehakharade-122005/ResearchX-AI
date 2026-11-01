import streamlit as st
import os
from datetime import datetime

from agents.planner import create_research_plan
from agents.researcher import research_topic
from agents.fact_checker import fact_check_research
from agents.synthesizer import synthesize_research

from report_generator import create_pdf_report
from ppt_generator import create_professional_ppt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResearchX-AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* MAIN TEXT */

    .stApp p,
    .stApp li,
    .stApp label {
        color: #1e293b;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #0f172a;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    /* TITLES */

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 3px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #0f172a;
        margin-top: 30px;
        margin-bottom: 8px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* CURRENT RESEARCH CARD */

    .current-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 22px;
        margin-top: 10px;
    }

    .current-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    .current-topic {
        color: #0f172a;
        font-size: 20px;
        font-weight: 700;
        margin-top: 7px;
    }

    /* STATUS */

    [data-testid="stStatusWidget"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }

    /* INPUT */

    input {
        color: #0f172a !important;
    }

    /* FOOTER */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "research_plan": None,
    "research": None,
    "fact_check": None,
    "final_report": None,
    "pdf_path": None,
    "ppt_path": None,
    "research_history": [],
    "research_topic": "",
    "page": "Overview"
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_research():

    st.session_state.research_plan = None
    st.session_state.research = None
    st.session_state.fact_check = None
    st.session_state.final_report = None
    st.session_state.pdf_path = None
    st.session_state.ppt_path = None


def get_source_count():

    if st.session_state.research:

        return len(
            st.session_state.research.get(
                "sources",
                []
            )
        )

    return 0


def save_history(topic):

    history_item = {
        "topic": topic,
        "date": datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        ),
        "sources": get_source_count()
    }

    st.session_state.research_history.insert(
        0,
        history_item
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔬 ResearchX-AI")

    st.caption(
        "Multi-Agent Research Intelligence"
    )

    st.divider()

    pages = [
        "Overview",
        "New Research",
        "Research History",
        "Reports",
        "Analytics"
    ]

    page = st.radio(
        "Navigation",
        pages,
        index=pages.index(
            st.session_state.page
        ),
        label_visibility="collapsed"
    )

    st.session_state.page = page

    st.divider()

    st.markdown("### AI Pipeline")

    st.write("01  Planner Agent")
    st.write("02  Research Agent")
    st.write("03  Fact Checker")
    st.write("04  Synthesizer")

    st.divider()

    st.caption("ResearchX-AI v1.0")


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">ResearchX-AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'AI-powered research, verification and professional report generation'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW
# ============================================================

if st.session_state.page == "Overview":

    st.markdown(
        '<div class="section-title">Research Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Monitor your research projects and AI agent pipeline.'
        '</div>',
        unsafe_allow_html=True
    )

    total_projects = len(
        st.session_state.research_history
    )

    total_sources = get_source_count()

    total_reports = (
        1
        if st.session_state.final_report
        else 0
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Research Projects",
            total_projects
        )

    with col2:

        st.metric(
            "Sources Collected",
            total_sources
        )

    with col3:

        st.metric(
            "Reports Generated",
            total_reports
        )

    with col4:

        st.metric(
            "AI Agents",
            4
        )


    # ========================================================
    # AI PIPELINE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'AI Research Pipeline'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Four specialized agents transform a research topic '
        'into a verified professional report.'
        '</div>',
        unsafe_allow_html=True
    )


    agent1, agent2, agent3, agent4 = st.columns(4)


    # ========================================================
    # AGENT 01
    # ========================================================

    with agent1:

        st.markdown("#### AGENT 01")

        st.markdown("### Planner Agent")

        st.write(
            "Creates the research objective, "
            "questions, subtopics and methodology."
        )

        if st.session_state.research_plan:

            st.success("✓ Completed")

        else:

            st.info("Waiting")


    # ========================================================
    # AGENT 02
    # ========================================================

    with agent2:

        st.markdown("#### AGENT 02")

        st.markdown("### Research Agent")

        st.write(
            "Searches the web, collects sources "
            "and analyzes research evidence."
        )

        if st.session_state.research:

            st.success("✓ Completed")

        else:

            st.info("Waiting")


    # ========================================================
    # AGENT 03
    # ========================================================

    with agent3:

        st.markdown("#### AGENT 03")

        st.markdown("### Fact Checker")

        st.write(
            "Evaluates important claims against "
            "the collected research sources."
        )

        if st.session_state.fact_check:

            st.success("✓ Completed")

        else:

            st.info("Waiting")


    # ========================================================
    # AGENT 04
    # ========================================================

    with agent4:

        st.markdown("#### AGENT 04")

        st.markdown("### Synthesizer")

        st.write(
            "Combines verified findings into "
            "a detailed professional report."
        )

        if st.session_state.final_report:

            st.success("✓ Completed")

        else:

            st.info("Waiting")


    # ========================================================
    # CURRENT RESEARCH
    # ========================================================

    if st.session_state.research_topic:

        st.markdown(
            '<div class="section-title">'
            'Current Research'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="current-card">

                <div class="current-label">
                    ACTIVE RESEARCH TOPIC
                </div>

                <div class="current-topic">
                    {st.session_state.research_topic}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="section-title">'
            'Start Your First Research'
            '</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Enter a topic and let ResearchX-AI "
            "plan, research, verify and synthesize the results."
        )

        if st.button(
            "Start New Research",
            type="primary"
        ):

            st.session_state.page = "New Research"

            st.rerun()


# ============================================================
# NEW RESEARCH
# ============================================================

elif st.session_state.page == "New Research":

    st.markdown(
        '<div class="section-title">'
        'New Research'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Start a complete multi-agent research workflow.'
        '</div>',
        unsafe_allow_html=True
    )


    topic = st.text_input(
        "Research Topic",
        placeholder=(
            "Example: Impact of Generative AI on Data Science Jobs"
        )
    )


    start_button = st.button(
        "Start Research",
        type="primary",
        use_container_width=True
    )


    if start_button:

        if not topic.strip():

            st.error(
                "Please enter a research topic."
            )

        else:

            reset_research()

            st.session_state.research_topic = (
                topic.strip()
            )


            try:

                # ==================================================
                # PIPELINE
                # ==================================================

                with st.status(
                    "ResearchX-AI is working...",
                    expanded=True
                ) as pipeline:

                    # ----------------------------------------------
                    # PLANNER
                    # ----------------------------------------------

                    st.write(
                        "01 — Planner Agent"
                    )

                    st.write(
                        "Creating research strategy..."
                    )

                    research_plan = create_research_plan(
                        topic
                    )

                    st.session_state.research_plan = (
                        research_plan
                    )

                    st.success(
                        "Planner Agent completed."
                    )


                    # ----------------------------------------------
                    # RESEARCHER
                    # ----------------------------------------------

                    st.write(
                        "02 — Research Agent"
                    )

                    st.write(
                        "Searching and analyzing sources..."
                    )

                    research = research_topic(
                        topic,
                        research_plan
                    )

                    st.session_state.research = (
                        research
                    )

                    source_count = len(
                        research.get(
                            "sources",
                            []
                        )
                    )

                    st.success(
                        f"Research Agent completed. "
                        f"{source_count} sources collected."
                    )


                    # ----------------------------------------------
                    # FACT CHECKER
                    # ----------------------------------------------

                    st.write(
                        "03 — Fact Checker"
                    )

                    st.write(
                        "Checking important research claims..."
                    )

                    fact_check = fact_check_research(
                        research
                    )

                    st.session_state.fact_check = (
                        fact_check
                    )

                    st.success(
                        "Fact Checker completed."
                    )


                    # ----------------------------------------------
                    # SYNTHESIZER
                    # ----------------------------------------------

                    st.write(
                        "04 — Synthesizer"
                    )

                    st.write(
                        "Creating final evidence-based report..."
                    )

                    final_report = synthesize_research(
                        research,
                        fact_check
                    )

                    st.session_state.final_report = (
                        final_report
                    )

                    st.success(
                        "Synthesizer completed."
                    )


                    # ----------------------------------------------
                    # PDF
                    # ----------------------------------------------

                    st.write(
                        "Generating PDF report..."
                    )

                    pdf_path = create_pdf_report(
                        final_report
                    )

                    st.session_state.pdf_path = (
                        pdf_path
                    )

                    st.success(
                        "PDF report generated."
                    )


                    # ----------------------------------------------
                    # POWERPOINT
                    # ----------------------------------------------

                    st.write(
                        "Generating PowerPoint..."
                    )

                    ppt_path = create_professional_ppt(
                        final_report,
                        topic
                    )

                    st.session_state.ppt_path = (
                        ppt_path
                    )

                    st.success(
                        "PowerPoint generated."
                    )


                    # ----------------------------------------------
                    # HISTORY
                    # ----------------------------------------------

                    save_history(
                        topic
                    )

                    pipeline.update(
                        label="Research completed successfully",
                        state="complete",
                        expanded=False
                    )


                st.success(
                    "ResearchX-AI completed the full research workflow."
                )


            except Exception as e:

                st.error(
                    f"Research pipeline failed: {str(e)}"
                )


    # ========================================================
    # RESEARCH RESULTS
    # ========================================================

    if st.session_state.research:

        st.markdown(
            '<div class="section-title">'
            'Research Results'
            '</div>',
            unsafe_allow_html=True
        )

        source_count = len(
            st.session_state.research.get(
                "sources",
                []
            )
        )

        st.info(
            f"Research Agent collected {source_count} unique sources."
        )


        # ====================================================
        # SOURCES
        # ====================================================

        st.markdown(
            "### Collected Sources"
        )

        sources = st.session_state.research.get(
            "sources",
            []
        )

        if sources:

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

                with st.expander(
                    f"Source {index}: {title}"
                ):

                    st.write(
                        "URL:"
                    )

                    st.write(
                        url
                    )

                    st.write(
                        source.get(
                            "content",
                            ""
                        )[:1500]
                    )

        else:

            st.warning(
                "No sources were collected."
            )


        # ====================================================
        # RESEARCH ANALYSIS
        # ====================================================

        st.markdown(
            "### Research Analysis"
        )

        research_analysis = (
            st.session_state.research.get(
                "analysis",
                ""
            )
        )

        st.markdown(
            research_analysis
        )


    # ========================================================
    # FACT CHECK RESULTS
    # ========================================================

    if st.session_state.fact_check:

        st.markdown(
            '<div class="section-title">'
            'Fact Check Results'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.fact_check
        )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    if st.session_state.final_report:

        st.markdown(
            '<div class="section-title">'
            'Final Research Report'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.final_report
        )


# ============================================================
# RESEARCH HISTORY
# ============================================================

elif st.session_state.page == "Research History":

    st.markdown(
        '<div class="section-title">'
        'Research History'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Previously completed research projects.'
        '</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.research_history


    if not history:

        st.info(
            "No research projects have been completed yet."
        )

    else:

        for item in history:

            with st.container(border=True):

                st.markdown(
                    f"### {item['topic']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.caption(
                        f"Created: {item['date']}"
                    )

                with col2:

                    st.caption(
                        f"Sources collected: {item['sources']}"
                    )


# ============================================================
# REPORTS
# ============================================================

elif st.session_state.page == "Reports":

    st.markdown(
        '<div class="section-title">'
        'Reports'
        '</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.final_report:

        st.info(
            "No report is available yet. "
            "Start a new research project first."
        )

    else:

        st.markdown(
            f"### {st.session_state.research_topic}"
        )

        st.divider()

        col1, col2 = st.columns(2)


        # ====================================================
        # PDF
        # ====================================================

        with col1:

            if (
                st.session_state.pdf_path
                and os.path.exists(
                    st.session_state.pdf_path
                )
            ):

                with open(
                    st.session_state.pdf_path,
                    "rb"
                ) as file:

                    st.download_button(
                        "Download PDF Report",
                        data=file,
                        file_name=os.path.basename(
                            st.session_state.pdf_path
                        ),
                        mime="application/pdf",
                        use_container_width=True
                    )


        # ====================================================
        # POWERPOINT
        # ====================================================

        with col2:

            if (
                st.session_state.ppt_path
                and os.path.exists(
                    st.session_state.ppt_path
                )
            ):

                with open(
                    st.session_state.ppt_path,
                    "rb"
                ) as file:

                    st.download_button(
                        "Download PowerPoint",
                        data=file,
                        file_name=os.path.basename(
                            st.session_state.ppt_path
                        ),
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.presentationml.presentation"
                        ),
                        use_container_width=True
                    )


        st.divider()

        st.markdown(
            "### Final Research Report"
        )

        st.markdown(
            st.session_state.final_report
        )


# ============================================================
# ANALYTICS
# ============================================================

elif st.session_state.page == "Analytics":

    st.markdown(
        '<div class="section-title">'
        'Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Overview of your ResearchX-AI activity.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Research Projects",
            len(
                st.session_state.research_history
            )
        )


    with col2:

        st.metric(
            "Current Sources",
            get_source_count()
        )


    with col3:

        st.metric(
            "AI Agents",
            4
        )


    st.markdown(
        "### Agent Status"
    )


    if st.session_state.research_plan:

        st.success(
            "Planner Agent — Completed"
        )

    else:

        st.info(
            "Planner Agent — Waiting"
        )


    if st.session_state.research:

        st.success(
            "Research Agent — Completed"
        )

    else:

        st.info(
            "Research Agent — Waiting"
        )


    if st.session_state.fact_check:

        st.success(
            "Fact Checker — Completed"
        )

    else:

        st.info(
            "Fact Checker — Waiting"
        )


    if st.session_state.final_report:

        st.success(
            "Synthesizer — Completed"
        )

    else:

        st.info(
            "Synthesizer — Waiting"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'ResearchX-AI • Multi-Agent AI Research Platform'
    '</div>',
    unsafe_allow_html=True
)
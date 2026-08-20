import streamlit as st
import os

from agents.researcher import research_topic
from agents.fact_checker import fact_check_research
from agents.synthesizer import synthesize_research
from report_generator import create_pdf_report
from ppt_generator import create_ppt_report


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchX-AI",
    page_icon="🔬",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #777;
    margin-bottom: 35px;
}

.step-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title"> ResearchX-AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Research Assistant</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# TOPIC INPUT
# --------------------------------------------------

st.subheader(" Research Topic")

topic = st.text_input(
    "Enter the topic you want to research",
    placeholder="Example: Impact of Generative AI on Data Science Jobs"
)


generate = st.button(
    " Generate Research",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# RESEARCH PIPELINE
# --------------------------------------------------

if generate:

    if not topic.strip():

        st.warning(" Please enter a research topic.")

    else:

        # ------------------------------------------
        # STEP 1 — RESEARCHER
        # ------------------------------------------

        with st.status(
            " Researcher Agent is working...",
            expanded=True
        ):

            st.write("Searching the web...")
            st.write("Analyzing research sources...")

            research = research_topic(topic)

            st.write(" Research completed.")


        # ------------------------------------------
        # STEP 2 — FACT CHECKER
        # ------------------------------------------

        with st.status(
            " Fact Checker Agent is working...",
            expanded=True
        ):

            st.write("Checking research claims...")
            st.write("Evaluating source reliability...")

            fact_check = fact_check_research(research)

            st.write(" Fact checking completed.")


        # ------------------------------------------
        # STEP 3 — SYNTHESIS
        # ------------------------------------------

        with st.status(
            " Synthesis Agent is working...",
            expanded=True
        ):

            st.write("Combining research findings...")
            st.write("Generating final report...")

            final_report = synthesize_research(
                research,
                fact_check
            )

            st.write(" Research synthesis completed.")


        # ------------------------------------------
        # STEP 4 — PDF
        # ------------------------------------------

        with st.spinner(" Generating PDF report..."):

            pdf_path = create_pdf_report(
                final_report
            )


        st.success(
            f" PDF report created: {pdf_path}"
        )


        # ------------------------------------------
        # STEP 5 — POWERPOINT
        # ------------------------------------------

        with st.spinner(
            " Generating professional PowerPoint..."
        ):

            ppt_path = create_ppt_report(
                final_report
            )


        st.success(
            f" PowerPoint created: {ppt_path}"
        )


        st.divider()


        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        st.header(" Final Research Report")

        st.markdown(final_report)


        st.divider()


        # --------------------------------------------------
        # DOWNLOAD BUTTONS
        # --------------------------------------------------

        st.header(" Download Your Research")

        col1, col2 = st.columns(2)


        # PDF DOWNLOAD

        with col1:

            if os.path.exists(pdf_path):

                with open(pdf_path, "rb") as file:

                    st.download_button(
                        label=" Download PDF Report",
                        data=file,
                        file_name="research_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


        # PPT DOWNLOAD

        with col2:

            if os.path.exists(ppt_path):

                with open(ppt_path, "rb") as file:

                    st.download_button(
                        label=" Download PowerPoint",
                        data=file,
                        file_name="research_presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )


        st.success(
            " ResearchX-AI completed your research successfully!"
        )
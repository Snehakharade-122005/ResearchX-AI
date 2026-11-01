# ResearchX-AI 🤖
### AI-Powered Multi-Agent Research Assistant

< **[🚀 Live Demo – Try ResearchX-AI](https://researchx-ai.streamlit.app/)** >

ResearchX-AI is an intelligent research assistant that automates the process of researching, analyzing, fact-checking, and generating professional research reports using multiple AI agents.

The system combines Generative AI, web search, and automated report generation to transform a research topic into a structured, evidence-based report and presentation.

## 🚀 Live Application

**Try ResearchX-AI here:** https://researchx-ai.streamlit.app/

## ✨ Key Features

- AI Research Planning
- Automated Web Research using Tavily
- AI-Powered Analysis using Google Gemini
- Fact Checking
- Research Synthesis
- PDF Report Generation
- PowerPoint Presentation Generation
- Interactive Streamlit Dashboard
- Research History

## 🧠 Multi-Agent Architecture

```text
User Input
    |
    v
Planner Agent
    |
    v
Researcher Agent
    |
    v
Fact Checker Agent
    |
    v
Synthesizer Agent
    |
    v
Final Research Report
    |
    +------ PDF Report
    |
    +------ PowerPoint Presentation
```

## 🛠️ Technology Stack

- **Programming:** Python
- **AI:** Google Gemini, LangChain
- **Web Research:** Tavily API
- **Frontend:** Streamlit, HTML, CSS
- **Backend:** Flask, Flask-CORS
- **PDF:** ReportLab
- **PowerPoint:** Python-PPTX
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
ResearchX-AI/
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── fact_checker.py
│   └── synthesizer.py
├── database/
├── frontend/
├── rag/
├── reports/
├── tools/
├── utils/
├── workflow/
├── app.py
├── backend.py
├── ppt_generator.py
├── report_generator.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Snehakharade-122005/ResearchX-AI.git
cd ResearchX-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_MODEL=gemini-3.8-flash
GEMINI_FALLBACK_MODEL=
```

API resources:

- Google Gemini: https://aistudio.google.com/app/apikey
- Tavily: https://app.tavily.com/

**Never upload your `.env` file or expose API keys on GitHub.**

### 6. Run the Application

```bash
streamlit run app.py
```

## ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

**Live URL:** https://researchx-ai.streamlit.app/

## 🎯 Project Objective

To simplify and automate research activities through intelligent AI agents, reduce manual research effort, organize information from multiple sources, and generate professional research documents.

## 🔮 Future Enhancements

- Advanced Retrieval-Augmented Generation (RAG)
- Improved source credibility scoring
- Enhanced research analytics
- Additional AI agents and research workflows
- More report customization options

## 👩‍💻 Developer

**Sneha Dilip Kharade**

B.Tech – Computer Science and Engineering (Data Science)

Sir Padampat Singhania University, Udaipur

**GitHub:** https://github.com/Snehakharade-122005

---

⭐ If you find this project interesting, consider giving the repository a star!

*ResearchX-AI – Making research smarter with multi-agent artificial intelligence.*

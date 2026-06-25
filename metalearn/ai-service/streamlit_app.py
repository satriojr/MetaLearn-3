import streamlit as st
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _check_gemini() -> bool:
    return bool(os.getenv("GEMINI_API_KEY"))


st.set_page_config(
    page_title="MetaLearn AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.image(
    "https://img.shields.io/badge/MetaLearn-AI_Dashboard-purple?style=for-the-badge",
    use_container_width=False,
)

st.sidebar.markdown("## Navigation")
st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/1_nlp.py", label="NLP Engine", icon="💬")
st.sidebar.page_link("pages/2_bkt.py", label="BKT Engine", icon="📊")
st.sidebar.page_link("pages/3_pathway.py", label="Pathway Engine", icon="🗺️")
st.sidebar.page_link("pages/4_ast.py", label="AST Evaluator", icon="🔍")
st.sidebar.page_link("pages/5_report.py", label="Report Engine", icon="📝")
st.sidebar.page_link("pages/6_quiz_ai.py", label="AI Quiz Engine", icon="🧪")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**MetaLearn** — Platform Pembelajaran Adaptif Berbasis AI\n\n"
    "Tim NexaNode — Universitas Muria Kudus\n\n"
    "Samsung Solve for Tomorrow 2026"
)

st.title("🧠 MetaLearn AI Service Dashboard")
st.markdown(
    "Dashboard interaktif untuk menguji dan memvisualisasikan mesin AI MetaLearn."
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("NLP Engine", "Online" if _check_gemini() else "No API Key",
              help="Natural Language Processing — Pause & Ask AI")

with col2:
    st.metric("BKT Engine", "Ready",
              help="Bayesian Knowledge Tracing — mastery estimation")

with col3:
    st.metric("Pathway Engine", "Online" if _check_gemini() else "No API Key",
              help="Adaptive learning path generation")

with col4:
    st.metric("AST Evaluator", "Online" if _check_gemini() else "Limited",
              help="Abstract Syntax Tree — answer structure evaluation")

with col5:
    st.metric("Report Engine", "Online" if _check_gemini() else "No API Key",
              help="AI-generated narrative reports")

with col6:
    st.metric("AI Quiz Engine", "Ready",
              help="Quiz with AST + BKT + NLP")

st.markdown("---")

st.subheader("Quick Start")
st.markdown("""
- **💬 NLP Engine** — Test Pause & Ask AI, generate summaries and questions
- **📊 BKT Engine** — Simulate mastery tracing with adjustable parameters
- **🗺️ Pathway Engine** — Generate adaptive learning pathways
- **🔍 AST Evaluator** — Evaluate student answer structures
- **📝 Report Engine** — Generate narrative student reports
- **🧪 AI Quiz Engine** — Quiz with AST evaluation + BKT mastery + NLP feedback
""")

if not _check_gemini():
    st.warning(
        "⚠️ **GEMINI_API_KEY** tidak terdeteksi. "
        "Engine berbasis AI (NLP, Pathway, AST, Report) akan menggunakan mode terbatas. "
        "Setel environment variable `GEMINI_API_KEY` untuk aktivasi penuh.",
        icon="⚠️",
    )

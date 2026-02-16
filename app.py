import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# -----------------------------
# ENV SETUP
# -----------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# -----------------------------
# IMPORTS
# -----------------------------
from parser.document_parser import extract_text
from graph.contract_graph import build_contract_graph
from utils.vector_store import index_contract
from reports.report_generator import generate_report

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ClauseAI – Contract Intelligence",
    layout="wide"
)

# -----------------------------
# THEME TOGGLE
# -----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=True)
st.session_state.theme = "dark" if dark_mode else "light"

# -----------------------------
# THEME CSS
# -----------------------------
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
    body {background:#0F172A;color:#E5E7EB;}
    .hero{
        background:linear-gradient(135deg,#1E1B4B,#312E81);
        padding:3rem;border-radius:24px;margin-bottom:2rem;
    }
    .card{
        background:#020617;padding:2rem;border-radius:20px;
        box-shadow:0 0 20px rgba(99,102,241,0.25);
    }
    .stButton>button{
        background:#6366F1;color:white;border-radius:12px;
        font-weight:600;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body {background:#F9FAFB;color:#0F172A;}
    .hero{
        background:linear-gradient(135deg,#4F46E5,#6366F1);
        padding:3rem;border-radius:24px;margin-bottom:2rem;
    }
    .card{
        background:white;padding:2rem;border-radius:20px;
        box-shadow:0 10px 25px rgba(0,0,0,0.06);
    }
    .stButton>button{
        background:#4F46E5;color:white;border-radius:12px;
        font-weight:600;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero">
<h1>📄 ClauseAI</h1>
<p>AI-powered contract intelligence using LangGraph, Gemini & Pinecone</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR OPTIONS
# -----------------------------
st.sidebar.header("⚙️ Report Settings")

tone = st.sidebar.selectbox(
    "Report Tone",
    ["professional","business-friendly","simple","strict-legal"]
)

focus = st.sidebar.selectbox(
    "Report Focus",
    ["balanced","risk-heavy","compliance-heavy","financial-heavy"]
)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload Contracts",
    type=["pdf","docx"],
    accept_multiple_files=True
)

# -----------------------------
# PROCESS FILES
# -----------------------------
def process_file(file):
    file_type = file.name.split(".")[-1]
    text = extract_text(file, file_type)
    index_contract(file.name, text)
    return f"\n\n--- {file.name} ---\n{text}"

if uploaded_files:

    with st.spinner("📥 Extracting & indexing contracts..."):
        with ThreadPoolExecutor() as executor:
            texts = list(executor.map(process_file, uploaded_files))

    all_text = "".join(texts)

    st.success(f"✅ {len(uploaded_files)} contracts processed successfully")

    with st.expander("📜 View Extracted Text"):
        st.text_area("", all_text, height=300)

    # -----------------------------
    # RUN ANALYSIS
    # -----------------------------
    if st.button("🚀 Run AI Analysis"):

        with st.spinner("🤖 Running multi-agent workflow..."):
            graph = build_contract_graph()

            final_state = graph.invoke({
                "contract_text": all_text,
                "contract_id": "Multiple Documents",
                "shared_memory": [],
                "retrieved_clauses": [],
                "compliance": [],
                "finance": [],
                "legal": [],
                "operations": []
            })

        st.success("✅ Analysis completed")

        # -----------------------------
        # GENERATE REPORT
        # -----------------------------
        report = generate_report(final_state, tone, focus)

        # -----------------------------
        # TABS
        # -----------------------------
        tabs = st.tabs([
            "⚖️ Compliance",
            "💰 Finance",
            "📜 Legal",
            "⚙️ Operations",
            "📑 Final Report",
            "💬 Feedback"
        ])

        # -----------------------------
        # RENDER FUNCTION
        # -----------------------------
        def render(findings):
            if not findings:
                st.info("No issues detected.")
                return

            for c in findings:
                with st.expander(c["clause_type"]):
                    st.markdown(f"**Category:** {c['category']}")
                    st.markdown(f"**Explanation:** {c['explanation']}")
                    st.markdown(f"**How it appears:** {c['how_it_appears']}")
                    st.markdown(f"**Why it matters:** {c['why_it_matters']}")
                    st.markdown(f"**Risk:** {c['risk_or_note']}")
                    st.markdown(f"**Counter Measure:** {c.get('counter_measure','N/A')}")
                    st.markdown(f"**Severity:** {c.get('severity','N/A')}")
                    st.markdown(f"**Confidence:** {c.get('confidence','N/A')}")
                    st.markdown(f"**Summary:** {c.get('summary','N/A')}")
                    st.markdown(f"**Source:** {c.get('source_document','N/A')}")

        with tabs[0]: render(final_state["compliance"])
        with tabs[1]: render(final_state["finance"])
        with tabs[2]: render(final_state["legal"])
        with tabs[3]: render(final_state["operations"])

        with tabs[4]:
            st.text_area("Generated Report", report, height=450)

        with tabs[5]:
            feedback = st.text_area("Your feedback")
            if st.button("Submit Feedback"):
                st.success("Thanks for your feedback!")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("ClauseAI © 2026 | LangGraph • Gemini • Pinecone • Streamlit")

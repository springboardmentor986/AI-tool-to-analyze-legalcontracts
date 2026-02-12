import streamlit as st
import sys
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# ---------------- PATH SETUP ----------------

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ingestion.parser import parse_file
from ingestion.chunker import chunk_text
from embeddings.pinecone_client import upsert_chunks
from planner.domain_classifier import classify_domains
from planner.planner import create_plan
from planner.executor import run_agents
from qa.contract_qa import answer_question



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

st.set_page_config(page_title="ClauseAI", layout="wide")



if "history" not in st.session_state:
    st.session_state.history = []

if "current_session" not in st.session_state:
    st.session_state.current_session = None

if "contract_id" not in st.session_state:
    st.session_state.contract_id = None

# ---------------- SIDEBAR ----------------

st.sidebar.title("Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Contract",
    type=["pdf", "docx", "txt"]
)

analyze_btn = st.sidebar.button("Analyze Contract")

st.sidebar.divider()

st.title("Contract Analysis")

# =====================================================
#               UPLOAD + ANALYSIS
# =====================================================

if uploaded_file and analyze_btn:

    with st.spinner("Parsing contract..."):
        text = asyncio.run(parse_file(uploaded_file))

    contract_id = uploaded_file.name
    st.session_state.contract_id = contract_id

    # Chunk + Store
    with st.spinner("Chunking and storing in Pinecone..."):
        chunks = chunk_text(text)
        upsert_chunks(chunks, namespace=contract_id)

    # Domain Classification
    domains = classify_domains(text)
    plan = create_plan(domains)

    with st.spinner("Running parallel domain analysis..."):
        results = asyncio.run(run_agents(plan))


    session = {
        "name": uploaded_file.name,
        "domains": domains,
        "results": results,
        "time": datetime.now().strftime("%H:%M")
    }

    st.session_state.history.insert(0, session)
    st.session_state.current_session = session

# =====================================================
#               DISPLAY RESULTS
# =====================================================

session = st.session_state.current_session

if session:

    st.caption(f"Detected Domains: {', '.join(session['domains'])}")
    st.divider()

    if session["results"]:

        cols = st.columns(len(session["results"]))

        for col, (domain, output) in zip(cols, session["results"].items()):
            with col:
                st.subheader(domain.upper())

                analysis_text = (
                    output.get("analysis")
                    if isinstance(output, dict)
                    else str(output)
                )

                st.markdown(
                    f"""
                    <div style="
                        background-color:#111;
                        padding:15px;
                        border-radius:10px;
                        min-height:300px;
                        overflow-y:auto;
                    ">
                    {analysis_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("No results returned.")

else:
    st.info("Upload and analyze a contract first.")

# =====================================================
#               QA SECTION
# =====================================================

st.divider()
st.subheader("Ask Questions About Contract")

if not st.session_state.contract_id:
    st.warning("Please upload and analyze a contract first.")
else:
    user_question = st.text_input("Enter your question")

    if st.button("Get Answer"):

        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching contract..."):
                result = answer_question(
                    question=user_question,
                    namespace=st.session_state.contract_id
                )

            st.success(result["answer"])

            if result.get("context"):
                with st.expander("View Supporting Clauses"):
                    st.write(result["context"])

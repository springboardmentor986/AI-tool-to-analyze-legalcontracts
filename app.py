"""
ClauseAI - AI-Powered Contract Analysis System
Streamlit Application (Milestone 4 - Final Stable Version)
"""

import streamlit as st
from vector_store import (
    store_chunks_in_vector_store,
    query_index,
    initialize_pinecone
)
from sentence_transformers import SentenceTransformer
import docx2txt
from PyPDF2 import PdfReader
import os
import uuid

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ClauseAI - Contract Analysis",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "embed_model" not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

if "pinecone_initialized" not in st.session_state:
    st.session_state.pinecone_initialized = False

if "last_query_results" not in st.session_state:
    st.session_state.last_query_results = []

if "current_contract_id" not in st.session_state:
    st.session_state.current_contract_id = None

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📄 ClauseAI - Contract Analysis System")
st.markdown("Upload contracts, analyze clauses, and generate AI-powered reports.")

# --------------------------------------------------
# SIDEBAR CONFIGURATION
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input("Pinecone API Key", type="password")

    if api_key:
        os.environ["PINECONE_API_KEY"] = api_key

        if not st.session_state.pinecone_initialized:
            with st.spinner("Initializing Pinecone..."):
                if initialize_pinecone():
                    st.session_state.pinecone_initialized = True
                    st.success("✅ Pinecone Connected")
                else:
                    st.error("❌ Pinecone Initialization Failed")

    st.divider()

    chunk_size = st.slider("Chunk Size", 200, 1000, 500, 50)
    top_k = st.slider("Top K Results", 1, 10, 5)

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "📤 Upload Document",
    "🔍 Query Analysis",
    "📊 Generate Report"
])

# ==================================================
# TAB 1 — UPLOAD
# ==================================================

with tab1:
    st.header("Upload Contract")

    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    if uploaded_file:
        try:
            with st.spinner("Extracting text..."):
                if uploaded_file.type == "application/pdf":
                    reader = PdfReader(uploaded_file)
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])
                else:
                    text = docx2txt.process(uploaded_file)

            st.success(f"Loaded: {uploaded_file.name}")

            col1, col2 = st.columns(2)
            col1.metric("Characters", len(text))
            col2.metric("Words", len(text.split()))

            with st.expander("Preview"):
                st.text_area("Document Preview", text[:1000], height=200)

            if st.button("🚀 Process & Store", type="primary"):

                if not st.session_state.pinecone_initialized:
                    st.error("Configure Pinecone first.")
                    st.stop()

                contract_id = str(uuid.uuid4())
                st.session_state.current_contract_id = contract_id

                chunks = [
                    text[i:i+chunk_size]
                    for i in range(0, len(text), chunk_size)
                ]

                embeddings = st.session_state.embed_model.encode(
                    chunks,
                    batch_size=32,
                    show_progress_bar=True
                ).tolist()

                store_chunks_in_vector_store(
                    chunks,
                    embeddings,
                    contract_id=contract_id,
                    filename=uploaded_file.name
                )

                st.success(f"Stored {len(chunks)} chunks successfully!")
                st.info(f"Contract ID: {contract_id}")

        except Exception as e:
            st.error(str(e))

# ==================================================
# TAB 2 — QUERY
# ==================================================

with tab2:
    st.header("Query Contract Database")

    if not st.session_state.pinecone_initialized:
        st.warning("Configure Pinecone API Key first.")
    else:
        query = st.text_input("Enter your query")

        if st.button("🔍 Search") and query:

            query_embedding = st.session_state.embed_model.encode(
                [query]
            )[0].tolist()

            results = query_index(
                query_embedding,
                top_k=top_k,
                contract_id=st.session_state.current_contract_id
            )

            st.session_state.last_query_results = results

            for i, res in enumerate(results, 1):
                with st.expander(f"Result {i} | Score: {res['score']:.4f}"):
                    st.write(res["text"])
                    if "filename" in res["metadata"]:
                        st.caption(f"Source: {res['metadata']['filename']}")

# ==================================================
# TAB 3 — REPORT GENERATION
# ==================================================

with tab3:
    st.header("Automated Report Generation")

    if not st.session_state.last_query_results:
        st.info("Run a query first to generate a report.")
    else:

        tone = st.selectbox(
            "Report Tone",
            ["Professional", "Legal", "Executive", "Simplified"]
        )

        structure = st.selectbox(
            "Report Structure",
            ["Detailed Analysis", "Bullet Points", "Executive Summary"]
        )

        focus = st.selectbox(
            "Report Focus",
            ["Full Contract", "Risk Analysis",
             "Financial Terms", "Obligations",
             "Termination Clauses"]
        )

        if st.button("📊 Generate Report", type="primary"):

            combined_text = " ".join(
                [res["text"] for res in st.session_state.last_query_results]
            )

            report = f"""
CONTRACT ANALYSIS REPORT
------------------------
Tone: {tone}
Structure: {structure}
Focus: {focus}

SUMMARY:
{combined_text[:2000]}

END OF REPORT
"""

            st.success("Report Generated Successfully")
            st.text_area("Generated Report", report, height=400)

            st.download_button(
                "⬇ Download Report",
                report,
                file_name="contract_report.txt"
            )

            st.divider()
            st.subheader("Feedback")

            col1, col2 = st.columns(2)

            if col1.button("👍 Helpful"):
                st.success("Thanks for your feedback!")

            if col2.button("👎 Needs Improvement"):
                st.warning("We will improve the report quality.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.markdown(
    "<div style='text-align:center;color:gray;'>ClauseAI v2.0 | Multi-Contract AI Analysis</div>",
    unsafe_allow_html=True
)

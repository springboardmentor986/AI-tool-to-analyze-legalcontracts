import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from datetime import datetime

# ---------------- Imports ----------------
from ingestion.load_docs import load_contract

from orchestration.parallel_agents import run_parallel_agents
from pipelines.risk_pipeline import (
    compliance_risk_pipeline,
    finance_risk_pipeline,
    calculate_overall_risk
)
from multi_turn.agent_interaction import finance_reviews_legal
from memory.pinecone_store import store_result
from ai_assistant.ai_chat import chat_with_contract



# ---------------- Page Config ----------------
st.set_page_config(
    page_title="ClauseAI – Contract Intelligence",
    page_icon="📄",
    layout="wide"
)

# ---------------- Sidebar ----------------
st.sidebar.title("📄 ClauseAI")

section = st.sidebar.radio(
    "Navigate",
    [
        "Upload & Analyze",
        "Risk Summary",
        "Cross-Agent Reasoning",
        "AI Assistant",
        "Download Report"
    ]
)

st.sidebar.caption("Parallel Agents • Multi-Document • Memory")

# ---------------- Header ----------------
st.title("📄 ClauseAI – AI Contract Intelligence Platform")
st.write("Upload one or more contracts and analyze them using parallel AI agents.")
st.divider()

# ---------------- Session State ----------------
if "documents" not in st.session_state:
    st.session_state.documents = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "ai_context" not in st.session_state:
    st.session_state.ai_context = ""


# ===================== UPLOAD & ANALYZE =====================
if section == "Upload & Analyze":

    st.subheader("📂 Upload Contracts")

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    # -------- Process NEW uploads --------
    if uploaded_files:
        st.session_state.documents = []
        st.session_state.chat_history = []
        st.session_state.ai_context = ""

        os.makedirs("contracts", exist_ok=True)

        for uploaded_file in uploaded_files:

            st.markdown(f"## 📄 {uploaded_file.name}")

            file_path = os.path.join("contracts", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # -------- Text Extraction --------
            with st.spinner("Extracting contract text..."):
                chunks = load_contract(file_path)

            contract_text = " ".join(c.page_content for c in chunks)

            # -------- Parallel Agent Execution --------
            with st.spinner("Running parallel AI agents..."):
                results = run_parallel_agents(contract_text)

            doc = {
                "name": uploaded_file.name,
                "text": contract_text,
                "legal": results["legal"],
                "finance": results["finance"],
                "compliance": results["compliance"],
                "operations": results["operations"],
                "store": False
            }

            st.session_state.documents.append(doc)

        st.success("✅ All contracts analyzed successfully")

    # -------- Persistent Display --------
    if st.session_state.documents:

        st.subheader("📑 Analyzed Contracts")

        for idx, doc in enumerate(st.session_state.documents):

            st.markdown(f"### 📄 {doc['name']}")

            with st.expander("📄 Sample Extracted Text"):
                st.write(doc["text"][:2000] + "...")

            with st.expander("⚖️ Legal Agent Output"):
                st.write(doc["legal"])

            with st.expander("💰 Finance Agent Output"):
                st.write(doc["finance"])

            with st.expander("📋 Compliance Agent Output"):
                st.write(doc["compliance"])

            with st.expander("⚙️ Operations Agent Output"):
                st.write(doc["operations"])

            doc["store"] = st.checkbox(
                f"🧠 Store `{doc['name']}` in Pinecone",
                key=f"store_{idx}"
            )

        if st.button("📥 Store Selected Documents in Pinecone"):
            for doc in st.session_state.documents:
                if doc["store"]:
                    store_result(doc["legal"], {"agent": "legal", "doc": doc["name"]})
                    store_result(doc["finance"], {"agent": "finance", "doc": doc["name"]})
                    store_result(doc["compliance"], {"agent": "compliance", "doc": doc["name"]})
                    store_result(doc["operations"], {"agent": "operations", "doc": doc["name"]})

            st.success("✅ Selected documents stored successfully")

    else:
        st.info("Upload contracts to begin analysis.")


# ===================== RISK SUMMARY =====================
elif section == "Risk Summary":

    if not st.session_state.documents:
        st.info("Upload contracts first.")
    else:
        for doc in st.session_state.documents:

            st.markdown(f"### 📄 {doc['name']}")

            compliance_risks = compliance_risk_pipeline(doc["compliance"])
            finance_risks = finance_risk_pipeline(doc["finance"])

            overall_risk = calculate_overall_risk(
                compliance_risks,
                finance_risks
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📋 Compliance Risks")
                st.write(compliance_risks)

            with col2:
                st.subheader("💰 Financial Risks")
                st.write(finance_risks)

            st.subheader("📊 Overall Contract Risk")
            st.markdown(f"### {overall_risk}")


# ===================== CROSS-AGENT REASONING =====================
elif section == "Cross-Agent Reasoning":

    if not st.session_state.documents:
        st.info("Upload contracts first.")
    else:
        for doc in st.session_state.documents:
            st.markdown(f"### 📄 {doc['name']}")
            review = finance_reviews_legal(doc["legal"])
            st.write(review)


# ===================== AI ASSISTANT =====================
elif section == "AI Assistant":

    if not st.session_state.documents:
        st.info("Upload and analyze contracts first.")
    else:
        st.subheader("🤖 AI Assistant – Chat with Contracts")
        st.caption("Answers are based ONLY on analyzed agent outputs")

        if not st.session_state.ai_context:
            blocks = []
            for doc in st.session_state.documents:
                blocks.append(
                    f"""
DOCUMENT: {doc['name']}
LEGAL: {doc['legal']}
FINANCE: {doc['finance']}
COMPLIANCE: {doc['compliance']}
OPERATIONS: {doc['operations']}
"""
                )
            st.session_state.ai_context = "\n".join(blocks)

        user_query = st.chat_input(
            "Ask about risks, termination, penalties, comparisons, etc."
        )

        if user_query:
            answer = chat_with_contract(
                st.session_state.ai_context,
                user_query
            )
            st.session_state.chat_history.append(
                {"q": user_query, "a": answer}
            )

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["q"])
            with st.chat_message("assistant"):
                st.write(chat["a"])


# ===================== DOWNLOAD REPORT =====================
elif section == "Download Report":

    if not st.session_state.documents:
        st.info("Upload contracts first.")
    else:
        now = datetime.now().strftime("%d %B %Y | %H:%M")
        report = f"ClauseAI Report\nGenerated: {now}\n\n"

        for doc in st.session_state.documents:
            report += f"""
==============================
DOCUMENT: {doc['name']}
==============================

LEGAL:
{doc['legal']}

FINANCE:
{doc['finance']}

COMPLIANCE:
{doc['compliance']}

OPERATIONS:
{doc['operations']}
"""

        st.download_button(
            "📄 Download TXT Report",
            report,
            file_name="ClauseAI_Report.txt",
            mime="text/plain"
        )

# ---------------- Footer ----------------
st.divider()
st.caption("ClauseAI © 2026 | AI Contract Intelligence Platform")

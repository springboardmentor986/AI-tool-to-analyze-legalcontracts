from dotenv import load_dotenv
load_dotenv()

import os
import json
import streamlit as st
import PyPDF2
from docx import Document
from groq import Groqgit 
from concurrent.futures import ThreadPoolExecutor, as_completed

from langgraph_flow import run_langgraph_pipeline
from embeddings.embedding_service import generate_embedding
from vectorstore.pinecone_store import init_pinecone, store_clause_vectors
from vectorstore.pinecone_query import query_contract_clauses
from qa.answer_generator import generate_answer


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ClauseAI — Contract Intelligence",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# SESSION DEFAULTS
# --------------------------------------------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


def safe_llm(prompt: str):
    try:
        r = groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return None


def safe_json(text):
    try:
        return json.loads(text)
    except Exception:
        return {}


# --------------------------------------------------
# AUTO SUMMARY GENERATOR (ROBUST FALLBACK)
# --------------------------------------------------
def generate_agent_summary(agent, clauses_text, full_contract_text):

    context = clauses_text.strip()

    if not context:
        context = full_contract_text[:3000]

    prompt = f"""
You are a {agent} contract analyst.

Generate a concise domain summary.

Return ONLY valid JSON:

{{
  "overall_risk": "Low|Medium|High",
  "key_concerns": [],
  "priority_actions": []
}}

Context:
{context}
"""

    result = safe_llm(prompt)

    return safe_json(result) if result else {}


# --------------------------------------------------
# UI — HERO
# --------------------------------------------------
st.markdown("""
<h1 style='text-align:center;'>📄 ClauseAI</h1>
<p style='text-align:center; font-size:1.1em;'>
AI-powered Contract Intelligence Platform
</p>
""", unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# UPLOAD
# --------------------------------------------------
st.markdown("## 🚀 Upload & Analyze Contract")

uploaded_file = st.file_uploader(
    "Upload PDF / DOCX / TXT",
    ["pdf", "docx", "txt"]
)

analyze_btn = st.button("🔍 Analyze Contract", use_container_width=True)


# --------------------------------------------------
# TEXT EXTRACTION
# --------------------------------------------------
def extract_text(file, ext):

    if ext == "pdf":
        return "\n".join(
            p.extract_text() or ""
            for p in PyPDF2.PdfReader(file).pages
        )

    if ext == "docx":
        return "\n".join(
            p.text for p in Document(file).paragraphs if p.text
        )

    if ext == "txt":
        return file.read().decode("utf-8")

    return ""


# --------------------------------------------------
# AGENT PROMPT
# --------------------------------------------------
def agent_prompt(agent, text):

    return f"""
Return ONLY valid JSON.

{{
 "domain_summary": {{
   "overall_risk": "Low|Medium|High",
   "key_concerns": [],
   "priority_actions": []
 }},
 "clauses": []
}}

Analyze this contract from {agent.upper()} perspective.

Contract:
{text[:3000]}
"""


# --------------------------------------------------
# PARALLEL AGENT EXECUTION
# --------------------------------------------------
def run_agents_parallel(text):

    agents = ["Legal", "Compliance", "Finance", "Operations"]
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:

        futures = {
            executor.submit(safe_llm, agent_prompt(agent, text)): agent
            for agent in agents
        }

        for future in as_completed(futures):

            agent = futures[future]
            output = future.result()

            results[agent] = output if output else "{}"

    return results


# --------------------------------------------------
# FINAL VERDICT
# --------------------------------------------------
def generate_verdict(agent_results):

    return safe_llm(f"""
Summarize overall contract risk using:

{json.dumps(agent_results)[:6000]}

Format:
### Overall Risk: Low/Medium/High
**Key Issues**
- ...
**Red Flags**
- ...
**Next Steps**
- ...
""")


# --------------------------------------------------
# MAIN ANALYSIS
# --------------------------------------------------
if uploaded_file and analyze_btn:

    ext = uploaded_file.name.split(".")[-1].lower()
    text = extract_text(uploaded_file, ext)

    if not text:
        st.error("❌ Failed to extract text")
        st.stop()


    # Save full contract text (IMPORTANT)
    st.session_state.full_contract_text = text


    with st.spinner("🧠 Running multi-agent analysis..."):

        run_langgraph_pipeline(text)

        agent_results = run_agents_parallel(text)

        verdict = generate_verdict(agent_results)

        # Pinecone
        index = init_pinecone()
        contract_id = uploaded_file.name.replace(" ", "_")

        for agent, content in agent_results.items():

            parsed = safe_json(content)
            clauses = parsed.get("clauses", [])

            for c in clauses:
                c["embedding"] = generate_embedding(
                    f"{c.get('clause_type')} {c.get('summary')}"
                )

            if clauses:
                store_clause_vectors(index, contract_id, agent, clauses)


    # Session
    st.session_state.analysis_done = True
    st.session_state.agent_results = agent_results
    st.session_state.verdict = verdict
    st.session_state.contract_name = uploaded_file.name

    st.success("✅ Analysis completed successfully!")


# --------------------------------------------------
# RESULTS
# --------------------------------------------------
if st.session_state.analysis_done:

    st.divider()
    st.markdown("## 📊 Analysis Results")


    # ---------- Verdict ----------
    st.subheader("✅ Final Verdict")
    st.markdown(st.session_state.verdict)


    # ---------- Agent Tabs ----------
    st.subheader("🧠 Agent Reports")

    tabs = st.tabs(st.session_state.agent_results.keys())


    for tab, agent in zip(tabs, st.session_state.agent_results):

        with tab:

            parsed = safe_json(
                st.session_state.agent_results[agent]
            )

            clauses = parsed.get("clauses", [])


            # ---------- GUARANTEED SUMMARY ----------
            summary = parsed.get("domain_summary")

            if not summary or not summary.get("overall_risk"):

                clause_text = "\n".join(
                    f"{c.get('clause_type')}: {c.get('summary')}"
                    for c in clauses
                )

                summary = generate_agent_summary(
                    agent,
                    clause_text,
                    st.session_state.full_contract_text
                )


            # ---------- UI ----------
            st.markdown(f"### 📊 {agent} Summary")

            st.metric(
                "Overall Risk",
                summary.get("overall_risk", "N/A")
            )


            st.markdown("**Key Concerns**")

            if summary.get("key_concerns"):
                for x in summary["key_concerns"]:
                    st.write("•", x)
            else:
                st.write("• No major concerns identified")


            st.markdown("**Priority Actions**")

            if summary.get("priority_actions"):
                for x in summary["priority_actions"]:
                    st.write("•", x)
            else:
                st.write("• No immediate actions required")


            st.divider()


            # ---------- CLAUSES ----------
            st.markdown("### 📄 Extracted Clauses")

            if clauses:

                for i, c in enumerate(clauses, 1):

                    with st.expander(
                        f"{i}. {c.get('clause_type')} ({c.get('risk_level')})"
                    ):

                        st.write("**Summary:**", c.get("summary"))
                        st.write("**Recommendation:**", c.get("recommendation"))

            else:
                st.info("No significant clauses extracted.")


    # ---------- Download ----------
    st.subheader("📥 Download Full Report")

    st.download_button(
        "⬇️ Download Analysis Report",
        json.dumps(st.session_state.agent_results, indent=2),
        "ClauseAI_Report.json",
        "application/json"
    )


    # ---------- RAG ----------
    st.subheader("💬 Ask Questions (RAG)")

    q = st.text_input("Ask a question about this contract")

    if st.button("Ask"):

        matches = query_contract_clauses(q)

        answer = generate_answer(q, matches)

        st.markdown(answer)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------
st.divider()
st.markdown("## ✨ Advanced Features")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📊 Visualization Dashboard")
    st.write("Simple visual insights for risk and clauses.")

with c2:
    st.markdown("### 🤝 Negotiation AI")
    st.write("AI-powered negotiation suggestions before signing.")

with c3:
    st.markdown("### 🗺️ Smart Action Plan")
    st.write("Clear next steps without legal complexity.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown("© 2026 ClauseAI — Developed by Pari")

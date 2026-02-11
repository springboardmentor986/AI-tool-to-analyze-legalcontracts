from __future__ import annotations
from src.clauseai.llm import get_llm


import asyncio
import os
import time
import uuid
import json
import io
import zipfile
import streamlit as st

from src.clauseai.loaders import load_contract
from src.clauseai.graph import build_graph
from src.clauseai.config import settings


# ✅ Fix for Streamlit threads on Windows: ensure an event loop exists
def _ensure_event_loop() -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


_ensure_event_loop()

st.set_page_config(
    page_title="ClauseAI — Contract Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- UI Styles ----------
st.markdown(
    """
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px;}
.card {
  border:1px solid #e2e8f0; border-radius:18px; padding:16px;
  background:#fff; box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}
.muted {color:#64748b; font-size: 13px;}
.badge {
  display:inline-block; font-size:12px; padding:4px 10px; border-radius:999px;
  background:#f1f5f9; border:1px solid #e2e8f0; margin-right:6px;
}
.kpi {
  border:1px solid #e2e8f0; border-radius:16px; padding:12px; background:#f8fafc;
}
.kpi .label {color:#64748b; font-size:12px; margin-bottom:4px;}
.kpi .value {font-size:18px; font-weight:700; color:#0f172a;}
.small-note {font-size:12px; color:#64748b; margin-top:6px;}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
<div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
  <h2 style="margin:0;">ClauseAI</h2>
  <span class="badge">⚖️ Contract Analyzer</span>
  <span class="badge">Groq + Pinecone</span>
</div>
<div class="muted">Upload a contract → Preview text → Analyze → View & Download report bundle.</div>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Settings")
tone = st.sidebar.selectbox("Report tone", ["Professional", "Simple", "Strict"], index=0)
focus = st.sidebar.multiselect(
    "Focus areas",
    ["Compliance", "Finance", "Legal", "Operations"],
    default=["Compliance", "Finance", "Legal", "Operations"],
)
feedback = st.sidebar.text_area("Message me/ notes (optional)", value="", height=120)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Status")

groq_ok = bool(os.getenv("GROQ_API_KEY") or getattr(settings, "groq_api_key", ""))
pinecone_ok = bool(os.getenv("PINECONE_API_KEY") or getattr(settings, "pinecone_api_key", ""))

st.sidebar.write("✅ Groq key loaded" if groq_ok else "❌ Groq key missing")
st.sidebar.write("✅ Pinecone key loaded" if pinecone_ok else "❌ Pinecone key missing")

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Pinecone")
st.sidebar.write("Index:", getattr(settings, "pinecone_index", "Not set"))

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Provider")
st.sidebar.write("LLM:", (os.getenv("LLM_PROVIDER", "groq") or "groq").upper())
st.sidebar.write("Model:", os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"))
st.sidebar.write("Embeddings:", os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))

# ---------- Session State ----------
if "out" not in st.session_state:
    st.session_state.out = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "file_type" not in st.session_state:
    st.session_state.file_type = ""
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "last_run" not in st.session_state:
    st.session_state.last_run = {}
if "analysis_error" not in st.session_state:
    st.session_state.analysis_error = None

# ---------- Layout ----------
c1, c2 = st.columns([1.35, 0.65], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Contract")
    uploaded = st.file_uploader("PDF or DOCX", type=["pdf", "docx"])
    st.markdown(
        '<div class="muted">Tip: Huge contracts can be slower. If it hangs, reduce TOP_K / chunk size.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🧾 Run Summary")
    st.write(f"**Tone:** {tone}")
    st.write(f"**Focus:** {', '.join(focus) if focus else 'None'}")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs([
    "🔎 Preview",
    "🧠 Analyze",
    "🤖 Agent Review",
    "📌 Final Report"
])


# ---------- Preview Tab ----------
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Extracted Text Preview")

    if uploaded:
        os.makedirs("tmp", exist_ok=True)
        file_path = os.path.join("tmp", uploaded.name)
        with open(file_path, "wb") as f:
            f.write(uploaded.read())

        file_type, text = load_contract(file_path)
        st.session_state.raw_text = text or ""
        st.session_state.file_type = file_type or ""
        st.session_state.filename = uploaded.name

        st.caption(f"Detected: {file_type} | Characters: {len(st.session_state.raw_text):,}")
        st.text_area("Preview (first 4,000 chars)", st.session_state.raw_text[:4000], height=240)

        st.markdown(
            '<div class="small-note">✅ Preview loaded. Go to the <b>Analyze</b> tab.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Upload a file to preview extracted text.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Analyze Tab ----------
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Run Contract Analysis")

    left_btn, right_btn = st.columns([1, 1])

    def _clear_results():
        st.session_state.out = None
        st.session_state.last_run = {}
        st.session_state.analysis_error = None

    run = left_btn.button("🚀 Analyze Contract", use_container_width=True)
    right_btn.button("🧹 Clear Results", use_container_width=True, on_click=_clear_results)

    st.write("")
    prog = st.progress(0)
    status = st.empty()

    if run:
        st.session_state.analysis_error = None

        if not pinecone_ok:
            st.error("Missing PINECONE_API_KEY in .env")
            st.stop()
        if not groq_ok:
            st.error("Missing GROQ_API_KEY in .env (LLM_PROVIDER=groq)")
            st.stop()

        text = st.session_state.get("raw_text", "")
        file_type = st.session_state.get("file_type", "")

        if not text.strip():
            st.error("No extracted text found. Go to Preview tab and re-upload.")
            st.stop()

        namespace = f"contract-{uuid.uuid4().hex[:10]}"
        graph = build_graph()

        status.info("Running analysis… (don’t close this tab)")
        prog.progress(10)

        start = time.time()
        try:
            out = graph.invoke(
                {
                    "raw_text": text,
                    "file_type": file_type,
                    "namespace": namespace,
                    "tone": tone,
                    "focus_areas": focus,
                    "feedback": feedback,
                }
            )
        except Exception as e:
            st.session_state.analysis_error = repr(e)
            st.error("❌ Analysis failed. See error below:")
            st.code(st.session_state.analysis_error)
            st.stop()

        took = time.time() - start
        prog.progress(100)
        status.success(f"✅ Done in {took:.1f}s")

        st.session_state.out = out
        st.session_state.last_run = {
            "took": took,
            "chars": len(text),
            "namespace": namespace,
            "tone": tone,
            "focus": focus,
            "filename": st.session_state.get("filename", ""),
            "file_type": file_type,
        }

        st.success("✅ Result ready. Open the **Report** tab to view & download.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- AGENT REVIEW TAB ----------
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🤖 Agent Review")

    from src.clauseai.llm import get_llm  # make sure this file exists

    out = st.session_state.get("out")

    if not out:
        st.info("Run analysis first.")
    else:
        domain_reports = out.get("domain_reports", {}) or {}

        if not domain_reports:
            st.warning("No agent outputs found.")
        else:
            agent_tabs = st.tabs(list(domain_reports.keys()))

            for i, domain in enumerate(domain_reports.keys()):
                with agent_tabs[i]:

                    # ---------- AGENT SUMMARY ----------
                    dr = domain_reports.get(domain, {})

                    summary = ""

                    if isinstance(dr, dict):
                        if dr.get("error"):
                            st.error(dr["error"])
                        else:
                            summary = dr.get("summary") or dr.get("raw") or ""
                    else:
                        summary = str(dr)

                    if summary:
                        # ---- Bold Important Headings ----
                        summary = summary.replace("Domain Overview:", "**Domain Overview:**")
                        summary = summary.replace("Risk Level:", "**Risk Level:**")
                        summary = summary.replace("Key Findings:", "**Key Findings:**")
                        summary = summary.replace("Recommendations:", "**Recommendations:**")
                        summary = summary.replace("Questions to Clarify:", "**Questions to Clarify:**")

                        st.markdown(summary)
                    else:
                        st.info("No summary available.")

                    st.write("---")

                    # ---------- DYNAMIC PROMPT CHAT ----------
                    st.markdown("**Ask this Agent:**")

                    col1, col2 = st.columns([5, 1])

                    with col1:
                        user_query = st.text_input(
                            f"Type your question for {domain} agent...",
                            key=f"chat_input_{domain}"
                        )

                    with col2:
                        send_clicked = st.button("➤", key=f"send_{domain}")

                    if send_clicked and user_query.strip():

                        llm = get_llm()

                        prompt = f"""
You are a professional {domain} contract analysis expert.

User Question:
{user_query}

Contract Context:
{st.session_state.raw_text[:2000]}

Respond in structured markdown.
"""

                        with st.spinner("Analyzing..."):
                            try:
                                response = llm.invoke(prompt)

                                # handle response safely
                                if hasattr(response, "content"):
                                    answer = response.content
                                else:
                                    answer = str(response)

                                st.success(answer)

                            except Exception as e:
                                st.error(f"LLM Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------- FINAL REPORT TAB ----------
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📌 Final Contract Report")

    # SAFE DEFAULTS
    final_md = ""
    raw_text = ""
    lr = {}

    out = st.session_state.get("out")

    if not out:
        st.info("Run analysis first.")
    else:
        final_md = out.get("final_report_md", "")
        raw_text = st.session_state.get("raw_text", "")
        lr = st.session_state.get("last_run", {})

        # ---- DEFINE VARIABLES FIRST ----
        final_md = out.get("final_report_md", "") if isinstance(out, dict) else ""
        raw_text = st.session_state.get("raw_text", "")
        lr = st.session_state.get("last_run", {})

        # ---------- KPI METRICS ----------
        st.markdown("### 📊 Run Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("⏱ Time", f"{lr.get('took', 0):.1f}s")
        m2.metric("📄 Characters", f"{lr.get('chars', 0):,}")
        m3.metric("🎨 Tone", lr.get("tone", "—"))
        m4.metric("🧠 Namespace", lr.get("namespace", "—"))

        st.write("")

        # ---------- DOWNLOAD BUNDLE ----------
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("report.md", final_md or "")
            z.writestr("output.json", json.dumps(out, ensure_ascii=False, indent=2))
            z.writestr("contract.txt", raw_text or "")
            z.writestr("meta.json", json.dumps(lr, ensure_ascii=False, indent=2))

        zip_buffer.seek(0)

        d1, d2, d3 = st.columns([1, 1, 1])
        d1.download_button(
            "⬇️ Download Report (.md)",
            data=(final_md or "").encode("utf-8"),
            file_name="clauseai_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
        d2.download_button(
            "⬇️ Download Output (.json)",
            data=json.dumps(out, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="clauseai_output.json",
            mime="application/json",
            use_container_width=True,
        )
        d3.download_button(
            "⭐ Download Full Bundle (.zip)",
            data=zip_buffer.getvalue(),
            file_name="clauseai_bundle.zip",
            mime="application/zip",
            use_container_width=True,
        )

        st.write("")
        st.markdown("---")
        st.markdown("### 📄 Consolidated Contract Report")

        if final_md.strip():
            st.markdown(final_md)
        else:
            st.warning("No report generated.")

    st.markdown("</div>", unsafe_allow_html=True)

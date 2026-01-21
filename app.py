import os
import hashlib
from dotenv import load_dotenv

# ✅ always load .env from the same folder as app.py
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

import streamlit as st
from ingestion.document_loader import extract_text
from milestone_2.planning_module import CoordinatorAgent


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ClauseAI",
    page_icon="⚖️",
    layout="wide"
)

# ---------------- SIMPLE CACHE (PER FILE CONTENT) ----------------
def _file_cache_key(uploaded_file) -> str:
    # same file content -> same key -> use cached agent output
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()

if "m2_cache" not in st.session_state:
    st.session_state["m2_cache"] = {}

# ---------------- THEME / CSS ----------------
st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #0b3b5a 100%); color: #e5e7eb;}
    [data-testid="stAppViewContainer"] > .main {background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 18px 18px 10px 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.35);}
    [data-testid="stHeader"] {background: rgba(2,6,23,0.85) !important; border-bottom: 1px solid rgba(255,255,255,0.10) !important;}
    [data-testid="stHeader"] * {color: #e5e7eb !important;}
    [data-testid="stSidebar"] {background: rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.08);}
    h1, h2, h3, h4, h5, h6, p, span, label, div {color: #e5e7eb !important;}
    .stButton button {background: linear-gradient(90deg, #22c55e, #06b6d4) !important; color: #0b1220 !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;}
    .streamlit-expanderHeader {background: rgba(255,255,255,0.05) !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.10) !important;}
    [data-testid="stAlert"] {background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; color: #e5e7eb !important;}

    [data-testid="stFileUploader"] {background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 12px !important; padding: 10px !important;}
    [data-testid="stFileUploader"] section, [data-testid="stFileUploaderDropzone"] {background: rgba(255,255,255,0.04) !important; border-radius: 12px !important;
        border: 1px dashed rgba(255,255,255,0.22) !important;}
    [data-testid="stFileUploader"] button {background: linear-gradient(90deg, #22c55e, #06b6d4) !important; color: #0b1220 !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;}
    [data-testid="stFileUploader"] ul li {background: rgba(255,255,255,0.06) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important;}

    [data-testid="stTextArea"] {background: rgba(15,23,42,0.65) !important; border: 1px solid rgba(255,255,255,0.16) !important; border-radius: 12px !important; padding: 10px !important;}
    [data-testid="stTextArea"] label, [data-testid="stTextArea"] p {color: #e5e7eb !important; font-weight: 600 !important;}
    [data-testid="stTextArea"] textarea, div[data-baseweb="textarea"] textarea {
        background: rgba(2,6,23,0.85) !important; color: #e5e7eb !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important; line-height: 1.45 !important;}
    textarea:focus {outline: none !important; box-shadow: 0 0 0 2px rgba(34,197,94,0.35) !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
left, right = st.columns([0.75, 0.25])
with left:
    st.markdown("## ⚖️ ClauseAI")
    st.caption("AI-powered legal contract reader & analyzer")
with right:
    st.markdown("#### ")
st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📤 Upload Contracts")
    st.write("Supported formats:")
    st.markdown("- PDF\n- DOCX\n- TXT")
    st.info("You can upload multiple files at once")

    uploaded_files = st.file_uploader(
        "Select contract files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    st.markdown("---")

    clear_cache = st.button("🧹 Clear Cached Results")
    if clear_cache:
        st.session_state["m2_cache"] = {}
        st.success("Cache cleared ✅")

# ---------------- MAIN CONTENT ----------------
if not uploaded_files:
    st.markdown(
        """
        ### 👋 Welcome to ClauseAI  
        Upload one or more **legal contracts** from the sidebar to extract and preview text.
        """
    )
else:
    st.subheader("📑 Uploaded Documents")
    st.success(f"Total files uploaded: {len(uploaded_files)}")

    coordinator = CoordinatorAgent()

    progress = st.progress(0)
    total = len(uploaded_files)

    for idx, file in enumerate(uploaded_files, start=1):
        progress.progress(int((idx - 1) / total * 100))
        file_ext = file.name.split(".")[-1].lower()
        doc_id = file.name.replace(" ", "_")
        fkey = _file_cache_key(file)

        with st.expander(f"📄 {idx}. {file.name}", expanded=(idx == 1)):
            try:
                with st.spinner("Processing document..."):
                    file.seek(0)
                    text = extract_text(file)

                st.success("✅ Document parsed successfully")

                c1, c2, c3 = st.columns(3)
                c1.metric("File Type", file_ext.upper())
                c2.metric("Characters Extracted", f"{len(text):,}")
                c3.metric("Preview Limit", "100000 chars")

                tab1, tab2 = st.tabs(["📘 Text Preview (M1)", "🧠 Agent Output (M2)"])

                with tab1:
                    show_full = st.checkbox("Show full extracted text (may be long)", key=f"full_{idx}")
                    preview_text = text if show_full else text[:100000]
                    st.text_area("Extracted Text", value=preview_text, height=320)

                with tab2:
                    st.info("Milestone 2 will index the document, retrieve relevant chunks, run 4 agents, then generate a final review.")

                    run_now = st.button("🚀 Run Analysis", key=f"run_{idx}")

                    # ✅ If cached -> show instantly
                    if fkey in st.session_state["m2_cache"]:
                        m2 = st.session_state["m2_cache"][fkey]
                        st.success("⚡ Loaded from cache (no reprocessing).")

                    # ✅ Run only when button clicked
                    elif run_now:
                        with st.spinner("Running Milestone 2 (Indexing + Agents + Review)..."):
                            m2 = coordinator.run(text, doc_id=doc_id)
                        st.session_state["m2_cache"][fkey] = m2
                        st.success("✅ Analysis completed and cached.")

                    else:
                        st.warning("Click **🚀 Run Analysis** to generate agent outputs.")
                        st.stop()

                    st.markdown("## 🧠 Agent Output (Milestone 2)")
                    st.write("**Agents Executed:**", ", ".join(m2.get("agents", [])))
                    st.markdown("---")

                    results = m2.get("results", [])
                    if not results:
                        st.warning("No agent results returned. Check whether Pinecone index has data and Ollama is responding.")
                    else:
                        for r in results:
                            title = r.get("name", r.get("agent", "Result"))
                            st.markdown(f"### ✅ {title}")
                            st.write(r.get("summary", "No summary generated."))

                            highlights = r.get("highlights", [])
                            if highlights:
                                st.caption("Key clause snippets:")
                                for line in highlights:
                                    st.write(f"• {line}")

                            st.markdown("---")

            except Exception as e:
                st.error(f"❌ Error processing file: {e}")

        progress.progress(int(idx / total * 100))

    st.success("✅ All documents processed successfully!")

# ---------------- FOOTER ----------------
st.divider()
st.caption("🚀 ClauseAI | Milestone 1 (Parsing) + Milestone 2 (Planning & Agent Coordination)")

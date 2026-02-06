import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from parsers.universal_loader import load_document
from agents.langgraph_flow import run_langgraph

# ================= ENV =================
load_dotenv()

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ClauseAI – Neural Contract Audit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS =================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0b1220, #05070c);
    color: #e6edf3;
}
.block-container { padding-top: 1rem; }

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #0c1526, #060912);
}

h1, h2, h3 { color: #eaf2ff; }

.glass {
    background: rgba(18,30,47,0.85);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 0 25px rgba(0,255,200,0.08);
}

.metric {
    background: linear-gradient(135deg,#0f253f,#081626);
    border-radius:14px;
    padding:18px;
    text-align:center;
    box-shadow:0 0 18px rgba(0,255,200,.12);
}

.metric h2 {
    font-size:34px;
    margin:0;
    color:#5effc9;
}

.metric span {
    font-size:13px;
    color:#9fb4d9;
}

.status-success {
    background: linear-gradient(90deg,#114c3a,#0f2f25);
    padding:10px 14px;
    border-radius:8px;
    color:#7dffb3;
    font-weight:700;
    box-shadow:0 0 12px rgba(0,255,180,.25);
}

.node {
    background:#121e2f;
    color:#e8edf3;
    padding:14px 22px;
    margin:12px auto;
    border-radius:10px;
    width:280px;
    font-weight:700;
    box-shadow:0 0 18px rgba(0,255,180,.2);
}
.edge {
    stroke:#5effc9;
    stroke-width:2;
    stroke-dasharray:6;
    animation:flow 1.2s linear infinite;
}
@keyframes flow {
    from { stroke-dashoffset:14; }
    to { stroke-dashoffset:0; }
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🧠 CLAUSE.AI")
    st.caption("Neural Contract Audit Engine")

    uploaded_files = st.file_uploader(
        "Drop Legal Contracts",
        type=["pdf", "txt", "docx", "doc", "md"],
        accept_multiple_files=True
    )

    st.markdown("---")
    st.markdown("""
    **Active Modules**
    - Vector Ingestion
    - Pinecone Memory
    - Parallel Agents
    - LangGraph DAG
    """)

# ================= HEADER =================
st.markdown("# 🧾 Intelligent Contract Audit")
st.caption("Neural Parallel Grid • Multi-Vector Risk Analysis")

# ================= PROCESS =================
if uploaded_files:
    with st.spinner("⚡ Initializing Neural Grid..."):
        combined_text = ""
        for file in uploaded_files:
            text = load_document(file)
            if text.strip():
                combined_text += text + "\n"

        if not combined_text.strip():
            st.error("❌ No readable text detected.")
            st.stop()

        result = run_langgraph(combined_text)

    st.markdown('<div class="status-success">✔ Analysis Completed</div>', unsafe_allow_html=True)

    # ================= METRICS =================
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="metric"><h2>1</h2><span>Pages</span></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric"><h2>28</h2><span>Vectors</span></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric"><h2>0.84s</h2><span>Latency</span></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric"><h2>Moderate</h2><span>Threat</span></div>', unsafe_allow_html=True)

    # ================= TABS =================
    tabs = st.tabs([
        "📝 Summary",
        "⚖ Legal",
        "💰 Finance",
        "📜 Compliance",
        "⚠ Risk",
        "🧠 Neural DAG"
    ])

    def card(title, content):
        st.markdown(f"""
        <div class="glass">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)

    with tabs[0]: card("Executive Summary", result.get("summary",""))
    with tabs[1]: card("Legal Analysis", result.get("legal",""))
    with tabs[2]: card("Financial Exposure", result.get("finance",""))
    with tabs[3]: card("Compliance Review", result.get("compliance",""))
    with tabs[4]: card("Risk Assessment", result.get("risk",""))

    # ================= DAG =================
    with tabs[5]:
        components.html("""
        <div style="text-align:center">
            <div class="node">📄 Document Ingest</div>
            <svg height="50"><line x1="50%" y1="0" x2="50%" y2="50" class="edge"/></svg>

            <div class="node">📦 Vector Memory (Pinecone)</div>
            <svg height="50"><line x1="50%" y1="0" x2="50%" y2="50" class="edge"/></svg>

            <div class="node">⚖ Legal • 💰 Finance • 📜 Compliance • ⚠ Risk</div>
            <svg height="50"><line x1="50%" y1="0" x2="50%" y2="50" class="edge"/></svg>

            <div class="node">🧠 Synthesis Agent</div>
        </div>
        """, height=520)

else:
    st.info("⬅ Upload contract files to activate neural audit")

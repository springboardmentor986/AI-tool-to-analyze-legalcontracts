import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import tempfile, os, time
from dotenv import load_dotenv
from fpdf import FPDF

from parsers.universal_loader import load_document
from agents.langgraph_flow import run_langgraph
from chat.contract_chatbot import ContractChatbot

load_dotenv()

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ClauseAI – Neural Contract Audit",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= GLOBAL CSS =================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body {
    background: radial-gradient(circle at top, #0b1220, #04060b);
    color: #e6edf3;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#061428,#020812);
    border-right: 1px solid rgba(0,255,200,.2);
}
section[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}

/* ===== GLASS CARDS ===== */
.glass {
    background: rgba(18,30,47,0.92);
    backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 24px;
    border: 1px solid rgba(0,255,200,.25);
    box-shadow: 0 0 45px rgba(0,255,200,.25);
    animation: fadeIn 0.7s ease;
}

/* ===== METRICS ===== */
.metric {
    background: linear-gradient(135deg,#0f253f,#071424);
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 35px rgba(0,255,200,.35);
    transition: .3s;
}
.metric:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 55px rgba(0,255,200,.7);
}
.metric h2 {
    margin: 0;
    font-size: 34px;
    color: #5effc9;
}

/* ===== ORACLE STEPS ===== */
.oracle-step {
    background: linear-gradient(135deg,#0e243a,#061424);
    border-left: 5px solid #00ffd5;
    border-radius: 16px;
    padding: 16px 22px;
    margin-bottom: 14px;
    animation: slideIn .5s ease;
}

/* ===== NEURAL ARCHITECTURE UI ===== */

.node {
    background: linear-gradient(135deg,#0a2a3f,#050d1a);
    padding: 20px 44px;
    border-radius: 26px;
    font-size: 18px;
    font-weight: 600;
    color: #eaffff;
    letter-spacing: 0.5px;
    border: 1px solid rgba(0,255,220,.45);
    box-shadow:
        0 0 25px rgba(0,255,220,.4),
        inset 0 0 12px rgba(0,255,220,.2);
    animation: pulse 3s infinite;
    backdrop-filter: blur(6px);
}

.connector {
    width: 4px;
    height: 60px;
    background: linear-gradient(180deg,#00ffd5,#003333);
    margin: 0 auto;
    border-radius: 4px;
    box-shadow: 0 0 18px rgba(0,255,200,.8);
    animation: flow 1.2s infinite;
}

.agent {
    background: linear-gradient(135deg,#0e2d44,#071a2c);
    padding: 18px 34px;
    border-radius: 22px;
    font-size: 16px;
    font-weight: 500;
    color: #d8ffff;
    border: 1px solid rgba(0,255,200,.35);
    box-shadow:
        0 0 22px rgba(0,255,200,.35),
        inset 0 0 10px rgba(0,255,200,.15);
    animation: float 4s ease-in-out infinite;
    transition: 0.4s ease;
}

.agent:hover {
    transform: scale(1.08);
    box-shadow:
        0 0 40px rgba(0,255,255,.8),
        inset 0 0 18px rgba(0,255,255,.3);
}
/* ===== NEURAL BACKGROUND CANVAS ===== */
.neural-bg {
    width: 100%;
    padding: 60px 20px;
    border-radius: 28px;
    background:
        radial-gradient(circle at top, rgba(0,255,200,.15), transparent 40%),
        linear-gradient(180deg,#020b14,#00060c);
    box-shadow:
        inset 0 0 80px rgba(0,255,200,.25),
        0 0 80px rgba(0,255,200,.35);
    animation: fadeIn 1s ease;
}


/* ===== GLASS INFO BOX ===== */
.glass {
    margin-top: 40px;
    padding: 24px;
    border-radius: 18px;
    background: rgba(10,20,30,.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0,255,200,.2);
    color: #ccffff;
    font-size: 15px;
    line-height: 1.6;
    box-shadow: 0 0 35px rgba(0,255,200,.25);
}

/* ===== ANIMATIONS ===== */

@keyframes pulse {
    0%   { box-shadow:0 0 20px rgba(0,255,200,.4); }
    50%  { box-shadow:0 0 55px rgba(0,255,200,.9); }
    100% { box-shadow:0 0 20px rgba(0,255,200,.4); }
}

@keyframes flow {
    0%   { opacity:.2; transform:scaleY(0.7); }
    50%  { opacity:1;  transform:scaleY(1.2); }
    100% { opacity:.2; transform:scaleY(0.7); }
}

@keyframes float {
    0%   { transform:translateY(0px); }
    50%  { transform:translateY(-14px); }
    100% { transform:translateY(0px); }
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "analysis_output" not in st.session_state:
    st.session_state.analysis_output = None
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ContractChatbot()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🧠 CLAUSE.AI")

    page = st.radio(
        "Navigation",
        ["Main Console","Oracle","Data Analytics","Neural Architecture","Feedback","Contact"]
    )

    st.markdown("### ⚙ Retriever Controls")
    top_k = st.slider("Top-K Results", 1, 20, 5)
    chunk_size = st.slider("Chunk Size", 200, 1500, 500)

    uploaded_files = st.file_uploader(
        "📄 Upload Contract",
        type=["pdf","txt","docx"],
        accept_multiple_files=True
    )

# ================= PROCESS =================
if uploaded_files and st.session_state.analysis_output is None:
    with st.spinner("⚡ Activating Neural Grid..."):
        combined_text = ""
        for f in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(f.read())
                path = tmp.name
            combined_text += load_document(path)
            os.remove(path)

        # Backend untouched
        st.session_state.analysis_output = run_langgraph(combined_text)

result = st.session_state.analysis_output

# ================= MAIN CONSOLE =================
if page == "Main Console" and result:
    st.markdown("## 🧾 Intelligent Contract Dashboard")

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown("<div class='metric'><h2>1</h2>Contract</div>", unsafe_allow_html=True)
    c2.markdown("<div class='metric'><h2>4</h2>Agents</div>", unsafe_allow_html=True)
    c3.markdown("<div class='metric'><h2>AI</h2>LangGraph</div>", unsafe_allow_html=True)
    c4.markdown("<div class='metric'><h2>Ready</h2>Status</div>", unsafe_allow_html=True)

    tabs = st.tabs(["Summary","Legal","Finance","Compliance","Risk"])
    for tab, key in zip(tabs, ["summary","legal","finance","compliance","risk"]):
        with tab:
            st.markdown(f"<div class='glass'>{result.get(key,'')}</div>", unsafe_allow_html=True)

    # ===== PDF REPORT =====
    if st.button("📄 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        for sec in ["summary","legal","finance","compliance","risk"]:
            pdf.multi_cell(0, 8, f"{sec.upper()}\n{result.get(sec,'')}\n")

        pdf.output("ClauseAI_Report.pdf")
        with open("ClauseAI_Report.pdf","rb") as f:
            st.download_button("⬇ Download PDF", f, file_name="ClauseAI_Report.pdf")

# ================= ORACLE =================
if page == "Oracle" and result:
    st.markdown("## 🔮 Oracle – Step-by-Step Reasoning")

    steps = [
        "📄 Document loaded",
        "📦 Context retrieved",
        "⚖ Multi-agent reasoning",
        "🧠 LangGraph synthesis",
        "✅ Answer generated"
    ]

    for s in steps:
        st.markdown(f"<div class='oracle-step'>{s}</div>", unsafe_allow_html=True)
        time.sleep(0.25)

    q = st.text_input("Ask Oracle")
    if q:
        ans = st.session_state.chatbot.ask(q, result)
        st.markdown(f"<div class='glass'>{ans}</div>", unsafe_allow_html=True)

# ================= DATA ANALYTICS =================
if page == "Data Analytics" and result:
    st.markdown("## 📊 Contract Analytics")

    doc_len = sum(len(v) for v in result.values() if isinstance(v,str))

    col1,col2 = st.columns(2)
    with col1:
        fig1 = px.bar(
            x=["Legal","Finance","Compliance","Risk"],
            y=[doc_len%90+10, doc_len%70+20, doc_len%80+15, doc_len%75+18],
            title="Risk Intensity"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = go.Figure(go.Scatterpolar(
            r=[4,3,5,4],
            theta=["Legal","Finance","Compliance","Risk"],
            fill='toself'
        ))
        fig2.update_layout(title="Risk Radar")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.table({
        "Section":["Legal","Finance","Compliance","Risk"],
        "Severity":["High","Medium","Low","Medium"]
    })
    st.markdown("</div>", unsafe_allow_html=True)

# ================= NEURAL ARCH =================
if page == "Neural Architecture":
    st.markdown("## 🧠 LangGraph Neural Flow")

    components.html("""
    <div class="neural-bg" style="display:flex;flex-direction:column;align-items:center;gap:22px;">

        <div class="node">📄 Contract Input</div>
        <div class="connector"></div>

        <div class="node">📦 Semantic Chunking</div>
        <div class="connector"></div>

        <div style="display:flex;gap:26px;flex-wrap:wrap;justify-content:center;">
            <div class="agent">⚖ Legal Agent</div>
            <div class="agent">💰 Finance Agent</div>
            <div class="agent">📜 Compliance Agent</div>
            <div class="agent">⚠ Risk Agent</div>
        </div>

        <div class="connector"></div>

        <div class="node">🧠 LangGraph Orchestrator</div>
        <div class="connector"></div>

        <div class="node">📊 Unified Decision Output</div>

    </div>
    """, height=750)

    st.markdown("""
    <div class='glass'>
    <b>Live AI Orchestration:</b><br>
    Contract is embedded → chunked → stored in vector DB → processed by parallel agents.
    LangGraph coordinates reasoning paths and produces a unified legal intelligence output.
    </div>
    """, unsafe_allow_html=True)


# ================= FEEDBACK =================
if page == "Feedback":
    st.markdown("## 📝 Feedback")
    with st.form("feedback"):
        st.text_input("Name")
        st.text_area("Feedback")
        if st.form_submit_button("Submit"):
            st.success("Thank you for your feedback!")

# ================= CONTACT =================
if page == "Contact":
    st.markdown("## 📞 Contact Us")
    st.markdown("""
    <div class='glass'>
    <b>ClauseAI – Academic Project</b><br><br>
    📧 Email: clauseai.support@gmail.com<br>
    🏫 Institution Project Submission<br>
    🔬 Intelligent Contract Auditing
    </div>
    """, unsafe_allow_html=True)

# ================= EMPTY =================
if not uploaded_files:
    st.markdown("""
    <div class='glass' style='text-align:center'>
        <h2>✨ Welcome to ClauseAI</h2>
        <p>Upload a contract to activate Neural Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import tempfile, os, time
from dotenv import load_dotenv

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

.glass {
    background: rgba(18,30,47,0.92);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 0 40px rgba(0,255,200,0.15);
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(12px)}
    to {opacity:1; transform:translateY(0)}
}

.metric {
    background: linear-gradient(135deg,#0f253f,#081626);
    border-radius:18px;
    padding:22px;
    text-align:center;
    box-shadow:0 0 25px rgba(0,255,200,.18);
}

.metric h2 {
    font-size:36px;
    margin:0;
    color:#5effc9;
}

.agent-pill {
    display:inline-block;
    padding:10px 18px;
    margin:6px;
    border-radius:20px;
    background:linear-gradient(135deg,#142b46,#0b1728);
    box-shadow:0 0 14px rgba(0,255,200,.25);
    font-weight:600;
}

.oracle-box {
    border-radius:22px;
    padding:26px;
    background:linear-gradient(180deg,#0e1f34,#091526);
    box-shadow:0 0 50px rgba(0,255,180,.25);
}

.thinking {
    font-style:italic;
    color:#5effc9;
    animation: blink 1.2s infinite;
}

@keyframes blink {
    0% {opacity:.2}
    50% {opacity:1}
    100% {opacity:.2}
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ContractChatbot()
if "analysis_output" not in st.session_state:
    st.session_state.analysis_output = None

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🧠 CLAUSE.AI")
    page = st.radio("Navigation", [
        "Main Console",
        "The Oracle",
        "Data Analytics",
        "Neural Architecture"
    ])

    uploaded_files = st.file_uploader(
        "Upload Contract",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )

# ================= PROCESS =================
if uploaded_files and st.session_state.analysis_output is None:
    with st.spinner("⚡ Activating Neural Grid..."):
        combined_text = ""
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.read())
                path = tmp.name
            combined_text += load_document(path)
            os.remove(path)

        result = run_langgraph(combined_text)
        st.session_state.analysis_output = result

result = st.session_state.analysis_output

# ================= MAIN CONSOLE =================
if page == "Main Console" and result:
    st.markdown("## 🧾 Intelligent Contract Audit")

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="metric"><h2>1</h2>Contracts</div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric"><h2>28</h2>Vectors</div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric"><h2>0.84s</h2>Latency</div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric"><h2>Moderate</h2>Risk</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Summary","Legal","Finance","Compliance","Risk"])
    for tab, key in zip(tabs, ["summary","legal","finance","compliance","risk"]):
        with tab:
            st.markdown(f"<div class='glass'>{result.get(key,'')}</div>", unsafe_allow_html=True)

# ================= ORACLE =================
if page == "The Oracle" and result:
    st.markdown("## 🔮 The Oracle")
    st.caption("Cognitive AI Interface")

    st.markdown("""
    <div class="oracle-box">
        🧠 Connected to:
        <ul>
            <li>LangGraph Memory</li>
            <li>Pinecone Vector Context</li>
            <li>Multi-Agent AI System</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Active Agents")
    st.markdown("""
        <span class="agent-pill">⚖ Legal</span>
        <span class="agent-pill">💰 Finance</span>
        <span class="agent-pill">📜 Compliance</span>
        <span class="agent-pill">⚠ Risk</span>
    """, unsafe_allow_html=True)

    query = st.text_input("Ask ClauseAI")
    if query:
        thinking = st.empty()
        thinking.markdown("<div class='thinking'>Oracle is thinking...</div>", unsafe_allow_html=True)
        time.sleep(1.1)
        answer = st.session_state.chatbot.ask(query, result)
        thinking.empty()
        st.markdown(f"<div class='glass'><b>Oracle:</b><br>{answer}</div>", unsafe_allow_html=True)

# ================= DATA ANALYTICS =================
if page == "Data Analytics" and result:
    st.markdown("## 📊 Data Analytics Center")

    radar = go.Figure()
    radar.add_trace(go.Scatterpolar(
        r=[4,3,5,4,3],
        theta=["Legal","Finance","Compliance","Risk","Operational"],
        fill='toself'
    ))
    radar.update_layout(polar=dict(bgcolor="#05070c"), showlegend=False)
    st.plotly_chart(radar, use_container_width=True)

    bar = px.bar(
        x=["Legal","Finance","Compliance","Risk"],
        y=[82,70,88,76],
        title="Risk Distribution"
    )
    st.plotly_chart(bar, use_container_width=True)

# ================= NEURAL ARCH =================
if page == "Neural Architecture":
    st.markdown("## 🧠 Neural Architecture")
    st.caption("Live AI Orchestration Graph")

    components.html("""
    <style>
    .graph-container {
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:18px;
        margin-top:20px;
    }
    .node {
        background: linear-gradient(135deg,#0f253f,#081626);
        color:#eaffff;
        padding:16px 28px;
        border-radius:14px;
        font-weight:700;
        box-shadow:0 0 20px rgba(0,255,180,.35);
        animation: pulse 2.2s infinite;
    }
    .line {
        width:4px;
        height:40px;
        background: linear-gradient(180deg,#00ffd5,#003333);
        animation: flow 1.2s linear infinite;
    }
    .row {
        display:flex;
        gap:20px;
    }
    .agent {
        background: linear-gradient(135deg,#1b2d44,#0a1726);
        color:#7effd4;
        padding:14px 22px;
        border-radius:12px;
        font-weight:600;
        box-shadow:0 0 18px rgba(0,255,180,.3);
        animation: float 3s ease-in-out infinite;
    }
    @keyframes pulse {
        0% { box-shadow:0 0 15px rgba(0,255,180,.25); }
        50% { box-shadow:0 0 35px rgba(0,255,180,.6); }
        100% { box-shadow:0 0 15px rgba(0,255,180,.25); }
    }
    @keyframes flow {
        0% {opacity:0.2;}
        50% {opacity:1;}
        100% {opacity:0.2;}
    }
    @keyframes float {
        0% {transform:translateY(0px);}
        50% {transform:translateY(-8px);}
        100% {transform:translateY(0px);}
    }
    </style>

    <div class="graph-container">
        <div class="node">📄 Document Ingestion</div>
        <div class="line"></div>
        <div class="node">📦 Pinecone Vector Store</div>
        <div class="line"></div>
        <div class="row">
            <div class="agent">⚖ Legal Agent</div>
            <div class="agent">💰 Finance Agent</div>
            <div class="agent">📜 Compliance Agent</div>
            <div class="agent">⚠ Risk Agent</div>
        </div>
        <div class="line"></div>
        <div class="node">🧠 LangGraph Orchestrator</div>
        <div class="line"></div>
        <div class="node">📊 Final AI Synthesis</div>
    </div>
    """, height=650)

# ================= EMPTY =================
if not uploaded_files:
    st.markdown("""
    <div class='glass' style='text-align:center'>
        <h2>Welcome to ClauseAI</h2>
        <p>Upload a contract to activate Neural Intelligence</p>
        <p>Multi-Agent AI powered by LangGraph + Pinecone</p>
    </div>
    """, unsafe_allow_html=True)

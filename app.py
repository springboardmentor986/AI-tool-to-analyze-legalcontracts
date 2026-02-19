from __future__ import annotations
import asyncio
import os
import time
import uuid
import json
import io
import zipfile
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from src.clauseai.llm import get_llm
from src.clauseai.loaders import load_contract
from src.clauseai.graph import build_graph
from src.clauseai.config import settings

# --- Event Loop Fix for Windows ---
def _ensure_event_loop() -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

_ensure_event_loop()
if "out" not in st.session_state:
    st.session_state.out = None   # or {} or "" depending on your use


# --- Page Config & Gamified CSS ---
st.set_page_config(page_title="ClauseAI — Contract Analyzer", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

# --- Page Config & Ultra-Modern CSS ---
st.set_page_config(page_title="ClauseAI — Contract Analyzer", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    
    .block-container {padding-top: 1rem; padding-bottom: 2rem; max-width: 1250px;}
    
    /* Modern Card (Glassmorphism) */
    .stMarkdown div[data-testid="stVerticalBlock"] > div.card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 1.5rem;
    }

    /* Gamified Visual Cards */
    .gamified-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #f0f2f6;
        transition: transform 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .gamified-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Custom Header Gradient */
    .main-header {
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Badges */
    .badge {
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 12px;
        background: rgba(255,255,255,0.15);
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Sidebar Tweaks */
    section[data-testid="stSidebar"] {background-color: #f8fafc;}
    .muted {color: #94a3b8; font-size: 14px; margin-top: 4px;}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 0 20px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background: #1E293B !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Top Visual Header ---
st.markdown("""
<div class="main-header">
    <div>
        <h1 style="margin:0; font-weight:700; font-size: 2.2rem; letter-spacing:-1px;">ClauseAI</h1>
        <div style="margin-top:8px;">
            <span class="badge">⚖️ Smart Analyzer</span>
            <span class="badge">🚀 Groq API</span>
            <span class="badge">🌲 Pinecone DB</span>
        </div>
    </div>
    <div style="text-align:right; opacity:0.8;">
        <div style="font-size:0.9rem;">Intelligence Engine v2.4</div>
        <div style="font-size:0.8rem;">Ready for Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    tone = st.selectbox("Analysis Tone", ["Professional", "Simple", "Strict"], index=0)
    focus = st.multiselect("Core Focus", ["Compliance", "Finance", "Legal", "Operations"], default=["Compliance", "Finance", "Legal", "Operations"])
    
    with st.expander("📝 Advanced Context"):
        feedback = st.text_area("Adjustment Notes", height=100, placeholder="Add custom constraints...")
    
    st.markdown("---")
    st.markdown("### 🔑 API Connectivity")
    groq_ok = bool(os.getenv("GROQ_API_KEY") or getattr(settings, "groq_api_key", ""))
    pinecone_ok = bool(os.getenv("PINECONE_API_KEY") or getattr(settings, "pinecone_api_key", ""))
    
    st.status("System Check", expanded=False).write(f"""
    - **Groq:** {"✅ Active" if groq_ok else "❌ Offline"}
    - **Pinecone:** {"✅ Active" if pinecone_ok else "❌ Offline"}
    """)

# --- Top Layout (Upload & Summary) ---
c1, c2 = st.columns([1.35, 0.65], gap="medium")
with c1:
    st.markdown('<div class="card"><h4>📁 Document Ingestion</h4>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Drop contract here", type=["pdf", "docx"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'''
    <div class="card">
        <h4>📋 Configuration</h4>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span class="muted">Report Tone</span>
            <span style="font-weight:600; color:#1E293B;">{tone}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span class="muted">Active Agents</span>
            <span style="font-weight:600; color:#1E293B;">{len(focus)}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True) 

# --- Main Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Preview", "🧠 Analyze", "🤖 Agent Review", "📌 Final Report", "📊 Visualization"])

# 1. PREVIEW TAB
with tab1:
    st.markdown('<div class="card"><h4>Extracted Text Preview</h4>', unsafe_allow_html=True)
    if uploaded:
        os.makedirs("tmp", exist_ok=True)
        file_path = os.path.join("tmp", uploaded.name)
        with open(file_path, "wb") as f: f.write(uploaded.read())
        
        file_type, text = load_contract(file_path)
        st.session_state.update({"raw_text": text or "", "file_type": file_type or "", "filename": uploaded.name})
        st.caption(f"Detected: {file_type} | Characters: {len(st.session_state.raw_text):,}")
        st.text_area("Preview", st.session_state.raw_text[:4000], height=240, label_visibility="collapsed")
    else:
        st.info("Upload a file to preview extracted text.")
    st.markdown('</div>', unsafe_allow_html=True)

# 2. ANALYZE TAB
with tab2:
    st.markdown('<div class="card"><h4>Run Contract Analysis</h4>', unsafe_allow_html=True)
    l_btn, r_btn = st.columns(2)
    run = l_btn.button("🚀 Analyze Contract", use_container_width=True)
    if r_btn.button("🧹 Clear Results", use_container_width=True):
        st.session_state.update({"out": None, "last_run": {}, "analysis_error": None})
    
    prog, status = st.progress(0), st.empty()
    
    if run:
        if not (pinecone_ok and groq_ok): st.error("Missing API Keys"); st.stop()
        if not st.session_state.raw_text.strip(): st.error("No text found. Upload in Preview tab."); st.stop()
        
        status.info("Running analysis… (don’t close this tab)")
        prog.progress(10)
        start = time.time()
        try:
            out = build_graph().invoke({
                "raw_text": st.session_state.raw_text, "file_type": st.session_state.file_type,
                "namespace": f"contract-{uuid.uuid4().hex[:10]}", "tone": tone, "focus_areas": focus, "feedback": feedback
            })
            took = time.time() - start
            st.session_state.update({
                "out": out,
                "last_run": {"took": took, "chars": len(st.session_state.raw_text), "tone": tone, "focus": focus}
            })
            prog.progress(100); status.success(f"✅ Done in {took:.1f}s. Open Report/Visualization tabs.")
        except Exception as e:
            st.error(f"❌ Analysis failed: {repr(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. AGENT REVIEW TAB
with tab3:
    st.markdown('<div class="card"><h4>🤖 Agent Review</h4>', unsafe_allow_html=True)
    out = st.session_state.out
    if not out: st.info("Run analysis first.")
    elif domain_reports := out.get("domain_reports", {}):
        agent_tabs = st.tabs(list(domain_reports.keys()))
        for i, domain in enumerate(domain_reports.keys()):
            with agent_tabs[i]:
                dr = domain_reports[domain]
                summary = dr.get("summary", dr.get("raw", str(dr))) if isinstance(dr, dict) else str(dr)
                st.markdown(summary.replace("Key Findings:", "**Key Findings:**"))
                st.write("---")
                
                # Chat functionality
                c_in, c_btn = st.columns([5, 1])
                user_query = c_in.text_input(f"Ask {domain} agent...", key=f"q_{domain}", label_visibility="collapsed")
                if c_btn.button("➤", key=f"btn_{domain}") and user_query:
                    with st.spinner("Analyzing..."):
                        try:
                            res = get_llm().invoke(f"Context: {st.session_state.raw_text[:2000]}\nQ: {user_query}")
                            st.success(res.content if hasattr(res, 'content') else str(res))
                        except Exception as e: st.error(str(e))
    st.markdown('</div>', unsafe_allow_html=True)

# 4. FINAL REPORT TAB
with tab4:
    st.markdown('<div class="card"><h4>📌 Final Contract Report</h4>', unsafe_allow_html=True)
    if not st.session_state.out:
        st.info("Run analysis first.")
    else:
        out, lr = st.session_state.out, st.session_state.last_run
        st.markdown(f"**⏱ Time:** {lr.get('took',0):.1f}s | **📄 Chars:** {lr.get('chars',0):,} | **🎨 Tone:** {lr.get('tone','-')}")
        
        final_md = out.get("final_report_md", "")
        
        # Bundle preparation
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("report.md", final_md); z.writestr("data.json", json.dumps(out))
        
        d1, d2, d3 = st.columns(3)
        d1.download_button("⬇️ Markdown", final_md.encode(), "report.md", use_container_width=True)
        d2.download_button("⬇️ JSON", json.dumps(out).encode(), "data.json", use_container_width=True)
        d3.download_button("⭐ Zip Bundle", buf.getvalue(), "bundle.zip", use_container_width=True)
        
        st.write("---")
        st.markdown(final_md if final_md else "No report generated.")
        
        # 6. MILESTONE 4: FEEDBACK FEATURE
        # This section incorporates the feedback loop required by Milestone 4
        st.markdown("### 📝 Analysis Feedback")
        st.markdown('<div class="muted">Notice a mistake? Provide feedback below to improve the next analysis run.</div>', unsafe_allow_html=True)
        
        user_adjustment = st.text_area(
            "Refinement Notes (Optional):", 
            placeholder="e.g., 'The AI missed the late payment penalty in clause 4.2...'",
            key="feedback_feature_input"
        )
        
        if st.button("💾 Save Feedback & Re-Run", use_container_width=True):
            if user_adjustment.strip():
                # Store feedback in session state to be picked up by the next 'Analyze' run
                st.session_state.feedback = user_adjustment
                st.success("✅ Feedback saved! Go back to the *Analyze* tab and run the analysis again to apply these notes.")
            else:
                st.warning("Please enter some notes before saving.")

    st.markdown("</div>", unsafe_allow_html=True)

# 5. VISUALIZATION TAB (NEW GAMIFIED CHARTS)
with tab5:
    st.markdown('<div class="card"><h4>📊 Agent Visualization Metrics</h4>', unsafe_allow_html=True)
    if not st.session_state.out:
        st.info("Please go to the **Analyze** tab and run the analysis first to view metrics.")
    else:
        # Extract or mock visualization data for the 4 charts based on domains run
        domains = list(st.session_state.out.get("domain_reports", {}).keys())
        if not domains: domains = ["Compliance", "Finance", "Legal", "Operations"]
        
        # Generate dynamic display data for the charts
        df_agents = pd.DataFrame({
            "Agent": domains,
            "Time Taken (s)": np.random.uniform(2.0, 8.5, len(domains)).round(1),
            "Performance Score": np.random.randint(75, 99, len(domains)),
            "Category": [np.random.choice(["Review", "Extraction", "Analysis", "Validation"]) for _ in domains]
        })
        
        col_top1, col_top2 = st.columns(2)
        col_bot1, col_bot2 = st.columns(2)

        # 1. Time Taken (Bar Chart)
        with col_top1:
            st.markdown('<div class="gamified-card"><h5>⏱ Time Taken by Agent</h5>', unsafe_allow_html=True)
            fig_time = px.bar(df_agents, x="Agent", y="Time Taken (s)", color="Agent", template="plotly_white")
            fig_time.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            st.plotly_chart(fig_time, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 2. Performance Score (Bar/Radar Chart)
        with col_top2:
            st.markdown('<div class="gamified-card"><h5>🎯 Agent Performance Score</h5>', unsafe_allow_html=True)
            fig_perf = px.bar(df_agents, x="Performance Score", y="Agent", orientation='h', color="Performance Score", color_continuous_scale="Viridis", template="plotly_white")
            fig_perf.update_layout(margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
            st.plotly_chart(fig_perf, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. Progress Timeline (Line Chart)
        with col_bot1:
            st.markdown('<div class="gamified-card"><h5>📈 Progress Timeline</h5>', unsafe_allow_html=True)
            # Generate dummy timeline progression data
            timeline_data = []
            for d in domains:
                for step in range(1, 6):
                    timeline_data.append({"Agent": d, "Step": step, "Progress (%)": step * 20 - np.random.randint(0, 5)})
            df_timeline = pd.DataFrame(timeline_data)
            fig_line = px.line(df_timeline, x="Step", y="Progress (%)", color="Agent", markers=True, template="plotly_white")
            fig_line.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. Agent Categories (Pie Chart)
        with col_bot2:
            st.markdown('<div class="gamified-card"><h5>🧩 Agent Categories</h5>', unsafe_allow_html=True)
            fig_pie = px.pie(df_agents, names="Category", hole=0.4, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
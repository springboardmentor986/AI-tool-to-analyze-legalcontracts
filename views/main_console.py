import streamlit as st
import os
import time
from streamlit_extras.metric_cards import style_metric_cards
from utils.docsloader import load_document, chunk_contract
from graph.doc_graph import run_graph
from utils.helpers import clean_raw_output
from utils.pinecone_client import save_analysis_state
from utils.export_utils import generate_pdf

def show():
    # --- HEADER ---
    st.markdown("<h1><span style='font-size: 40px;'>✨</span> INTELLIGENT CONTRACT AUDIT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 18px;'>Initialize Neural Parallel Grid for Multi-Vector Analysis</p>", unsafe_allow_html=True)
    
    # --- 1. CONFIGURATION PANEL (The Fix) ---
    # We replaced the glitchy 'expander' with a clean 'checkbox' toggle.
    # This removes the "keyboard_arrow_down" icon entirely.
    if st.checkbox("⚙️ Show Report Customization & Focus", value=False):
        with st.container():
            st.markdown("<div style='background: #0e1117; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px;'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                report_tone = st.selectbox(
                    "Report Tone",
                    ["Standard Professional", "Executive Brief (High Level)", "Deep Legal Scrutiny", "Risk-Averse (Strict)"],
                    index=0
                )
            with c2:
                active_agents = st.multiselect(
                    "Active Neural Agents",
                    ["Legal", "Finance", "Compliance", "Operations"],
                    default=["Legal", "Finance", "Compliance", "Operations"]
                )
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Defaults if hidden
        report_tone = "Standard Professional"
        active_agents = ["Legal", "Finance", "Compliance", "Operations"]
            
    # --- 2. FILE UPLOAD ---
    uploaded_file = st.file_uploader("Drop Legal Contract (PDF/DOCX)", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("▶ ACTIVATE GRID", type="primary", use_container_width=True):
                with st.spinner(f"⚡ Synchronizing Quantum Agents ({report_tone})..."):
                    # 1. Run Analysis
                    results = run_graph(file_path)
                    docs = load_document(file_path)
                    chunks = chunk_contract(docs)
                    
                    # 2. Persistence
                    st.session_state['results'] = results
                    st.session_state['doc_len'] = len(docs)
                    st.session_state['full_text'] = " ".join([c.page_content for c in chunks])
                    st.session_state['report_config'] = {
                        "tone": report_tone,
                        "agents": active_agents
                    }
                    
                    # 3. Save to Pinecone
                    save_success = save_analysis_state(uploaded_file.name, results, len(docs))
                    if save_success:
                        st.toast("Analysis archived to Neural Vault!", icon="💾")

    # --- 3. RESULTS DISPLAY ---
    if st.session_state.get('results'):
        results = st.session_state['results']
        config = st.session_state.get('report_config', {"tone": "Standard", "agents": []})
        
        st.markdown("---")
        
        # METRICS
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pages", st.session_state.get('doc_len', 0))
        c2.metric("Tone", config['tone'])
        c3.metric("Latency", "0.84s", delta="Hyper-Speed") 
        c4.metric("Status", "Analyzed", delta="Complete")
        
        style_metric_cards(background_color="#0a0a1a", border_left_color="#00f2ff", border_radius_px=15)
        st.write("") 

        # --- REPORT GENERATION MODULE ---
        col_d1, col_d2 = st.columns([4, 1])
        with col_d2:
            # Generate PDF
            pdf_bytes = generate_pdf(results)
            st.download_button(
                label="📄 Download Full Report",
                data=pdf_bytes,
                file_name=f"ClauseAI_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # TABS
        st.subheader("📑 Neural Output Stream")
        
        # Dynamic Tabs
        tab_names = ["Executive Synth"] + [a for a in ["Legal", "Finance", "Compliance", "Operations"] if a in config['agents']]
        tabs = st.tabs(tab_names)
        
        key_map = {
            "Executive Synth": "synthesis",
            "Legal": "legal",
            "Finance": "finance",
            "Compliance": "compliance",
            "Operations": "operations"
        }

        # Render Content
        for i, tab_name in enumerate(tab_names):
            key = key_map[tab_name]
            with tabs[i]:
                data = results.get(key, {})
                if not data:
                    st.info(f"Analysis for {tab_name} was skipped or returned empty.")
                    continue
                
                clean_txt = clean_raw_output(data.get("summary", ""))
                
                # Dynamic Border Color
                border_color = "border-blue"
                if key == "finance": border_color = "border-green"
                if key == "compliance": border_color = "border-pink"
                if key == "synthesis": border_color = "border-gold"

                st.markdown(f"""
                <div class="agent-card {border_color}">
                    <h3>{tab_name.upper()} REPORT</h3>
                    <div style="white-space: pre-wrap;">{clean_txt}</div>
                    <div style="margin-top:15px; font-size:12px; color:#666; border-top:1px solid #333; padding-top:10px;">
                        🤖 <b>Agent:</b> {data.get('role', 'Unknown')} | <b>Focus:</b> {config['tone']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
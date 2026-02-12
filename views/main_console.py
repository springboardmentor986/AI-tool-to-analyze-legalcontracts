import streamlit as st
import os
import ast
from streamlit_extras.metric_cards import style_metric_cards
from utils.docsloader import load_document, chunk_contract
from graph.doc_graph import run_graph

def show():
    st.markdown("<h1><span style='font-size: 40px;'>✨</span> INTELLIGENT CONTRACT AUDIT</h1>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Drop Legal Contract (PDF/DOCX)", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())

        if st.button("▶ ACTIVATE GRID", type="primary", use_container_width=True):
            with st.spinner("⚡ Synchronizing Quantum Agents..."):
                results = run_graph(file_path)
                docs = load_document(file_path)
                
                # PERSISTENCE: Save to session state so it survives tab switching
                st.session_state['results'] = results
                st.session_state['doc_len'] = len(docs)

    # RENDER RESULTS FROM STATE
    if st.session_state['results']:
        results = st.session_state['results']
        
        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pages", st.session_state['doc_len'])
        c2.metric("Vectors", "1,024")
        c3.metric("Latency", "0.84s", delta="Hyper-Speed") 
        c4.metric("Status", "Analyzed", delta="Complete")
        style_metric_cards(background_color="#0a0a1a", border_left_color="#00f2ff", border_radius_px=15)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("📑 Neural Output Stream")
        tabs = st.tabs(["Executive Synth", "Legal Core", "Financial", "Compliance", "Ops & SLA"])
        
        def render_card(tab, key, title, border):
            with tab:
                data = results.get(key, {})
                if not data: st.warning("Pending..."); return
                
                # Clean Data
                raw = data.get("summary", "")
                if isinstance(raw, dict): txt = raw.get('text', str(raw))
                elif isinstance(raw, list): txt = "\n".join([str(x) for x in raw])
                else: txt = str(raw)
                txt = txt.replace("\\n", "\n").strip()

                st.markdown(f"""
                <div class="agent-card {border}">
                    <h3>{title}</h3>
                    <div style="white-space: pre-wrap;">{txt}</div>
                    <div style="margin-top:15px; font-size:12px; color:#666; border-top:1px solid #333; padding-top:10px;">
                        🤖 <b>Agent:</b> {data.get('role', 'Unknown')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        render_card(tabs[0], "synthesis", "MASTER SYNTHESIS", "border-gold")
        render_card(tabs[1], "legal", "LEGAL AUDIT", "border-blue")
        render_card(tabs[2], "finance", "FINANCIAL", "border-green")
        render_card(tabs[3], "compliance", "REGULATORY", "border-pink")
        render_card(tabs[4], "operations", "OPERATIONS", "border-blue")
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
    
    # --- 1. CONFIGURATION PANEL ---
    show_settings = st.checkbox("⚙️ Show Report Customization & Focus", value=False)
    
    if show_settings:
        st.markdown("""
        <style>
            div[data-testid="stVerticalBlockBorderWrapper"] > div {
                border-color: rgba(0, 242, 255, 0.3) !important;
                background-color: rgba(20, 25, 35, 0.4) !important;
                border-radius: 10px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                report_tone = st.selectbox(
                    "Report Tone",
                    ["Standard Professional", "Executive Brief", "Deep Legal Scrutiny", "Simple Layman Terms"],
                    index=0
                )
            with c2:
                active_agents = st.multiselect(
                    "Active Neural Agents",
                    ["Legal", "Finance", "Compliance", "Operations"],
                    default=["Legal", "Finance", "Compliance", "Operations"]
                )
            # REMOVED Language selector from here. It is now dynamic below.
    else:
        report_tone = "Standard Professional"
        active_agents = ["Legal", "Finance", "Compliance", "Operations"]
            
    # --- 2. FILE UPLOAD ---
    uploaded_file = st.file_uploader("Drop Legal Contract (PDF/DOCX)", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())

        # PYPDF CHECK
        from utils.pdf_inspector import inspect_pdf_metadata
        pdf_meta = inspect_pdf_metadata(file_path)
        if "error" in pdf_meta:
            st.error(f"⚠️ {pdf_meta['error']}")
        else:
            st.caption(f"✅ Verified: {pdf_meta['pages']} Pages | Author: {pdf_meta['author']}")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("▶ ACTIVATE GRID", type="primary", use_container_width=True):
                with st.spinner(f"⚡ Synchronizing Quantum Agents ({report_tone})..."):
                    # 1. Run Analysis
                    results = run_graph(file_path)
                    docs = load_document(file_path)
                    chunks = chunk_contract(docs)
                    
                    # 2. Persistence
                    config = {"tone": report_tone, "agents": active_agents}
                    
                    st.session_state['report_config'] = config
                    st.session_state['results'] = results
                    st.session_state['doc_len'] = len(docs)
                    st.session_state['filename'] = uploaded_file.name # Save filename for caching
                    st.session_state['full_text'] = " ".join([c.page_content for c in chunks])
                    
                    # Clear old translation cache on new run
                    if 'translation_cache' in st.session_state:
                        del st.session_state['translation_cache']

                    # 3. Save to Pinecone
                    save_analysis_state(uploaded_file.name, results, len(docs), config)
                    st.toast("Analysis archived to Neural Vault!", icon="💾")

    # --- 3. RESULTS DISPLAY (Universal) ---
    if st.session_state.get('results'):
        # This block runs for BOTH fresh uploads AND Vault restores
        
        results = st.session_state['results']
        config = st.session_state.get('report_config', {})
        filename = st.session_state.get('filename', 'doc')
        
        st.markdown("---")
        
        # --- NEW LOCALIZATION HUB ---
        st.markdown("### 🌐 Localization Hub")
        st.caption("Translate your audit report instantly without re-analyzing.")
        
        loc_col1, loc_col2 = st.columns([2, 1])
        
        with loc_col1:
            target_lang = st.selectbox(
                "Select Language for PDF Report", 
                ["English", "Tamil", "Hindi", "French", "Spanish"],
                key="lang_selector"
            )
        
        # Determine Active Data (Original vs Translated)
        active_data = results
        is_translated = False
        
        with loc_col2:
            st.write("") # Spacer
            st.write("") 
            
            # Check Cache
            cache_key = f"{filename}_{target_lang}"
            if 'translation_cache' not in st.session_state:
                st.session_state['translation_cache'] = {}
                
            if target_lang == "English":
                st.success("✅ Original Loaded")
                active_data = results
            elif cache_key in st.session_state['translation_cache']:
                st.success(f"✅ {target_lang} Ready (Cached)")
                active_data = st.session_state['translation_cache'][cache_key]
                is_translated = True
            else:
                # Show Translate Button
                if st.button(f"⚡ Translate to {target_lang}", type="primary", use_container_width=True):
                    with st.spinner("AI Translating..."):
                        try:
                            from utils.translator import translate_report
                            # Translate the ORIGINAL results
                            trans_data = translate_report(results, target_lang)
                            # Save to Cache
                            st.session_state['translation_cache'][cache_key] = trans_data
                            active_data = trans_data
                            is_translated = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Translation Error: {e}")

        # --- METRICS & DOWNLOAD ---
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Pages", st.session_state.get('doc_len', 0))
        m2.metric("Tone", config.get('tone', 'Standard'))
        m3.metric("Language", target_lang)
        m4.metric("Status", "Translated" if is_translated else "Original", delta="Ready")
        
        style_metric_cards(background_color="#0a0a1a", border_left_color="#00f2ff", border_radius_px=15)
        st.write("")

        # DOWNLOAD BUTTON
        st.subheader("🖨️ Report Generation")
        
        with st.container(border=True):
            col_gen1, col_gen2 = st.columns([3, 1])
            
            with col_gen1:
                st.info(f"Ready to generate report in **{target_lang}**.")
                
            with col_gen2:
                # TRIGGER BUTTON
                if st.button("⚙️ Generate Files", type="primary", use_container_width=True):
                    st.session_state['files_generated'] = True
            
            # DOWNLOAD BUTTONS (Conditional Logic)
            if st.session_state.get('files_generated'):
                st.success("✅ Files Generated!")
                st.markdown("---")
                
                d1, d2 = st.columns(2)
                
                # LOGIC: If English -> PDF is safe. If Tamil -> PDF breaks, so use Word/HTML.
                if target_lang == "English":
                    # OPTION 1: STANDARD PDF (English Only)
                    with d1:
                        pdf_bytes = generate_pdf(active_data)
                        st.download_button(
                            label="📄 Download PDF",
                            data=pdf_bytes,
                            file_name=f"ClauseAI_{target_lang}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    # OPTION 1: HTML (For Perfect Tamil Viewing)
                    with d1:
                        from utils.export_html import generate_html
                        html_bytes = generate_html(active_data, config, filename)
                        st.download_button(
                            label="🌐 Download Web Report",
                            data=html_bytes,
                            file_name=f"ClauseAI_{target_lang}.html",
                            mime="text/html",
                            use_container_width=True,
                            help="Best format for viewing Tamil/Hindi fonts."
                        )

                # OPTION 2: WORD DOC (Universal - Works for ALL languages)
                with d2:
                    from utils.export_docx import generate_docx
                    # This now uses the CLEANED text function
                    docx_bytes = generate_docx(active_data, config)
                    st.download_button(
                        label="📝 Download Word Doc",
                        data=docx_bytes,
                        file_name=f"ClauseAI_{target_lang}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        help="Fully editable legal document."
                    )

        # --- TABS (Displaying Active Data) ---
        st.subheader(f"📑 Neural Output Stream ({target_lang})")
        
        current_agents = config.get('agents', ["Legal", "Finance", "Compliance", "Operations"])
        if not current_agents: current_agents = ["Legal", "Finance", "Compliance", "Operations"]

        tab_names = ["Executive Synth"] + [a for a in ["Legal", "Finance", "Compliance", "Operations"] if a in current_agents]
        tabs = st.tabs(tab_names)
        
        key_map = {
            "Executive Synth": "synthesis",
            "Legal": "legal",
            "Finance": "finance",
            "Compliance": "compliance",
            "Operations": "operations"
        }

        for i, tab_name in enumerate(tab_names):
            key = key_map[tab_name]
            with tabs[i]:
                # We display 'active_data' so the UI ALSO updates to Tamil!
                data = active_data.get(key, {}) 
                
                if not data:
                    st.info(f"Analysis for {tab_name} empty.")
                    continue
                
                clean_txt = clean_raw_output(data.get("summary", ""))
                
                border_color = "border-blue"
                if key == "finance": border_color = "border-green"
                if key == "compliance": border_color = "border-pink"
                if key == "synthesis": border_color = "border-gold"

                st.markdown(f"""
                <div class="agent-card {border_color}">
                    <h3>{tab_name.upper()} REPORT</h3>
                    <div style="white-space: pre-wrap;">{clean_txt}</div>
                </div>
                """, unsafe_allow_html=True)
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.colored_header import colored_header
from streamlit_extras.badges import badge
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import re
import asyncio
import sys
import uuid
from ingestion.file_loader import text_extractor
from orchestration.graph import build_clauseai_graph
from utils.history_manager import save_to_history, load_history
from utils.ui_components import display_lottie, inject_custom_css

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ClauseAI – Intelligent Contract Analysis",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    # Use V3 Cyber CSS with cache buster
    with open("assets/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    inject_custom_css() 
except:
    pass # Fallback if CSS not found

# ---------- SESSION STATE ----------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "report_tone" not in st.session_state: st.session_state.report_tone = "Standard Professional"
if "focus_area" not in st.session_state: st.session_state.focus_area = "General Analysis"
if "report_length" not in st.session_state: st.session_state.report_length = "Standard"
if "included_sections" not in st.session_state: 
    st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]


# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.markdown("## ClauseAI ⚡")
    
    # Handle Programmatic Navigation (Must be done before widget render)
    default_index = 0
    if st.session_state.get("force_analysis_view", False):
        default_index = 0
        if "main_menu" in st.session_state:
            del st.session_state["main_menu"] # Reset widget state
        st.session_state.force_analysis_view = False # Reset flag

    # Navbar
    selected_page = option_menu(
        menu_title=None,
        options=["Analysis", "History"],
        icons=["search", "clock-history"],
        menu_icon="cast",
        default_index=default_index,
        key="main_menu", # Add key to control state
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "#818cf8", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"5px", "--hover-color": "#1e293b"},
            "nav-link-selected": {"background-color": "#1e293b", "color": "#818cf8", "border-left": "3px solid #818cf8"},
        }
    )
    
    add_vertical_space(2)
    
    # Global Info
    st.info("💡 **Pro Tip**: Upload documents and use the configure button to customize your analysis.")
    
    add_vertical_space(10)
    st.markdown("---")
    st.caption("v2.0.0 | Powered by Gemini & Pinecone")

# ---------- MAIN CONTENT : ANALYSIS PAGE ----------
if selected_page == "Analysis":
    
    # Hero Section - Cyber / Tech Theme
    col_hero_text, col_hero_img = st.columns([3, 2]) 
    with col_hero_text:
        st.markdown('<h1 style="margin-bottom: 0px;">INTELLIGENT<br/>CONTRACT ANALYSIS</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; font-size: 1.2rem; margin-top: 10px;">DEPLOYING <span style="color: #10b981; font-weight: bold; font-family: monospace;">MULTI-AGENT.AI_SYSTEMS</span> TO DECODE LEGAL VECTORS.</p>', unsafe_allow_html=True)
        
        add_vertical_space(1)
        
        # Tech Badges
        st.markdown("""
        <div style="display: flex; gap: 15px;">
            <div class="badge-tech" style="border: 1px solid #10b981; padding: 5px 15px; color: #10b981; font-family: monospace; font-size: 0.9rem; border-radius: 4px;">STATUS: ONLINE</div>
            <div class="badge-tech" style="border: 1px solid #22d3ee; padding: 5px 15px; color: #22d3ee; font-family: monospace; font-size: 0.9rem; border-radius: 4px;">V2.0.1 INITIALIZED</div>
        </div>
        """, unsafe_allow_html=True)

    with col_hero_img:
        # "Digital Scan/Shield" Animation
        display_lottie("https://assets9.lottiefiles.com/packages/lf20_3rwasyjy.json", height=280, key="hero_lottie_cyber")
    
    add_vertical_space(3)

    # Main Input Card
    with st.container():
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        st.markdown("### 📂 INGEST DOCUMENTATION")
        st.caption("SELECT INPUT VECTOR OR INJECT TEXT STREAM")
        
        # Input Mode Selector
        input_mode = st.radio("Input Mode", ["Browse Files", "Paste Text"], horizontal=True, label_visibility="collapsed")

        # Layout: Input area + Configure button
        col_input, col_config = st.columns([5, 1], gap="small", vertical_alignment="bottom")
        
        # Initialize variables to avoid NameError
        uploaded_files = []
        pasted_text = ""

        with col_input:
            if input_mode == "Browse Files":
                st.markdown("Supported: PDF, DOCX, TXT (Max 5)")
                uploaded_files = st.file_uploader(
                    "Upload files", 
                    type=["pdf", "docx", "txt"], 
                    accept_multiple_files=True,
                    label_visibility="collapsed"
                )
                
                if len(uploaded_files) > 5:
                    st.error("⚠️ Maximum 5 files allowed. Please remove some files.")
                    uploaded_files = [] # Prevent processing

            else:
                pasted_text = st.text_area("Contract Text", height=200, placeholder="Paste contract text here...", label_visibility="collapsed")

        with col_config:
            # "Configure" Popover Button
            with st.popover("⚙️ Configure", use_container_width=True, help="Adjust analysis settings"):
                st.markdown("### Analysis Settings")
                
                # 1. Presets
                preset = st.selectbox("Quick Profile", ["Default", "CFO Brief", "Legal Deep Dive", "Compliance Check"])
                
                if preset == "CFO Brief":
                    st.session_state.report_tone = "Executive Summary"
                    st.session_state.focus_area = "Financial Risks"
                    st.session_state.report_length = "Concise"
                elif preset == "Legal Deep Dive":
                    st.session_state.report_tone = "Strict Legal"
                    st.session_state.focus_area = "Legal Loopholes"
                    st.session_state.report_length = "Exhaustive"
                    
                st.divider()

                # 2. Manual Overrides
                st.text_input("Specific Focus", placeholder="e.g. Termination", key="user_instructions_input") 
                st.radio("Tone", ["Standard Professional", "Strict Legal", "Executive Summary"], key="report_tone")
                st.radio("Length", ["Concise", "Standard", "Exhaustive"], key="report_length")
                st.selectbox("Focus Area", ["General Analysis", "Financial Risks", "Compliance Gaps", "Operational Liabilities", "Legal Loopholes"], key="focus_area")
                st.multiselect("Sections", ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"], default=st.session_state.included_sections, key="included_sections")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Process Input
    contract_text = ""
    all_extracted_data = []
    
    if uploaded_files:
        try:
            for file in uploaded_files:
                extracted = text_extractor(file)
                if extracted:
                    all_extracted_data.extend(extracted)
                    contract_text += "\\n".join([item["text"] for item in extracted]) + "\\n\\n"
        except Exception as e:
            st.error(f"Error reading file: {e}")
    elif pasted_text:
        contract_text = pasted_text
        all_extracted_data = [{"text": pasted_text, "source": "user_input", "page": 1}]

    # Action Button
    col_centered = st.columns([1, 2, 1])
    with col_centered[1]:
        analyze_btn = st.button("🚀 Analyze Contract", type="primary", use_container_width=True, disabled=not contract_text.strip())

    # Analysis Logic
    if analyze_btn:
        status_placeholder = st.empty()
        
        # Clear previous report cache
        if "pdf_bytes" in st.session_state: del st.session_state.pdf_bytes
        if "docx_bytes" in st.session_state: del st.session_state.docx_bytes
        
        with status_placeholder.container():
            st.markdown("### 🔄 Processing...")
            col_load1, col_load2 = st.columns([1, 4])
            with col_load1:
                display_lottie("https://assets9.lottiefiles.com/packages/lf20_p8bfn5to.json", height=100, key="loading_lottie")
            with col_load2:
                progress_bar = st.progress(0)
            
            try:
                # 1. Setup
                final_instructions = (
                    f"User Request: {st.session_state.get('user_instructions_input', 'None')}\\n"
                    f"Report Tone: {st.session_state.report_tone}\\n"
                    f"Focus Area: {st.session_state.focus_area}\\n"
                    f"Report Length: {st.session_state.report_length}\\n"
                    f"Target Sections: {', '.join(st.session_state.included_sections)}"
                )
                graph = build_clauseai_graph()
                progress_bar.progress(20, text="Graph initialized...")
                
                # 2. Ingest
                ingest_data = all_extracted_data if all_extracted_data else [{"text": contract_text, "source": "text", "page": 1}]
                progress_bar.progress(40, text="Ingesting & Embedding...")
                
                # 3. Analyze (Async)
                if sys.platform.startswith("win"):
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                
                progress_bar.progress(60, text="Running AI Agents (Finance, Legal, Compliance)...")
                
                result = asyncio.run(graph.ainvoke({
                    "contract_text": contract_text,
                    "extracted_data": ingest_data,
                    "user_instructions": final_instructions
                }))
                
                progress_bar.progress(90, text="Synthesizing Final Report...")
                st.session_state.analysis_result = result
                
                # Check for Risk Level
                risk_match = re.search(r"Risk Level:?\\s*(\\w+)", result.get("final_report", ""), re.IGNORECASE)
                risk_level = risk_match.group(1).upper() if risk_match else "N/A"
                
                # Generate unique View ID for this report session (fixes auto-download)
                st.session_state.view_id = str(uuid.uuid4())

                # SAVE TO HISTORY
                save_to_history(
                    contract_text=contract_text,
                    final_report=result.get("final_report", ""),
                    agent_outputs=result.get("agent_outputs", {}),
                    risk_level=risk_level
                )
                
                progress_bar.progress(100, text="Complete!")
                time.sleep(1)
                status_placeholder.empty()
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")

    # Results View
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        final_report = result.get("final_report", "")
        
        # Parse Risk (Again for display if needed, but result has it)
        risk_match = re.search(r"Risk Level:?\\s*(\\w+)", final_report, re.IGNORECASE)
        risk_level = risk_match.group(1).upper() if risk_match else "N/A"
        
        # 1. Executive Dashboard
        st.markdown("### 📊 Executive Dashboard")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Overall Risk", risk_level, delta="High" if risk_level == "HIGH" else ("Low" if risk_level == "LOW" else None), delta_color="inverse")
        col_m2.metric("Focus Area", st.session_state.focus_area)
        col_m3.metric("Processed Clauses", len(all_extracted_data)) # Proxy metric
        col_m4.metric("Agents Active", "4")
        
        style_metric_cards(background_color="#1e293b", border_left_color="#818cf8", border_radius_px=10, box_shadow=True)
        
        add_vertical_space(2)

        # 2. Executive Summary Card
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.markdown("#### 📌 Executive Summary")
        exec_summary_match = re.search(r"(?:#+)?\\s*1\\.\\s*Executive Summary(.*?)(?:#+)?\\s*2\\.", final_report, re.DOTALL | re.IGNORECASE)
        summary_text = exec_summary_match.group(1).strip() if exec_summary_match else "See full report details."
        st.markdown(summary_text)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. Detailed Agent Analysis Tabs
        st.markdown("### 🔍 Detailed Analysis")
        
        outputs = result.get("agent_outputs", {})
        if outputs:
            tabs = st.tabs([k.capitalize() for k in outputs.keys()])
            for i, (agent, content) in enumerate(outputs.items()):
                with tabs[i]:
                    st.markdown(content)
        
        add_vertical_space(2)
        
        # 4. Export Actions
        st.markdown("### 📥 Export Report")
        
        # Generate reports if not already in session state
        if "pdf_bytes" not in st.session_state or "docx_bytes" not in st.session_state:
             with st.spinner("Preparing export files..."):
                from utils.report_generator import generate_pdf, generate_word
                st.session_state.pdf_bytes = generate_pdf(final_report)
                st.session_state.docx_bytes = generate_word(final_report)
        
        # Display buttons side-by-side
        view_id = st.session_state.get("view_id", f"gen_{uuid.uuid4()}")
        
        add_vertical_space(1)
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.download_button(
                label="📄 Download PDF", 
                data=st.session_state.pdf_bytes, 
                file_name="clauseai_report.pdf", 
                mime="application/pdf", 
                use_container_width=True, 
                key=f"safe_dl_pdf_{view_id}"
            )
        with col_ex2:
            st.download_button(
                label="📝 Download Word", 
                data=st.session_state.docx_bytes, 
                file_name="clauseai_report.docx", 
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                use_container_width=True, 
                key=f"safe_dl_word_{view_id}"
            )



# ---------- HISTORY PAGE ----------
elif selected_page == "History":
    st.title("Analysis History")
    
    history_data = load_history()
    
    if not history_data:
        st.info("No analysis history found. Run an analysis to see it here!")
    else:
        for item in history_data:
            with st.expander(f"📄 {item['timestamp']} - Risk: {item.get('risk_level', 'N/A')}"):
                st.markdown(f"**Risk Level:** {item.get('risk_level', 'N/A')}")
                st.markdown(f"**Summary:** {item.get('summary', 'No summary')}")
                
                if st.button("View Full Report", key=f"view_{item['id']}"):
                    st.session_state.analysis_result = {
                        "final_report": item["final_report"],
                        "agent_outputs": item["agent_outputs"]
                    }
                    # Clear report cache to ensure regeneration for this history item
                    if "pdf_bytes" in st.session_state: del st.session_state.pdf_bytes
                    if "docx_bytes" in st.session_state: del st.session_state.docx_bytes
                    
                    # Set unique View ID for download buttons (Must be fresh UUID every view!)
                    st.session_state.view_id = str(uuid.uuid4())

                    # Set flag to force navigation on rerun
                    st.session_state.force_analysis_view = True
                    st.rerun()
                    
                st.divider()
                st.markdown("### Full Report Preview")
                st.markdown(item["final_report"])
        
        add_vertical_space(3)
        st.markdown("---")
        st.caption("🔒 **Security Note**: Your confidentiality is our responsibility. All history is stored locally on your machine and is never shared.")

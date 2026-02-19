from ingestion.file_loader import text_extractor
from orchestration.graph import build_clauseai_graph
import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="ClauseAI – Contract Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Session State Initialization ----------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620601.png", width=50) # Placeholder icon
    st.title("ClauseAI")
    st.markdown("Automated Contract Analysis System")
    st.divider()
    st.info(
        """
        **How it works:**
        1.  **Upload**: Submit your contract (PDF/DOCX/TXT).
        2.  **Context**: Provide specific focus areas (optional).
        3.  **Analysis**: Our multi-agent AI (Finance, Legal, Compliance) analyzes the document.
        4.  **Report**: Receive a comprehensive, structured strategic report.
        """
    )
    st.divider()
    st.warning(
        "**Disclaimer**: This tool is an AI assistant for document analysis and does not constitute professional legal advice. Always consult with a qualified attorney for final contract review."
    )
    st.divider()
    st.caption("Powered by Gemini 1.5 Pro & Pinecone Vector DB")
    
    # Session state initialization for customization is handled in main flow now
    if "report_tone" not in st.session_state: st.session_state.report_tone = "Standard Professional"
    if "focus_area" not in st.session_state: st.session_state.focus_area = "General Analysis"
    if "report_length" not in st.session_state: st.session_state.report_length = "Standard"
    if "included_sections" not in st.session_state: 
        st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]


# ---------- Main Content ----------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("ClauseAI - AI Powered Legal Contract Analyzer")
    st.markdown("### Intelligent insights for your legal documents")
st.divider()

# ---------- Input Section ----------
input_container = st.container()

with input_container:
    input_mode = st.radio(
        "**Select Input Method:**",
        ["Upload Contract File", "Paste Contract Text"],
        horizontal=True
    )

    contract_text = ""

    if input_mode == "Upload Contract File":
        uploaded_files = st.file_uploader(
            "Upload contract file(s)",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT. Max 5 files.",
            accept_multiple_files=True
        )

        if uploaded_files:
            if len(uploaded_files) > 5:
                st.error("⚠️ Maximum limit is 5 files.")
            else:
                try:
                    all_text_parts = []
                    all_extracted_data = []

                    for file in uploaded_files:
                        extracted_list = text_extractor(file)
                        if extracted_list:
                            all_extracted_data.extend(extracted_list)
                            file_text = "\n".join([item["text"] for item in extracted_list])
                            all_text_parts.append(file_text)
                    
                    contract_text = "\n\n".join(all_text_parts)
                    
                    if contract_text.strip():
                        st.success(f"✅ {len(uploaded_files)} file(s) processed successfully.")
                        with st.expander("📄 View Extracted Text"):
                            st.text_area("Extracted Content", contract_text, height=200, disabled=True)
                    else:
                        st.warning("⚠️ Uploaded files contain no readable text.")

                except Exception as e:
                    st.error(f"❌ Error reading file: {e}")

    else:
        contract_text = st.text_area(
            "Paste contract text here",
            height=300,
            placeholder="Paste the full contract text here..."
        )
        # For pasted text, create a dummy extracted_data structure
        all_extracted_data = [{"text": contract_text, "source": "user_input", "page": 1}]

# ---------- Configuration & Execution (Conditional) ----------
analyze_clicked = False

if contract_text.strip():
    st.divider()
    
    # st.divider()
    
    # Layout: Instructions (Left) | Customization Button (Right)
    # We want "Specific Instructions" taking most space, and "Customize" on the right.
    
    # Layout: Instructions (Left) | Customization Button (Right)
    # User requested same row, same height components.
    
    # 1. Label row (outside to avoid offset issues)
    st.markdown("**Specific Instructions (Optional):**")
    
    # 2. Input and Button row
    # Vertical alignment "center" or "top" works best when components are naturally similar height
    col_instr, col_cust = st.columns([3, 1], vertical_alignment="top")
    
    with col_instr:
        # Switching to text_input to match button height perfectly
        user_instructions = st.text_input(
            "Instructions",
            placeholder="E.g., Focus specifically on termination clauses...",
            help="These instructions will guide the specialized agents.",
            label_visibility="collapsed"
        )

    with col_cust:
        # Popover for Customization
        with st.popover("⚙️ Customize Report", use_container_width=True):
            # Header row with "Report Settings" and simple "Reset" button
            # Align center to fix "upside" reset button
            col_head, col_reset = st.columns([3, 1], vertical_alignment="center")
            
            with col_head:
                st.markdown("### Report Settings")
            with col_reset:
                # User requested "minimal and no symbols just the reset text and small box"
                if st.button("Reset", key="reset_customization", help="Reset to defaults"):
                     st.session_state.report_tone = "Standard Professional"
                     st.session_state.focus_area = "General Analysis"
                     st.session_state.report_length = "Standard"
                     st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]
                     st.rerun()
            
            # --- Presets (Quick Profiles) ---
            st.markdown("**Quick Profiles**")
            # "Not in fit mode" + "Specific height equal for both"
            # We use use_container_width=True to fill space equally. 
            # Vertical alignment ensures they sit well.
            col_p1, col_p2 = st.columns(2, vertical_alignment="center")
            
            with col_p1:
                if st.button("🚀 CFO Brief", help="Sets: Executive Tone, Concise Length, Financial Focus", use_container_width=True):
                    st.session_state.report_tone = "Executive Summary (Brief)"
                    st.session_state.focus_area = "Financial Risks"
                    st.session_state.report_length = "Concise"
                    st.session_state.included_sections = ["Executive Summary", "Financial Analysis"]
                    st.rerun()
                    
            with col_p2:
                if st.button("⚖️ Legal Deep Dive", help="Sets: Strict Legal Tone, Exhaustive Length, Legal Loophole Focus", use_container_width=True):
                    st.session_state.report_tone = "Strict Legal"
                    st.session_state.focus_area = "Legal Loopholes"
                    st.session_state.report_length = "Exhaustive"
                    st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Legal Risks"]
                    st.rerun()

            st.divider()
            
            # 1. Tone
            st.radio(
                "Report Tone",
                ["Standard Professional", "Executive Summary (Brief)", "Plain English (Simplified)", "Strict Legal"],
                key="report_tone",
                help="Controls the writing style and vocabulary of the final report."
            )
            
            st.divider()
            
            # 2. Length
            st.radio(
                "Report Length",
                ["Concise", "Standard", "Exhaustive"],
                key="report_length",
                help="Determines the depth of detail and total word count."
            )
            
            st.divider()

            # 3. Focus
            st.radio(
                "Focus Area",
                ["General Analysis", "Financial Risks", "Compliance Gaps", "Operational Liabilities", "Legal Loopholes"],
                key="focus_area",
                help="Prioritizes specific types of risks and clauses in the analysis."
            )
            
            st.divider()
            
            # 4. Included Sections (Checkboxes)
            # Hack to add a tooltip to a "header" - use a column or just caption
            st.markdown("**Included Sections**", help="Select which sections to include in the final report.")
            
            all_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]
            
            # Sync checkboxes with session state list
            for section in all_sections:
                is_checked = section in st.session_state.included_sections
                if st.checkbox(section, value=is_checked, key=f"chk_{section}"):
                    if section not in st.session_state.included_sections:
                        st.session_state.included_sections.append(section)
                else:
                    if section in st.session_state.included_sections:
                        st.session_state.included_sections.remove(section)

    st.write("#####") # Spacing

# Make button always visible but disabled if no text
analyze_clicked = st.button(
    "🚀 Start Analysis",
    type="primary",
    use_container_width=True,
    disabled = not bool(contract_text.strip())
)

# ---------- Analysis Logic ----------
if analyze_clicked:
    if not contract_text.strip():
        st.error("Please provide contract text before starting analysis.")
    else:
        with st.status("🤖 Orchestrating AI Agents...", expanded=True) as status:
            try:
                # Construct Final Instructions from UI State
                final_instructions = (
                    f"User Request: {user_instructions}\n"
                    f"Report Tone: {st.session_state.report_tone}\n"
                    f"Focus Area: {st.session_state.focus_area}\n"
                    f"Report Length: {st.session_state.report_length}\n"
                    f"Target Sections: {', '.join(st.session_state.included_sections)}"
                )

                st.write("Initializing workflow graph...")
                graph = build_clauseai_graph()
                
                with st.spinner("📄 Ingesting and embedding document chunks..."):
                    # Use passed data or fallback to text
                    input_data = all_extracted_data if 'all_extracted_data' in locals() and all_extracted_data else [{"text": contract_text, "source": "user_input", "page": 1}]
                    # Small delay to visual comfort if needed, but actual logic matches
                    
                with st.spinner("🕵️‍♂️ Running multi-agent analysis (Finance, Legal, Compliance, Operations)..."):
                    # Use asyncio.run for async graph execution
                    import asyncio
                    result = asyncio.run(graph.ainvoke({
                        "contract_text": contract_text,
                        "extracted_data": input_data,
                        "user_instructions": final_instructions
                    }))
                
                with st.spinner("📝 Synthesizing final strategic report..."):
                    st.session_state.analysis_result = result
                    
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

            except Exception as e:
                status.update(label="❌ Analysis Failed", state="error")
                st.error(f"An error occurred during analysis: {e}")

# ---------- Results Display ----------
if st.session_state.analysis_result:
    st.divider()
    result = st.session_state.analysis_result
    
    st.subheader("📊 Analysis Report")
    
    # Domain Tag
    domain = result.get("plan", {}).get("domain", "General")
    st.caption(f"**Detected Domain:** {domain}")
    
    # Final Report
    full_report = result.get("final_report", "No report generated.")
    
    # --- EXECUTIVE DASHBOARD (Point 4) ---
    # Extract Executive Summary if present
    import re
    import time
    
    # Helper for Typewriter Effect (Point 23)
    def stream_data(text):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)

    # Look for "1. Executive Summary" or "## 1. Executive Summary" up to the next section
    # The next section usually starts with "2." or "## 2."
    exec_summary_match = re.search(r"(?:#+)?\s*1\.\s*Executive Summary(.*?)(?:#+)?\s*2\.", full_report, re.DOTALL | re.IGNORECASE)
    
    if exec_summary_match:
        summary_text = exec_summary_match.group(1).strip()
        with st.container():
            st.info(f"### 📌 Executive Summary\n\n{summary_text}")
    
    # Full Report Container
    with st.expander("📄 View Full Strategic Report", expanded=True):
        # Logic to stream only once
        if "report_streamed" not in st.session_state or st.session_state.get("last_result_id") != id(result):
            st.write_stream(stream_data(full_report))
            st.session_state.report_streamed = True
            st.session_state.last_result_id = id(result)
        else:
            st.markdown(full_report)

    # --- AGENT TABS (Point 6) ---
    st.write("#####")
    st.subheader("🔍 Detailed Agent Analysis")
    
    outputs = result.get("agent_outputs", {})
    if outputs:
        # Create tabs dynamically based on available agents
        tab_names = [name.capitalize() for name in outputs.keys()]
        tabs = st.tabs(tab_names)
        
        for i, (agent_name, agent_output) in enumerate(outputs.items()):
            with tabs[i]:
                st.markdown(f"**Analysis from {agent_name.capitalize()} Agent:**")
                st.markdown(agent_output)

    # ---------- Download Section ----------
    st.subheader("📥 Download Report")
    
    from utils.report_generator import generate_pdf, generate_word
    
    report_text = result.get("final_report", "No report content.")
    
    col_d1, col_d2 = st.columns([1, 2])
    
    with col_d1:
        format_choice = st.radio("Select Format:", ["PDF", "Word (DOCX)"])
        
    with col_d2:
        st.write("#####") # Spacing to align with radio
        if format_choice == "PDF":
            pdf_bytes = generate_pdf(report_text)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="clauseai_report.pdf",
                mime="application/pdf"
            )
        else:
            docx_bytes = generate_word(report_text)
            st.download_button(
                label="📝 Download Word Report",
                data=docx_bytes,
                file_name="clauseai_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

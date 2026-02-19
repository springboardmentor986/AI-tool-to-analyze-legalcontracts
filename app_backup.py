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
    st.caption("Powered by Gemini 1.5 Pro & Pinecone Vector DB")
    st.divider()
    st.warning(
        "**Disclaimer**: This tool is an AI assistant for document analysis and does not constitute professional legal advice. Always consult with a qualified attorney for final contract review."
    )
    
    # --- Session State for Customization ---
    if "report_tone" not in st.session_state: st.session_state.report_tone = "Standard Professional"
    if "focus_area" not in st.session_state: st.session_state.focus_area = "General Analysis"
    if "report_length" not in st.session_state: st.session_state.report_length = "Standard"
    if "included_sections" not in st.session_state: 
        st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]

    # --- Presets (Quick Profiles) ---
    st.divider()
    st.markdown("**Quick Profiles**")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        if st.button("🚀 CFO Brief", help="Sets: Executive Tone, Concise Length, Financial Focus"):
            st.session_state.report_tone = "Executive Summary (Brief)"
            st.session_state.focus_area = "Financial Risks"
            st.session_state.report_length = "Concise"
            st.session_state.included_sections = ["Executive Summary", "Financial Analysis"]
            
    with col_p2:
        if st.button("⚖️ Legal Deep Dive", help="Sets: Strict Legal Tone, Exhaustive Length, Legal Loophole Focus"):
            st.session_state.report_tone = "Strict Legal"
            st.session_state.focus_area = "Legal Loopholes"
            st.session_state.report_length = "Exhaustive"
            st.session_state.included_sections = ["Executive Summary", "Compliance Analysis", "Legal Risks"]

    # --- Customization Options ---
    st.divider()
    st.header("Report Customization")
    
    # 1. Tone
    st.radio(
        "Report Tone",
        ["Standard Professional", "Executive Summary (Brief)", "Plain English (Simplified)", "Strict Legal"],
        key="report_tone",
        help="Controls the writing style and vocabulary of the final report."
    )
    
    st.divider()
    
    # 2. Length (New Point 3)
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
    
    # 4. Section Toggles (New Point 5)
    all_sections = ["Executive Summary", "Compliance Analysis", "Financial Analysis", "Legal Risks", "Operational Notes"]
    st.multiselect(
        "Included Sections",
        all_sections,
        key="included_sections",
        help="Select which sections to include in the final report."
    )

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

# ---------- Configuration & Execution ----------
st.divider()

user_instructions = st.text_area(
    "**Specific Instructions (Optional):**",
    height=100,
    placeholder="E.g., Focus specifically on termination clauses and indemnity caps...",
    help="These instructions will guide the specialized agents."
)

st.write("#####") # Spacing

analyze_clicked = st.button(
    "🚀 Start Analysis",
    type="primary",
    use_container_width=True,
    disabled=(not contract_text.strip())
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
    report_container = st.container(border=True)
    with report_container:
        st.markdown(result.get("final_report", "No report generated."))
    
    # Agent Details Expander
    with st.expander("🔍 View Detailed Agent Outputs"):
        outputs = result.get("agent_outputs", {})
        for agent, output in outputs.items():
            st.markdown(f"**{agent.capitalize()}:**")
            st.text(str(output)[:500] + "...") # Preview
            st.divider()

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

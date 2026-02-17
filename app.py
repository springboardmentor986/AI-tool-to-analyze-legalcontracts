"""
Streamlit UI for Multi-Agent Legal Contract Analyzer
"""

import streamlit as st
import os
from dotenv import load_dotenv
from multi_agent_analyzer import MultiAgentContractAnalyzer
import tempfile

st.set_page_config(page_title="Legal Contract Analyzer", page_icon="⚖️")

# Load environment variables
load_dotenv()

st.title("⚖️ Legal Contract Analyzer")
st.write("Upload a contract (PDF or Word) for AI analysis")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])

if uploaded_file:
    if st.button("Analyze Contract"):
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name
        
        try:
            with st.spinner("Analyzing contract..."):
                # Initialize analyzer (uses OLLAMA configuration from .env)
                ollama_url = os.getenv("OLLAMA_BASE_URL")
                ollama_model = os.getenv("OLLAMA_MODEL")
                if not ollama_url or not ollama_model:
                    st.error("Ollama configuration not found. Please check your .env file.")
                    st.stop()
                    
                analyzer = MultiAgentContractAnalyzer()
                
                # Run analysis
                results = analyzer.analyze_contract(temp_path)
            
            st.success("Analysis complete!")
            
            # Display extracted clauses
            st.subheader("📑 Extracted Clauses (Parallel Processing)")
            if results.get('extracted_clauses'):
                tabs = st.tabs(["Compliance", "Finance", "Legal", "Operations"])
                
                domains = ['compliance', 'finance', 'legal', 'operations']
                for idx, domain in enumerate(domains):
                    with tabs[idx]:
                        clauses = results['extracted_clauses'].get(domain, [])
                        st.metric(f"{domain.capitalize()} Clauses", len(clauses))
                        
                        if clauses:
                            for i, clause in enumerate(clauses[:5], 1):  # Show top 5
                                with st.expander(f"{i}. {clause.clause_type.replace('_', ' ').title()}"):
                                    st.write(f"**Location:** {clause.location}")
                                    st.write(f"**Confidence:** {clause.confidence:.1%}")
                                    st.write(f"**Text:** {clause.text}")
                        else:
                            st.info(f"No {domain} clauses found in this contract.")
            
            # Display identified risks
            st.subheader("⚠️ Risk Identification (Structured Pipelines)")
            if results.get('identified_risks'):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔍 Compliance Risks")
                    compliance_risks = results['identified_risks'].get('compliance', [])
                    
                    if compliance_risks:
                        # Show severity distribution
                        severity_counts = {}
                        for risk in compliance_risks:
                            severity = risk.severity.value
                            severity_counts[severity] = severity_counts.get(severity, 0) + 1
                        
                        st.write(f"**Total:** {len(compliance_risks)} risks")
                        for severity, count in sorted(severity_counts.items()):
                            color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                            st.write(f"{color.get(severity, '⚪')} {severity}: {count}")
                        
                        # Show top risks
                        st.markdown("**Top Risks:**")
                        for risk in compliance_risks[:3]:
                            with st.expander(f"[{risk.severity.value}] {risk.category}"):
                                st.write(f"**Description:** {risk.description}")
                                st.write(f"**Evidence:** {risk.evidence}")
                                st.write(f"**Location:** {risk.location}")
                                st.info(f"**Recommendation:** {risk.recommendation}")
                
                with col2:
                    st.markdown("### 💰 Financial Risks")
                    finance_risks = results['identified_risks'].get('finance', [])
                    
                    if finance_risks:
                        # Show severity distribution
                        severity_counts = {}
                        for risk in finance_risks:
                            severity = risk.severity.value
                            severity_counts[severity] = severity_counts.get(severity, 0) + 1
                        
                        st.write(f"**Total:** {len(finance_risks)} risks")
                        for severity, count in sorted(severity_counts.items()):
                            color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                            st.write(f"{color.get(severity, '⚪')} {severity}: {count}")
                        
                        # Show top risks
                        st.markdown("**Top Risks:**")
                        for risk in finance_risks[:3]:
                            with st.expander(f"[{risk.severity.value}] {risk.category}"):
                                st.write(f"**Description:** {risk.description}")
                                st.write(f"**Evidence:** {risk.evidence}")
                                st.write(f"**Location:** {risk.location}")
                                st.info(f"**Recommendation:** {risk.recommendation}")
            
            # Milestone 2: Display contract classification and planning
            if results.get('contract_type') and results.get('analysis_plan'):
                st.subheader("🎯 Contract Classification")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Contract Type", 
                             results['contract_type'].replace('_', ' ').title())
                with col2:
                    plan = results['analysis_plan']
                    st.metric("Analysis Strategy", 
                             plan.get('execution_strategy', 'N/A').title())
                with col3:
                    st.metric("Analysis Depth", 
                             plan.get('recommended_depth', 'N/A').title())
                
                if plan.get('key_characteristics'):
                    st.info(f"**Key Characteristics:** {plan['key_characteristics']}")
                
                if plan.get('focus_areas'):
                    focus_tags = ' • '.join(plan['focus_areas'][:5])
                    st.caption(f"**Focus Areas:** {focus_tags}")
                
                st.divider()
            
            # Milestone 3: Display multi-turn discussions
            if results.get('discussion_summaries') and len(results['discussion_summaries']) > 0:
                st.subheader("💬 Agent Discussions (Multi-Turn Interactions)")
                st.info("Agents engaged in clarifying discussions when ambiguities were detected.")
                for i, discussion in enumerate(results['discussion_summaries'], 1):
                    with st.expander(f"Discussion {i}", expanded=False):
                        st.markdown(discussion)
                st.divider()
            
            # Display results
            st.subheader("📋 Executive Summary")
            if results.get('final_summary'):
                st.markdown(results['final_summary'])
            else:
                st.warning("Executive summary not available")
            
            st.subheader("🔍 Compliance Analysis")
            if results.get('compliance_analysis'):
                st.markdown(results['compliance_analysis'])
            else:
                st.warning("Compliance analysis not available")
            
            st.subheader("💰 Finance Analysis")
            if results.get('finance_analysis'):
                st.markdown(results['finance_analysis'])
            else:
                st.warning("Finance analysis not available")
            
            st.subheader("⚖️ Legal Analysis")
            if results.get('legal_analysis'):
                st.markdown(results['legal_analysis'])
            else:
                st.warning("Legal analysis not available")
            
            st.subheader("🔧 Operations Analysis")
            if results.get('operations_analysis'):
                st.markdown(results['operations_analysis'])
            else:
                st.warning("Operations analysis not available")
            
            # Show errors if any
            if results.get('errors'):
                with st.expander("⚠️ View Errors", expanded=False):
                    for error in results['errors']:
                        st.error(error)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            import traceback
            with st.expander("Show error details"):
                st.code(traceback.format_exc())
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

import streamlit as st
import os
from utils.docsloader import load_document, chunk_contract
from graph.doc_graph import run_graph

st.set_page_config(page_title="ClauseAI", layout="wide")

st.markdown("""
<style>
    /* Main Body Color */
    .stApp { background-color: #0b1f3a; color: #f5f7fa; font-family: 'Segoe UI', sans-serif; }
    
    /* Sidebar: Set to match the Body (Royal Blue) */
    section[data-testid="stSidebar"] { background-color: #0b1f3a; border-right: 1px solid rgba(212,175,55,0.35);}
    section[data-testid="stSidebar"] * { color: #f5f7fa; }
    
    /* Headers */
    h1, h2, h3 { color: #d4af37; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #102a43; 
        border-radius: 5px; 
        color: #d4af37; 
        padding: 10px 15px;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #d4af37 !important; 
        color: #0b1f3a !important; 
        font-weight: bold;
    }
    
    /* Prevent Text Overflow */
    .report-content {
        background-color: #102a43;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(212,175,55,0.2);
        word-wrap: break-word; /* Prevents overflow */
        white-space: pre-wrap; /* Preserves formatting */
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.title("ClauseAI Legal Document Analyzer")

with st.sidebar:
    st.header("📂 Contract Upload")
    uploaded_file = st.file_uploader("Upload Contract", type=["pdf","docx","txt"])
    st.info("System Components:\n- Planner\n- Legal Agent\n- Finance Agent\n- Compliance Agent\n- Operations Agent\n- Synthesis Reviewer")

if uploaded_file:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("🚀 Running Multi-Agent Parallel Analysis & Synthesis..."):
        results = run_graph(file_path)

    if "synthesis" in results and results["synthesis"].get("status") == "success":
        st.success("Analysis Complete!")
        
    st.subheader("🔍 Agent Analysis Results")

    # TABS: Shortened titles to prevent congestion
    tab_names = ["📝 Summary", "⚖️ Legal", "💰 Finance", "🛡️ Compliance", "⚙️ Ops"]
    tabs = st.tabs(tab_names)

    # Function to display content safely
    def display_agent(tab, key, title):
        with tab:
            if key in results and results[key].get("status") == "success":
                data = results[key]
                st.markdown(f"### {title}")
                st.markdown(f"**Role:** {data.get('role', 'Analyst')}")
                # Use a div class to handle text wrapping
                st.markdown(f'<div class="report-content">{data.get("summary")}</div>', unsafe_allow_html=True)
            elif key in results and results[key].get("status") == "error":
                st.error(f"Error: {results[key].get('message')}")
            else:
                st.info(f"{title} agent was not triggered for this document.")

    display_agent(tabs[0], "synthesis", "Executive Summary")
    display_agent(tabs[1], "legal", "Legal Analysis")
    display_agent(tabs[2], "finance", "Financial Analysis")
    display_agent(tabs[3], "compliance", "Compliance Analysis")
    display_agent(tabs[4], "operations", "Operations Analysis")

else:
    st.info("Please upload a contract to begin.")
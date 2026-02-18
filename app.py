import streamlit as st
from streamlit_option_menu import option_menu

# --- MODULE IMPORTS ---
from utils.styles import apply_custom_css, render_3d_cube
from utils.export_utils import generate_pdf
# UPDATE: Added ai_consultant to imports
from views import main_console, analytics, vault, architecture, oracle, ai_consultant

# 1. PAGE CONFIG
st.set_page_config(page_title="ClauseAI Ultimate", layout="wide", page_icon="✨")

# --- 🚨 SAFE CSS FIX: TARGET ONLY THE TOP-LEFT "OPEN" BUTTON 🚨 ---
st.markdown("""
    <style>
        /* ------------------------------------------------------------------- */
        /* 1. FIX THE "OPEN" BUTTON (Top Left)                               */
        /* This targets ONLY the toggle on the main screen.                  */
        /* ------------------------------------------------------------------- */
        
        /* Target the container for the collapsed sidebar control */
        [data-testid="stSidebarCollapsedControl"] {
            background-color: transparent !important;
            padding: 5px !important;
        }
        
        /* CRUSH the broken icon text (keyboard_double_arrow_right) */
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="stSidebarCollapsedControl"] span,
        [data-testid="stSidebarCollapsedControl"] svg {
            font-size: 0px !important; 
            color: transparent !important;
            width: auto !important;
        }

        /* REBUILD the button with "OPEN" text */
        [data-testid="stSidebarCollapsedControl"] button::after {
            content: "OPEN SIDEBAR";
            font-size: 14px !important;
            color: #00f2ff !important;
            font-weight: bold;
            background: rgba(14, 17, 23, 0.9);
            border: 1px solid #00f2ff;
            padding: 5px 15px;
            border-radius: 5px;
            display: block;
            visibility: visible;
            white-space: nowrap;
        }
    </style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------------------

# 2. APPLY CSS
apply_custom_css()

# 3. INITIALIZE STATE
if 'results' not in st.session_state: st.session_state['results'] = None
if 'doc_len' not in st.session_state: st.session_state['doc_len'] = 0
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = {"legal": [], "finance": [], "compliance": [], "operations": []}

# 4. SIDEBAR
with st.sidebar:
    render_3d_cube()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #00f2ff; margin:0; font-size: 26px;">CLAUSE.AI</h2>
        <p style="font-size: 10px; color: #64748b; margin:0; letter-spacing: 2px;">NEURAL AUDIT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    # NAVIGATION MENU (Updated with AI Consultant)
    selected = option_menu(
        menu_title=None,
        options=["Main Console", "The Oracle", "AI Consultant", "Data Analytics", "The Vault", "Neural Architecture"],
        icons=["hdd-network", "chat-dots-fill", "headset", "bar-chart-line-fill", "archive-fill", "diagram-3-fill"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00f2ff", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "color": "#94a3b8"},
            "nav-link-selected": {"background": "rgba(0, 242, 255, 0.1)", "color": "#fff", "border-left": "4px solid #00f2ff"},
        }
    )
    
    st.markdown("---")
    
    # MANUAL DOWNLOAD ONLY
    if st.session_state['results']:
        pdf_bytes = generate_pdf(st.session_state['results'])
        st.download_button(
            label="📄 Download Report",
            data=pdf_bytes,
            file_name="ClauseAI_Audit.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="pdf_download_btn"
        )

# 5. PAGE ROUTING
if selected == "Main Console":
    main_console.show()
elif selected == "The Oracle":
    oracle.show()
# --- NEW ROUTE ---
elif selected == "AI Consultant":
    ai_consultant.show()
# -----------------
elif selected == "Data Analytics":
    analytics.show()
elif selected == "The Vault":
    vault.show()
elif selected == "Neural Architecture":
    architecture.show()
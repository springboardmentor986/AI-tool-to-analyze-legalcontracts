import streamlit as st
from streamlit_option_menu import option_menu

# --- MODULE IMPORTS ---
from utils.styles import apply_custom_css, render_3d_cube
from utils.export_utils import generate_pdf
# Import the new view
from views import main_console, analytics, vault, architecture, oracle

# 1. PAGE CONFIG
st.set_page_config(page_title="ClauseAI Ultimate", layout="wide", page_icon="✨")

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
    
    # ADDED "THE ORACLE" TO THE MENU
    selected = option_menu(
        menu_title=None,
        options=["Main Console", "The Oracle", "Data Analytics", "The Vault", "Neural Architecture"],
        icons=["hdd-network", "chat-dots-fill", "bar-chart-line-fill", "archive-fill", "diagram-3-fill"], 
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
    oracle.show()  # <--- Loads the new full-page chat
elif selected == "Data Analytics":
    analytics.show()
elif selected == "The Vault":
    vault.show()
elif selected == "Neural Architecture":
    architecture.show()
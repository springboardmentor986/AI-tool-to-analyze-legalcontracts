import streamlit as st
from streamlit_option_menu import option_menu

# --- MODULE IMPORTS ---
from utils.styles import apply_custom_css, render_3d_cube
from utils.export_utils import generate_pdf
from utils import db
from views import main_console, analytics, vault, architecture, oracle, ai_consultant, auth, landing, payment

# 1. PAGE CONFIG
st.set_page_config(page_title="ClauseAI Ultimate", layout="wide", page_icon="✨")

# 2. INIT DATABASE & STATE
db.init_db()

if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'page' not in st.session_state: st.session_state['page'] = 'landing' # landing, login, signup, app
if 'plan' not in st.session_state: st.session_state['plan'] = 'Free'
if 'results' not in st.session_state: st.session_state['results'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = {"legal": [], "finance": [], "compliance": [], "operations": []}

# 3. GLOBAL STYLES (Footer & Sidebar Fix)
st.markdown("""
    <style>
        [data-testid="stSidebarCollapsedControl"] { background-color: transparent !important; padding: 5px !important; }
        [data-testid="stSidebarCollapsedControl"] button { font-size: 0px !important; color: transparent !important; }
        [data-testid="stSidebarCollapsedControl"] button::after {
            content: "MENU"; font-size: 14px !important; color: #00f2ff !important; font-weight: bold;
            background: rgba(14, 17, 23, 0.9); border: 1px solid #00f2ff; padding: 5px 15px; border-radius: 5px;
        }
        .footer {
            position: fixed; left: 0; bottom: 0; width: 100%; background-color: #0e1117;
            color: #64748b; text-align: center; padding: 10px; font-size: 12px;
            border-top: 1px solid #1e293b; z-index: 1000;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🎮 ROUTING LOGIC
# ==============================================================================

if not st.session_state['authenticated']:
    # --- PUBLIC PAGES ---
    if st.session_state['page'] == 'landing':
        landing.show()
    elif st.session_state['page'] == 'login':
        if st.button("← Back"): st.session_state['page'] = 'landing'; st.rerun()
        auth.login_form()
    elif st.session_state['page'] == 'signup':
        if st.button("← Back"): st.session_state['page'] = 'landing'; st.rerun()
        auth.signup_form()

else:
    # --- MAIN APPLICATION (LOGGED IN) ---
    apply_custom_css()
    
    with st.sidebar:
        render_3d_cube()
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #00f2ff; margin:0; font-size: 26px;">CLAUSE.AI</h2>
            <div style="background: #1e293b; padding: 5px; border-radius: 5px; margin-top: 10px; font-size: 12px; border: 1px solid #334155;">
                👤 <b>{}</b> | Plan: <span style="color: #00f2ff;">{}</span>
            </div>
        </div>
        """.format(st.session_state['username'], st.session_state['plan']), unsafe_allow_html=True)
        
        # NAVIGATION
        selected = option_menu(
            menu_title=None,
            options=["Main Console", "The Oracle", "AI Consultant", "Data Analytics", "The Vault", "Neural Architecture", "Billing & Plans"],
            icons=["hdd-network", "chat-dots-fill", "headset", "bar-chart-line-fill", "archive-fill", "diagram-3-fill", "credit-card-2-front"], 
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#00f2ff", "font-size": "16px"}, 
                "nav-link": {"font-size": "14px", "color": "#94a3b8"},
                "nav-link-selected": {"background": "rgba(0, 242, 255, 0.1)", "color": "#fff", "border-left": "4px solid #00f2ff"},
            }
        )
        
        st.markdown("---")
        if st.button("🔒 Logout", use_container_width=True):
            st.session_state['authenticated'] = False
            st.session_state['page'] = 'landing'
            st.rerun()

    # --- PAGE RENDERING & FEATURE LOCKING ---
    plan = st.session_state['plan']
    
    if selected == "Main Console":
        main_console.show()
        
    elif selected == "The Oracle":
        oracle.show()
        
    elif selected == "AI Consultant":
        # LOCK THIS FEATURE FOR FREE USERS
        if plan == 'Free':
            st.error("🔒 This feature is available on the PRO Plan.")
            st.markdown("Upgrade in **Billing & Plans** to unlock the AI Legal Avatar.")
            st.image("https://cdn.dribbble.com/users/32512/screenshots/5668419/ai-assistant-2.gif", width=300)
        else:
            ai_consultant.show()
            
    elif selected == "Data Analytics":
        analytics.show()
        
    elif selected == "The Vault":
        # LOCK THIS FEATURE FOR FREE USERS
        if plan == 'Free':
            st.error("🔒 The Vault (Unlimited Storage) is for PRO users only.")
        else:
            vault.show()
            
    elif selected == "Neural Architecture":
        architecture.show()
        
    elif selected == "Billing & Plans":
        payment.show()

# FOOTER
st.markdown("""
    <div class="footer">
        <p>© 2026 ClauseAI Inc. | Designed by <b>ARULDASS</b> | <span style="color: #00f2ff;">Springboard Internship Build v1</span></p>
    </div>
""", unsafe_allow_html=True)
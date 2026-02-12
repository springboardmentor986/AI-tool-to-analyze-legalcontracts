import streamlit as st
from streamlit_option_menu import option_menu

# --- MODULE IMPORTS ---
from utils.styles import apply_custom_css, render_3d_cube
from utils.universal_llm import universal_llm
from utils.export_utils import generate_pdf

# --- IMPORT VIEWS ---
# We will create these files next
from views import main_console, analytics, vault, architecture

# 1. PAGE CONFIG
st.set_page_config(page_title="ClauseAI Ultimate", layout="wide", page_icon="✨")

# 2. APPLY CSS (THE DESIGN ENGINE)
apply_custom_css()

# 3. INITIALIZE STATE
if 'results' not in st.session_state: st.session_state['results'] = None
if 'doc_len' not in st.session_state: st.session_state['doc_len'] = 0
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = {"legal": [], "finance": [], "compliance": [], "operations": []}

# 4. SIDEBAR
with st.sidebar:
    render_3d_cube() # The 3D Cube lives here!
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #00f2ff; margin:0; font-size: 26px;">CLAUSE.AI</h2>
        <p style="font-size: 10px; color: #64748b; margin:0; letter-spacing: 2px;">NEURAL AUDIT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Main Console", "Data Analytics", "The Vault", "Neural Architecture"],
        icons=["hdd-network", "bar-chart-line-fill", "archive-fill", "diagram-3-fill"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#00f2ff", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "color": "#94a3b8"},
            "nav-link-selected": {"background": "rgba(0, 242, 255, 0.1)", "color": "#fff", "border-left": "4px solid #00f2ff"},
        }
    )
    
    st.markdown("---")
    
    # MANUAL PDF DOWNLOAD (Milestone 4 Requirement)
    if st.session_state['results']:
        pdf_bytes = generate_pdf(st.session_state['results'])
        st.download_button(
            label="📄 Download Report",
            data=pdf_bytes,
            file_name="ClauseAI_Audit.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# 5. FLOATING CHAT WIDGET (Milestone 4 Requirement)
with st.popover("💬", help="Ask the Agents"):
    st.markdown("### 🧠 Neural Link")
    if not st.session_state['results']:
        st.warning("Analyze a contract first.")
    else:
        agent_tab = st.tabs(["Legal", "Finance", "Compliance", "Ops"])
        
        def render_chat(agent_name, tab_obj):
            with tab_obj:
                # History
                for msg in st.session_state['chat_history'][agent_name]:
                    st.markdown(f"**{msg['role'].title()}:** {msg['content']}")
                
                # Input
                q = st.text_input(f"Ask {agent_name}...", key=f"q_{agent_name}")
                if q:
                    # RAG Context
                    data = st.session_state['results'].get(agent_name, {})
                    context = str(data.get('summary', ''))
                    prompt = f"Role: {agent_name} Expert. Context: {context}. User Question: {q}"
                    
                    with st.spinner("..."):
                        ans = universal_llm.invoke(prompt).content
                        st.session_state['chat_history'][agent_name].append({"role": "user", "content": q})
                        st.session_state['chat_history'][agent_name].append({"role": "ai", "content": ans})
                        st.rerun()

        render_chat("legal", agent_tab[0])
        render_chat("finance", agent_tab[1])
        render_chat("compliance", agent_tab[2])
        render_chat("operations", agent_tab[3])

# 6. ROUTING
if selected == "Main Console":
    main_console.show()
elif selected == "Data Analytics":
    analytics.show()
elif selected == "The Vault":
    vault.show()
elif selected == "Neural Architecture":
    architecture.show()
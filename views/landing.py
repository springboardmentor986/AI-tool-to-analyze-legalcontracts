import streamlit as st
from views import auth

def show():
    # --- HERO SECTION ---
    st.markdown("""
        <style>
        .hero {
            padding: 5rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, #0e1117 0%, #1e293b 100%);
            border-bottom: 1px solid #334155;
        }
        .hero h1 {
            font-size: 60px;
            font-weight: 800;
            background: -webkit-linear-gradient(#eee, #333);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }
        .hero span {
            background: -webkit-linear-gradient(#00f2ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p {
            font-size: 20px;
            color: #94a3b8;
            margin-top: 10px;
        }
        .cta-btn {
            display: inline-block;
            background: #00f2ff;
            color: #000;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
            text-decoration: none;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .cta-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
        }
        </style>
        
        <div class="hero">
            <h1>CLAUSE.AI <span>ULTIMATE</span></h1>
            <p>The World's Most Advanced Neural Contract Auditor.</p>
            <p style="font-size: 14px;">AI Analysis • Risk Detection • Automated Consulting</p>
        </div>
    """, unsafe_allow_html=True)

    # --- ACTION BUTTONS ---
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.write("") # Spacer
        # Instead of HTML buttons, we use Streamlit buttons to control state
        col_login, col_signup = st.columns(2)
        with col_login:
            if st.button("🔐 Login", use_container_width=True, type="primary"):
                st.session_state['page'] = 'login'
                st.rerun()
        with col_signup:
            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state['page'] = 'signup'
                st.rerun()

    # --- FEATURES GRID ---
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Why Choose ClauseAI?</h3><br>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.info("**🚀 Neural Engine**\n\nScans contracts in seconds using advanced LLMs to find hidden risks.")
    with f2:
        st.success("**🤖 AI Consultant**\n\nReal-time video consultation with our digital legal expert.")
    with f3:
        st.warning("**📊 Analytics Vault**\n\nStore, organize, and visualize your contract data securely.")
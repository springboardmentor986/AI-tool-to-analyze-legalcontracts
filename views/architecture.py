import streamlit as st

def show():
    st.title("System Blueprint")
    st.markdown("""
    <div class="glass-panel">
        <h3 style="color:#fff !important;">🧬 Topology: Parallel Fan-Out Graph</h3>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top:20px;">
            <div style="background: linear-gradient(135deg, #00f2ff, #00c6ff); padding:5px 15px; border-radius:15px; color:black; font-weight:bold;">Ingestion</div>
            <div style="color:#555; padding-top:5px;">➜</div>
            <div style="background: linear-gradient(135deg, #ff00cc, #333399); padding:5px 15px; border-radius:15px; color:white; font-weight:bold;">Planner</div>
            <div style="color:#555; padding-top:5px;">➜</div>
            <div style="background: linear-gradient(135deg, #00ff87, #60efff); padding:5px 15px; border-radius:15px; color:black; font-weight:bold;">Parallel Agents</div>
            <div style="color:#555; padding-top:5px;">➜</div>
            <div style="background: linear-gradient(135deg, #fce38a, #f38181); padding:5px 15px; border-radius:15px; color:black; font-weight:bold;">Synthesis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
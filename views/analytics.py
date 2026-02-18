import streamlit as st
import pandas as pd
from utils.viz_utils import render_radar_chart

def show():
    st.title("📊 Data Analytics Center")
    
    if not st.session_state['results']:
        st.info("Please analyze a contract in 'Main Console' first.")
        return

    col1, col2 = st.columns([1, 1])
    risks = {"Legal": 80, "Financial": 45, "Privacy": 90, "SLA": 30, "IP": 65} 

    with col1:
        st.markdown('<div class="glass-panel"><h3>🕷️ Risk Radar</h3>', unsafe_allow_html=True)
        render_radar_chart(risks)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-panel"><h3>📉 Risk Distribution</h3>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"Category": list(risks.keys()), "Severity": list(risks.values())})
        # REMOVED use_container_width just to be safe if that was the warning source
        st.bar_chart(chart_data, x="Category", y="Severity", color="#ff00cc")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="glass-panel"><h3>📋 Detailed Metrics</h3>', unsafe_allow_html=True)
    df = pd.DataFrame([
        {"Metric": "Confidence Score", "Value": "98.2%"},
        {"Metric": "Processing Time", "Value": "1.4s"},
        {"Metric": "Tokens Used", "Value": "8,450"},
        {"Metric": "Cost Est.", "Value": "$0.002"}
    ])
    # Updated: Removed hide_index (deprecated in some versions) and use_container_width
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
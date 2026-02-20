import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from utils.history_manager import load_history

import re

def extract_agent_risk(text):
    if not isinstance(text, str):
        return 0
    # Look for common risk indicators
    matches = re.findall(r'(?i)\b(high|medium|low)\b', text)
    if not matches:
        return 0
    matches = [m.lower() for m in matches]
    if 'high' in matches:
        return 3
    if 'medium' in matches:
        return 2
    if 'low' in matches:
        return 1
    return 0

def render_dashboard():
    st.title("📊 Analytics Dashboard")
    st.caption("Insights derived from intelligent contract analysis history.")
    
    history_data = load_history()
    
    if not history_data:
        st.info("No analysis history found. Run an analysis to generate analytics.")
        return
        
    # Convert to DataFrame for timeline
    df = pd.DataFrame(history_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['risk_level'] = df['risk_level'].fillna("N/A").str.upper()
    df.loc[~df['risk_level'].isin(['LOW', 'MEDIUM', 'HIGH']), 'risk_level'] = 'N/A'
    
    # Selection Dropdown
    st.markdown("### 📄 Document Analysis Profiler")
    
    # Generate display labels for the history dropdown Menu
    # Sort history so newest items appear first
    sorted_history = sorted(history_data, key=lambda x: x['timestamp'], reverse=True)
    
    options = []
    for item in sorted_history:
        summary_snippet = item.get('summary', 'No summary')
        if isinstance(summary_snippet, str) and len(summary_snippet) > 50:
            summary_snippet = summary_snippet[:50] + "..."
        options.append(f"{item['timestamp']} | Risk: {item.get('risk_level', 'N/A')} | {summary_snippet}")
        
    selected_option = st.selectbox("Select a previously analyzed document:", options, index=0)
    
    # Find selected item
    selected_index = options.index(selected_option)
    selected_item = sorted_history[selected_index]
    
    st.markdown("---")
    
    # Render Visualizations Column 1 and 2
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Agent Risk Profile")
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        
        # Calculate scores for radar
        outputs = selected_item.get('agent_outputs', {})
        agents = ['Compliance', 'Finance', 'Legal', 'Operations']
        scores = [
            extract_agent_risk(outputs.get('compliance', '')),
            extract_agent_risk(outputs.get('finance', '')),
            extract_agent_risk(outputs.get('legal', '')),
            extract_agent_risk(outputs.get('operations', ''))
        ]
        
        # Close the loop
        radar_agents = agents + [agents[0]]
        radar_scores = scores + [scores[0]]
        text_labels = ['N/A' if s==0 else 'Low' if s==1 else 'Medium' if s==2 else 'High' for s in radar_scores]
        
        radar_df = pd.DataFrame(dict(
            Risk=radar_scores,
            Agent=radar_agents,
            Label=text_labels
        ))
        
        fig_radar = px.line_polar(
            radar_df, 
            r='Risk', 
            theta='Agent', 
            line_close=True,
            markers=True
        )
        
        fig_radar.update_traces(
            fill='toself', 
            fillcolor='rgba(34, 211, 238, 0.2)', # Cyan translucent
            line_color='#22d3ee',
            marker=dict(size=10),
            hovertemplate="<b>%{theta}</b><br>Risk Level: %{customdata[0]}<extra></extra>",
            customdata=radar_df[['Label']]
        )
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 3],
                    tickvals=[0, 1, 2, 3],
                    ticktext=['', 'Low', 'Medium', 'High'],
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                gridshape='linear', # Makes it a polygon instead of a circle
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=40, b=40, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown("#### Historical Activity Timeline")
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.caption("This chart displays the volume of contracts analyzed per day derived from your history. Peaks indicate high-activity days.")
        # Bar Chart
        df['Date'] = df['timestamp'].dt.date
        timeline_counts = df.groupby('Date').size().reset_index(name='Count')
        
        fig_bar = px.bar(
            timeline_counts, 
            x='Date', 
            y='Count',
            color_discrete_sequence=['#22d3ee'] # Cyan
        )
        fig_bar.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e2e8f0"),
            xaxis_title="Date",
            yaxis_title="Contracts Analyzed"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Document Summary Footer
    st.markdown("#### 📄 Document Summary")
    st.info(selected_item.get('summary', 'No summary available.'))

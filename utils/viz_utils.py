import plotly.graph_objects as go
import streamlit as st

def render_radar_chart(risks):
    """
    Renders a Cyberpunk Radar Chart for Risk Analysis.
    """
    categories = list(risks.keys())
    values = list(risks.values())
    
    # Close the loop
    categories = [*categories, categories[0]]
    values = [*values, values[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Risk Profile',
                line=dict(color='#00f2ff', width=3),
                fillcolor='rgba(0, 242, 255, 0.2)',
                marker=dict(size=8, color='#fff')
            )
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor='rgba(255,255,255,0.2)',
                gridcolor='rgba(255,255,255,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#e2e8f0'),
                linecolor='rgba(255,255,255,0.2)',
                gridcolor='rgba(255,255,255,0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
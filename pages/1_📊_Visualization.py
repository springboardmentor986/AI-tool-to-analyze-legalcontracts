import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Visualization Dashboard", layout="wide")

st.markdown("## 📊 Visualization Dashboard")

if "agent_results" not in st.session_state:
    st.warning("⚠️ Please analyze a contract first from the main page.")
    st.stop()

agent_results = st.session_state.agent_results


def safe_json_loads(text):
    try:
        return json.loads(text)
    except:
        return {}


# -----------------------------
# Risk Distribution Pie Chart
# -----------------------------
risks = []

for agent, content in agent_results.items():
    parsed = safe_json_loads(content)
    for c in parsed.get("clauses", []):
        risks.append(c.get("risk_level", "Low"))

if risks:
    df_risk = pd.DataFrame({"Risk Level": risks})
    fig1 = px.pie(
        df_risk,
        names="Risk Level",
        title="Overall Risk Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No risk data available.")


# -----------------------------
# Agent Risk Comparison Bar Chart
# -----------------------------
risk_map = {"Low": 1, "Medium": 2, "High": 3}
agent_scores = []

for agent, content in agent_results.items():
    parsed = safe_json_loads(content)
    risk = parsed.get("domain_summary", {}).get("overall_risk")
    if risk in risk_map:
        agent_scores.append({
            "Agent": agent,
            "Risk Score": risk_map[risk]
        })

if agent_scores:
    df_agents = pd.DataFrame(agent_scores)
    fig2 = px.bar(
        df_agents,
        x="Agent",
        y="Risk Score",
        title="Agent-wise Risk Comparison",
        range_y=[0, 3]
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No agent risk summary available.")

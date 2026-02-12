import streamlit as st
import pandas as pd
import plotly.express as px
import json
from collections import Counter

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="ClauseAI | Dashboard",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("📊 Visualization Dashboard")
st.caption("Contract Risk & Performance Insights")

st.divider()

# --------------------------------------------------
# CHECK DATA
# --------------------------------------------------
if "analysis_done" not in st.session_state or not st.session_state.analysis_done:
    st.warning("⚠️ Please analyze a contract first from the Home page.")
    st.stop()

agent_results = st.session_state.agent_results


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def safe_json(text):
    try:
        return json.loads(text)
    except:
        return {}


def extract_all_clauses(results):

    clauses = []

    for agent, content in results.items():

        parsed = safe_json(content)

        agent_clauses = parsed.get("clauses", [])

        # Fallback
        if not agent_clauses:
            summary = parsed.get("domain_summary", {})
            agent_clauses = [{
                "clause_type": f"{agent} Review",
                "risk_level": summary.get("overall_risk", "Medium"),
                "summary": " | ".join(summary.get("key_concerns", [])),
                "recommendation": " | ".join(summary.get("priority_actions", []))
            }]

        for c in agent_clauses:
            c["agent"] = agent
            clauses.append(c)

    return clauses


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
all_clauses = extract_all_clauses(agent_results)


# --------------------------------------------------
# METRICS
# --------------------------------------------------
def calculate_compliance():

    score_map = {"Low": 90, "Medium": 65, "High": 35}
    scores = []

    for agent, content in agent_results.items():

        parsed = safe_json(content)

        risk = parsed.get("domain_summary", {}).get("overall_risk", "Medium")

        scores.append(score_map.get(risk, 65))

    return int(sum(scores) / len(scores))


compliance_score = calculate_compliance()


# --------------------------------------------------
# TOP METRICS
# --------------------------------------------------
st.subheader("📌 Key Metrics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Contracts", 1)

with m2:
    st.metric("Total Clauses", len(all_clauses))

with m3:
    st.metric("Compliance Score", f"{compliance_score}%")

with m4:
    st.metric("Agents Used", len(agent_results))

st.divider()


# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Risk Overview",
    "📊 Agent Analysis",
    "📄 Clause Explorer"
])


# ==================================================
# TAB 1 — RISK OVERVIEW
# ==================================================
with tab1:

    st.subheader("Overall Risk Distribution")

    risks = [c.get("risk_level", "Medium") for c in all_clauses]

    risk_counts = Counter(risks)

    df_risk = pd.DataFrame({
        "Risk": risk_counts.keys(),
        "Count": risk_counts.values()
    })

    fig_pie = px.pie(
        df_risk,
        names="Risk",
        values="Count",
        hole=0.4,
        title="Clause Risk Distribution",
        color="Risk",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e74c3c"
        }
    )

    fig_pie.update_layout(height=420)

    st.plotly_chart(fig_pie, use_container_width=True)


# ==================================================
# TAB 2 — AGENT ANALYSIS
# ==================================================
with tab2:

    st.subheader("Agent-wise Risk Comparison")

    risk_map = {"Low": 1, "Medium": 2, "High": 3}

    data = []

    for agent, content in agent_results.items():

        parsed = safe_json(content)

        risk = parsed.get("domain_summary", {}).get("overall_risk", "Medium")

        data.append({
            "Agent": agent,
            "Risk Level": risk,
            "Score": risk_map.get(risk, 2)
        })

    df_agents = pd.DataFrame(data)

    fig_bar = px.bar(
        df_agents,
        x="Agent",
        y="Score",
        color="Risk Level",
        text="Risk Level",
        title="Agent Risk Assessment",
        color_discrete_map={
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e74c3c"
        }
    )

    fig_bar.update_layout(
        height=420,
        yaxis_range=[0, 3.5]
    )

    st.plotly_chart(fig_bar, use_container_width=True)


# ==================================================
# TAB 3 — CLAUSE EXPLORER
# ==================================================
with tab3:

    st.subheader("Important Clauses")

    if all_clauses:

        rows = []

        for c in all_clauses:
            rows.append({
                "Agent": c.get("agent"),
                "Type": c.get("clause_type"),
                "Risk": c.get("risk_level"),
                "Summary": c.get("summary"),
                "Recommendation": c.get("recommendation")
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No clauses found.")


# --------------------------------------------------
# FINAL VERDICT
# --------------------------------------------------
st.divider()

st.subheader("📌 Final Verdict")

if "verdict" in st.session_state:
    st.markdown(st.session_state.verdict)
else:
    st.info("Verdict not available")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption("ClauseAI Dashboard • Powered by Multi-Agent AI")

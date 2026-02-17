import streamlit as st
import pandas as pd
import altair as alt
import time

from parser import parse_pdf
from planner import plan_and_execute

st.set_page_config(
    page_title="CLAUSE.AI – Intelligent Contract Audit - By Asritha",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap');

:root {
    --bg-main: #020617;
    --glass-light: rgba(255,255,255,0.12);
    --glass-dark: rgba(255,255,255,0.04);
    --border-soft: rgba(255,255,255,0.16);
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;

    --accent-cyan: #22d3ee;
    --accent-blue: #38bdf8;
    --accent-indigo: #6366f1;
    --accent-green: #34d399;
    --accent-red: #fb7185;
    --accent-amber: #fbbf24;
}

* { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(600px circle at 15% 10%, rgba(99,102,241,0.25), transparent 40%),
        radial-gradient(500px circle at 85% 15%, rgba(34,211,238,0.22), transparent 45%),
        radial-gradient(700px circle at 50% 90%, rgba(56,189,248,0.18), transparent 50%),
        linear-gradient(180deg, #020617, #020617);
    color: var(--text-main);
}

#MainMenu, footer, header { visibility: hidden; }

.glass {
    background: linear-gradient(180deg, var(--glass-light), var(--glass-dark));
    backdrop-filter: blur(26px);
    border-radius: 28px;
    padding: 36px;
    border: 1px solid var(--border-soft);
    box-shadow: 0 40px 80px rgba(0,0,0,0.9);
    margin-bottom: 40px;
}

.section-title {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 16px;
}

.metric {
    background: rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px;
    border-left: 4px solid var(--accent-cyan);
}

.agent-box {
    background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.99));
    border-radius: 24px;
    padding: 28px;
    border-left: 5px solid var(--accent-blue);
}

.high { color: var(--accent-red); font-weight: 700; }
.medium { color: var(--accent-amber); font-weight: 700; }
.low { color: var(--accent-green); font-weight: 700; }

/* ---------- RISK DIVIDER ---------- */
.risk-divider {
    height: 1px;
    width: 100%;
    margin: 16px 0 18px 0;
    background: linear-gradient(
        to right,
        rgba(255,255,255,0.05),
        rgba(255,255,255,0.18),
        rgba(255,255,255,0.05)
    );
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="glass">
  <h1>✨ CLAUSE AI - INTELLIGENT CONTRACT AUDIT </h1>
  <p>
    Neural Parallel Grid executing multi-vector analysis across Legal, Finance,
    Compliance, and Operations with executive-grade AI synthesis.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📄 Upload Legal Contract</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    with open("temp_contract.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✓ Document uploaded: {uploaded_file.name}")

    text, chunks = parse_pdf("temp_contract.pdf")
    st.info(f"✓ Parsed into {len(chunks)} semantic chunks")

    with st.expander("📑 View Parsed Chunks"):
        for chunk in chunks[:25]:
            st.code(chunk[:400])

    if st.button("▶ ACTIVATE NEURAL GRID"):
        with st.spinner("🧠 Executing Parallel Risk Models..."):
            results = plan_and_execute(text)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🧠 MASTER SYNTHESIS</div>", unsafe_allow_html=True)
        st.markdown(results.get("Summary", "No executive synthesis generated."))
        st.markdown("</div>", unsafe_allow_html=True)

        rows = []
        severity_map = {"High": 3, "Medium": 2, "Low": 1}

        for domain, output in results.items():
            if not isinstance(output, list):
                continue
            for item in output:
                rows.append({
                    "Domain": domain,
                    "Severity": item["severity"],
                    "Score": severity_map[item["severity"]],
                    "Confidence": item["confidence"]
                })

        if rows:
            df = pd.DataFrame(rows)

            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>📊 SYSTEM TELEMETRY</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='metric'><h2>{len(df)}</h2>Total Risks</div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric'><h2>{df.Score.mean():.2f}</h2>Avg Severity</div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric'><h2>{int(df.Confidence.mean()*100)}%</h2>Confidence</div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='metric'><h2>{len(df[df.Severity=='High'])}</h2>Critical</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🔥 SEVERITY DISTRIBUTION</div>", unsafe_allow_html=True)

            heat = (
                df.groupby(["Domain", "Severity"])
                  .size()
                  .reset_index(name="Count")
            )

            chart = alt.Chart(heat).mark_rect().encode(
                x="Domain:N",
                y="Severity:N",
                color=alt.Color("Count:Q", scale=alt.Scale(scheme="teals")),
                tooltip=["Domain", "Severity", "Count"]
            ).properties(height=320)

            st.altair_chart(chart, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🤖 NEURAL OUTPUT STREAM</div>", unsafe_allow_html=True)

        cols = st.columns(4)
        agents = ["Legal", "Finance", "Compliance", "Operations"]

        for col, agent in zip(cols, agents):
            with col:
                st.markdown("<div class='agent-box'>", unsafe_allow_html=True)
                st.markdown(f"### {agent}")

                for item in results.get(agent, []):
                    sev = item["severity"].lower()
                    st.markdown(f"""
**Risk Type:** {item['risk_type']}  
**Severity:** <span class="{sev}">{item['severity']}</span>  
**Confidence:** {int(item['confidence']*100)}%

📄 *Clause Snapshot:*  
{item['clause'][:260]}
""", unsafe_allow_html=True)

                    st.markdown("<div class='risk-divider'></div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
<div class="glass" style="text-align:center;font-size:14px;color:#9ca3af;">
⚡ CLAUSE.AI • Neural Parallel Contract Intelligence Platform
</div>
""", unsafe_allow_html=True)

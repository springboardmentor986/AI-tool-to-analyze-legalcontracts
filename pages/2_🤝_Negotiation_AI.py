import streamlit as st
import json
from groq import Groq
import os

st.set_page_config(page_title="Negotiation AI", layout="wide")

st.markdown("## 🤝 Negotiation AI")

if "agent_results" not in st.session_state:
    st.warning("⚠️ Analyze a contract first.")
    st.stop()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_negotiation_points(agent_results):

    context = json.dumps(agent_results)[:6000]

    prompt = f"""
You are a contract negotiation assistant.

Based on the analysis below, suggest
practical negotiation points.

Rules:
- Max 6 points
- Short sentences
- Actionable
- Business-friendly language

Analysis:
{context}

Return as bullet points.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


if st.button("🔍 Generate Negotiation Suggestions"):
    with st.spinner("Thinking like a negotiator..."):
        suggestions = generate_negotiation_points(
            st.session_state.agent_results
        )
    st.markdown("### Suggested Negotiation Points")
    st.markdown(suggestions)

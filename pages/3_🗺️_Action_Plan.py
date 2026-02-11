import streamlit as st
import json
from groq import Groq
import os

st.set_page_config(page_title="Smart Action Plan", layout="wide")

st.markdown("## 🗺️ Smart Action Plan")

if "agent_results" not in st.session_state:
    st.warning("⚠️ Analyze a contract first.")
    st.stop()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_action_plan(agent_results):

    context = json.dumps(agent_results)[:6000]

    prompt = f"""
You are a contract advisor.

Create a clear, step-by-step
action plan for the user.

Rules:
- Max 6 steps
- Simple language
- No legal jargon
- Practical steps only

Analysis:
{context}

Return as numbered list.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


if st.button("📋 Generate Action Plan"):
    with st.spinner("Creating your action plan..."):
        plan = generate_action_plan(
            st.session_state.agent_results
        )
    st.markdown("### Your Personalized Action Plan")
    st.markdown(plan)

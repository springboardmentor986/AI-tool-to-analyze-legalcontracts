import streamlit as st
from contract_processor import process_contract
from config import APP_TITLE
from rag_chatbot import contract_chat

st.title(APP_TITLE)

# Sidebar customization
st.sidebar.header("Customization Panel")

tone = st.sidebar.selectbox("Select Tone", ["Formal", "Professional", "Simple"])
focus = st.sidebar.selectbox("Focus Area", ["Risk", "Compliance", "Summary"])
structure = st.sidebar.selectbox("Structure", ["Detailed", "Executive Summary"])

uploaded_files = st.file_uploader("Upload Contracts", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        content = file.read().decode(errors="ignore")

        report, risk_score = process_contract(content, tone, focus, structure)

        st.success("Report Generated Successfully!")
        st.metric("Risk Score", risk_score)
        st.text(report)

        st.download_button("Download Report", report, file_name="report.txt")

# ---------------- CHAT SECTION ---------------- #

st.header("Ask Questions About Contract")

user_question = st.text_input("Enter your question")

if user_question and uploaded_files:
    for file in uploaded_files:
        content = file.read().decode(errors="ignore")
        answer = contract_chat(content, user_question)
        st.write("Answer:", answer)

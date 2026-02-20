import csv

def save_feedback(rating, feedback_text):
    with open("feedback.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([rating, feedback_text])


import streamlit as st
from modules.workflow import run_clauseai
from datetime import datetime

st.set_page_config(page_title="ClauseAI", layout="wide")

st.title("ClauseAI - Contract Analysis System")

uploaded_file = st.file_uploader("Upload a contract (.txt)", type=["txt"])

if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")

    st.subheader("Document Preview")
    st.text_area("Preview", contract_text, height=200)

    st.subheader("Report Configuration")

    report_tone = st.selectbox(
        "Select Report Tone",
        ["Professional", "Simple Explanation", "Legal Expert", "Executive Summary"]
    )

    report_focus = st.selectbox(
        "Select Report Focus",
        ["Full Contract Analysis", "Risk Analysis Only", "Obligations Only", "Summary Only"]
    )


    if st.button("Generate Report"):

        with st.spinner("Generating AI Report..."):

            result = run_clauseai(contract_text, report_tone, report_focus)

        st.subheader("Generated Report")
        st.write(result)


        file_name = f"ClauseAI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        st.download_button(
            label="⬇ Download Report",
            data=result,
            file_name=file_name,
            mime="text/plain"
        )

        st.subheader("Provide Feedback")

        rating = st.slider("Rate this report (1-5)", 1, 5, 3)
        feedback_text = st.text_area("Additional Feedback")

        if st.button("Submit Feedback"):
            save_feedback(rating, feedback_text)
            st.success("Thank you for your feedback!")

import streamlit as st
import os

from utils.parser import load_document, chunk_text

from multi_agents.legal import legal_agent
from multi_agents.finance import finance_agent
from multi_agents.compliance import compliance_agent
from multi_agents.operations import operations_agent

st.set_page_config(page_title="ClauseAI", layout="wide")
st.title("ClauseAI Multi-Agent Contract Analyzer")

uploaded_file = st.file_uploader(
    "Upload Contract",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully.")

    text = load_document(file_path)

    if text.strip() == "":
        st.error("Text could not be extracted. Please upload a text-based document.")
        st.stop()

    chunks = chunk_text(text)

    if len(chunks) == 0:
        st.error("Text chunking failed.")
        st.stop()

    st.write("Total characters:", len(text))
    st.write("Total chunks:", len(chunks))

    st.subheader("Sample Chunk")
    st.write(chunks[0])

    st.subheader("Agent Outputs")

    st.write("Legal Analysis:", legal_agent(chunks[0]))
    st.write("Financial Analysis:", finance_agent(chunks[0]))
    st.write("Compliance Analysis:", compliance_agent(chunks[0]))
    st.write("Operational Analysis:", operations_agent(chunks[0]))

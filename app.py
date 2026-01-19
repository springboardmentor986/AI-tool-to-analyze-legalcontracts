import streamlit as st
import os

from utils.parser import load_document, chunk_text

from multi_agents.legal import legal_agent
from multi_agents.finance import finance_agent
from multi_agents.compliance import compliance_agent
from multi_agents.operations import operations_agent

st.set_page_config(page_title="ClauseAI", layout="wide")
st.title("ClauseAI – Multi-Agent Contract Analyzer")

uploaded_file = st.file_uploader(
    "Upload Contract",
    type=["pdf", "docx", "txt"]
)

if uploaded_file is not None:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully")

    text = load_document(file_path)

    if text.strip() == "":
        st.error("Text extract aagala. Text-based file upload pannu.")
        st.stop()

    chunks = chunk_text(text)

    if len(chunks) == 0:
        st.error("Chunks create aagala.")
        st.stop()

    st.write("Total characters:", len(text))
    st.write("Total chunks:", len(chunks))

    st.subheader("Sample Chunk")
    st.write(chunks[0])

    st.subheader("Agent Outputs")

    st.write("Legal:", legal_agent(chunks[0]))
    st.write("Finance:", finance_agent(chunks[0]))
    st.write("Compliance:", compliance_agent(chunks[0]))
    st.write("Operations:", operations_agent(chunks[0]))

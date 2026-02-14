import streamlit as st

from extract_text import extract_text
from chunk_text import chunk_text
from upload_chunks import upload_chunks

from finance_agent import FinanceAgent
from compliance_agent import ComplianceAgent
from legal_agent import LegalAgent
from operations_agent import OperationsAgent

st.set_page_config(
    page_title="Clause AI – Contract Analyzer",
    layout="wide"
)

st.title("Clause AI – Contract Analyzer")


if "full_text" not in st.session_state:
    st.session_state.full_text = ""

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


uploaded_file = st.file_uploader(
    "Drag and drop a contract (PDF / TXT)",
    type=["pdf", "txt"]
)

if uploaded_file:
    with st.spinner("Extracting text from document..."):
        try:
            st.session_state.full_text = extract_text(uploaded_file)
            st.session_state.uploaded = True
            st.session_state.analysis_done = False
        except Exception as e:
            st.error(f"Text extraction failed: {e}")


if st.session_state.uploaded:
    st.subheader(" Extracted Text (Preview)")
    st.text_area(
        "Document Text",
        st.session_state.full_text[:3000],
        height=220
    )

    chunks = chunk_text(st.session_state.full_text)

    st.subheader(" Text Chunks (Preview)")
    for i, chunk in enumerate(chunks[:5]):
        with st.expander(f"Chunk {i + 1}"):
            st.write(chunk)

   
    with st.spinner(" Uploading chunks to vector database..."):
        try:
            upload_chunks(chunks)
            st.success("Chunks uploaded successfully")
        except Exception as e:
            st.warning(f"Vector upload skipped: {e}")


st.divider()
st.header("Agent Analysis")

if st.session_state.uploaded:

    if st.button("Analyze Contract"):
        with st.spinner("Running AI agents..."):

            try:
                finance_agent = FinanceAgent()
                compliance_agent = ComplianceAgent()
                legal_agent = LegalAgent()
                operations_agent = OperationsAgent()

                st.session_state.finance_result = finance_agent.analyze(
                    st.session_state.full_text
                )
                st.session_state.compliance_result = compliance_agent.analyze(
                    st.session_state.full_text
                )
                st.session_state.legal_result = legal_agent.analyze(
                    st.session_state.full_text
                )
                st.session_state.operations_result = operations_agent.analyze(
                    st.session_state.full_text
                )

                st.session_state.analysis_done = True

            except Exception as e:
                st.error(f"Agent analysis failed: {e}")

        st.success(" Contract analysis completed!")

# ---------------- RESULTS ----------------
if st.session_state.analysis_done:
    st.subheader("Agent Outputs")

    with st.expander("Finance Agent", expanded=True):
        st.write(st.session_state.finance_result)

    with st.expander("Compliance Agent"):
        st.write(st.session_state.compliance_result)

    with st.expander("Legal Agent"):
        st.write(st.session_state.legal_result)

    with st.expander("Operations Agent"):
        st.write(st.session_state.operations_result)

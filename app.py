"""
ClauseAI - AI-Powered Contract Analysis System
Streamlit Application
"""

import streamlit as st
from vector_store import store_chunks_in_vector_store, query_index, initialize_pinecone
from sentence_transformers import SentenceTransformer
import docx2txt
from PyPDF2 import PdfReader
import os

# -----------------------------
# 🔹 Streamlit page config
# -----------------------------
st.set_page_config(
    page_title="ClauseAI - Contract Analysis",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# 🔹 Initialize session state
# -----------------------------
if 'embed_model' not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

if 'pinecone_initialized' not in st.session_state:
    st.session_state.pinecone_initialized = False

# -----------------------------
# 🔹 Header
# -----------------------------
st.title("📄 ClauseAI - Contract Analysis System")
st.markdown("Upload your legal contracts for AI-powered analysis")

# -----------------------------
# 🔹 Sidebar - Configuration
# -----------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Pinecone API Key input
    api_key = st.text_input(
        "Pinecone API Key",
        type="password",
        help="Enter your Pinecone API key"
    )
    
    if api_key:
        os.environ["PINECONE_API_KEY"] = api_key
        if not st.session_state.pinecone_initialized:
            with st.spinner("Initializing Pinecone..."):
                if initialize_pinecone():
                    st.session_state.pinecone_initialized = True
                    st.success("✅ Pinecone connected!")
                else:
                    st.error("❌ Failed to connect to Pinecone")
    
    st.divider()
    
    # Chunk size configuration
    chunk_size = st.slider(
        "Chunk Size (characters)",
        min_value=200,
        max_value=1000,
        value=500,
        step=50
    )
    
    # Top-k results
    top_k = st.slider(
        "Number of Results",
        min_value=1,
        max_value=10,
        value=5
    )

# -----------------------------
# 🔹 Main content area
# -----------------------------
tab1, tab2 = st.tabs(["📤 Upload Document", "🔍 Query Analysis"])

# ===== TAB 1: UPLOAD =====
with tab1:
    st.header("Upload Contract Document")
    
    uploaded_file = st.file_uploader(
        "Upload a PDF or DOCX file",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )
    
    if uploaded_file:
        try:
            # Extract text based on file type
            with st.spinner("Extracting text from document..."):
                if uploaded_file.type == "application/pdf":
                    reader = PdfReader(uploaded_file)
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    text = docx2txt.process(uploaded_file)
                else:
                    st.error("❌ Unsupported file format")
                    st.stop()
            
            # Display document stats
            st.success(f"✅ File loaded successfully: **{uploaded_file.name}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Characters", f"{len(text):,}")
            with col2:
                st.metric("Total Words", f"{len(text.split()):,}")
            with col3:
                num_chunks = len(text) // chunk_size + (1 if len(text) % chunk_size else 0)
                st.metric("Chunks", num_chunks)
            
            # Show preview
            with st.expander("📖 Document Preview"):
                st.text_area("First 1000 characters:", text[:1000], height=200)
            
            # Process and store button
            if st.button("🚀 Process & Store in Vector Database", type="primary"):
                if not st.session_state.pinecone_initialized:
                    st.error("❌ Please configure Pinecone API key in the sidebar first")
                    st.stop()
                
                with st.spinner("Processing document..."):
                    # Split into chunks
                    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                    
                    # Create embeddings
                    embeddings = st.session_state.embed_model.encode(chunks).tolist()
                    
                    # Store in Pinecone with metadata
                    metadata = {
                        "filename": uploaded_file.name,
                        "file_type": uploaded_file.type,
                        "total_chunks": len(chunks)
                    }
                    
                    store_chunks_in_vector_store(chunks, embeddings, metadata)
                    
                    st.success(f"✅ Successfully processed and stored {len(chunks)} chunks!")
                    st.balloons()
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.exception(e)

# ===== TAB 2: QUERY =====
with tab2:
    st.header("Query Contract Database")
    
    if not st.session_state.pinecone_initialized:
        st.warning("⚠️ Please configure Pinecone API key in the sidebar to enable querying")
    else:
        query = st.text_input(
            "Enter your query",
            placeholder="e.g., What are the payment terms? Who are the parties involved?"
        )
        
        if st.button("🔍 Search", type="primary") and query:
            with st.spinner("Searching..."):
                try:
                    # Create query embedding
                    query_embedding = st.session_state.embed_model.encode([query])[0].tolist()
                    
                    # Query Pinecone
                    results = query_index(query_embedding, top_k=top_k)
                    
                    # Display results
                    st.subheader(f"Top {len(results)} Results")
                    
                    for i, res in enumerate(results, 1):
                        with st.expander(f"Result {i} - Score: {res['score']:.4f}"):
                            st.markdown(f"**Relevance Score:** {res['score']:.4f}")
                            
                            # Show metadata if available
                            if 'filename' in res['metadata']:
                                st.markdown(f"**Source:** {res['metadata']['filename']}")
                            
                            st.markdown("**Text:**")
                            st.write(res['text'])
                            
                            # Show full metadata
                            with st.expander("View Metadata"):
                                st.json(res['metadata'])
                
                except Exception as e:
                    st.error(f"❌ Error during search: {str(e)}")
                    st.exception(e)

# -----------------------------
# 🔹 Footer
# -----------------------------
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    ClauseAI v1.0 - AI-Powered Contract Analysis | Built with Streamlit & LangChain
    </div>
    """,
    unsafe_allow_html=True
)
import time
import uuid
import json
import os
import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Import Keys
try:
    from config import PINECONE_API_KEY, INDEX_NAME
except ImportError:
    st.error("🚨 Error: Could not import 'config.py'.")
    PINECONE_API_KEY = None
    INDEX_NAME = None

# 3. Initialize Embedding Model
# We will use this to "Test" the dimension size dynamically
try:
    gemini_key = os.getenv("gemini_api_key") 
    
    if not gemini_key:
        st.error("🚨 Error: 'gemini_api_key' missing in .env")
        embeddings = None
    else:
        # We try to use the standard model. 
        # If it outputs 3072, our code below will now handle it.
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=gemini_key
        )
except Exception as e:
    st.error(f"⚠️ Embeddings Failed: {e}")
    embeddings = None

def get_embedding_dimension():
    """
    Runs a dummy test to see exactly how many dimensions 
    your specific API key/Model is generating.
    """
    if not embeddings: return 768
    try:
        # Embed a single word to measure the vector size
        test_vec = embeddings.embed_query("test")
        return len(test_vec)
    except Exception as e:
        st.warning(f"Could not determine embedding dimension: {e}")
        return 768 # Default fallback

def get_index():
    """
    Connects to Pinecone. 
    AUTO-CREATES the index with the CORRECT dimensions.
    """
    if not PINECONE_API_KEY:
        st.error("🚨 Error: PINECONE_API_KEY missing in config.py")
        return None

    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # --- AUTO-CREATION LOGIC ---
        existing_indexes = [i.name for i in pc.list_indexes()]
        
        if INDEX_NAME not in existing_indexes:
            # 1. Detect the ACTUAL dimension your system is producing
            detected_dim = get_embedding_dimension()
            
            st.warning(f"⚠️ Index '{INDEX_NAME}' not found. Creating it with {detected_dim} dimensions (Auto-Detected)...")
            try:
                pc.create_index(
                    name=INDEX_NAME,
                    dimension=detected_dim, # <--- DYNAMIC DIMENSION
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                time.sleep(10) # Wait for initialization
                st.success(f"✅ Index created successfully with {detected_dim} dimensions!")
            except Exception as create_err:
                st.error(f"Failed to create index: {create_err}")
                return None
        # ---------------------------

        # Connect
        return pc.Index(INDEX_NAME)
            
    except Exception as e:
        st.error(f"❌ Pinecone Connection Failed: {str(e)}")
        return None

# --- ALIAS ---
def get_pinecone_client():
    return get_index()

def save_analysis_state(filename, results, doc_len):
    index = get_index()
    if not index or not embeddings: return False

    try:
        scan_id = str(uuid.uuid4())
        payload = json.dumps(results)[:38000] 
        vector = embeddings.embed_query(filename)
        
        metadata = {
            "type": "APP_STATE", 
            "filename": filename,
            "doc_len": doc_len,
            "date": time.strftime("%Y-%m-%d"),
            "analysis_json": payload
        }

        index.upsert(vectors=[(scan_id, vector, metadata)])
        return True
    except Exception as e:
        st.error(f"Pinecone Save Failed: {e}")
        return False

def search_archives(query):
    index = get_index()
    if not index or not embeddings: return []

    try:
        query_vec = embeddings.embed_query(query)
        results = index.query(
            vector=query_vec,
            top_k=10,
            include_metadata=True,
            filter={"type": "APP_STATE"} 
        )
        
        archives = []
        for match in results['matches']:
            md = match['metadata']
            archives.append({
                "id": match['id'],
                "filename": md.get('filename', 'Unknown'),
                "date": md.get('date', 'N/A'),
                "score": match['score'],
                "doc_len": int(md.get('doc_len', 0)),
                "analysis_json": md.get('analysis_json', '{}')
            })
        return archives
        
    except Exception as e:
        st.error(f"Pinecone Search Failed: {e}")
        return []
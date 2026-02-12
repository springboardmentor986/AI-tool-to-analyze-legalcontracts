import streamlit as st
import json
# --- IMPORT THE SEARCHER ---
from utils.pinecone_client import search_archives

def show():
    st.title("🗄️ Neural Archives (The Vault)")
    st.markdown("<p style='color:#94a3b8'>Retrieve past contract analyses from Pinecone.</p>", unsafe_allow_html=True)
    
    # 1. SEARCH INPUT
    query = st.text_input("Search Archives...", placeholder="e.g., 'Employment' or 'SLA'", key="vault_search")
    
    # Default query to show *something* if empty (optional, or wait for button)
    search_query = query if query else "Contract" 

    # 2. PERFORM REAL SEARCH
    if st.button("🔍 Search Pinecone") or query:
        with st.spinner("Scanning Vector Space..."):
            # CALL REAL API
            archives = search_archives(search_query)
            
        if not archives:
            st.warning("No archives found. Try analyzing a document in 'Main Console' first.")
        else:
            st.success(f"Found {len(archives)} archived records.")
            
            # 3. RENDER RESULTS
            st.markdown("---")
            for doc in archives:
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    
                    with col_a:
                        st.markdown(f"### 📄 {doc['filename']}")
                        st.caption(f"Archived on: {doc['date']} | Size: {doc['doc_len']} Pages")
                    
                    with col_b:
                        match_score = int(doc['score'] * 100)
                        st.markdown(f"**Match:** {match_score}%")
                        
                    with col_c:
                        # THE REAL LOAD BUTTON
                        if st.button("⚡ LOAD", key=f"load_{doc['id']}", use_container_width=True):
                            try:
                                # A. Parse the JSON string back to Dict
                                restored_results = json.loads(doc['analysis_json'])
                                
                                # B. Hydrate Session State
                                st.session_state['results'] = restored_results
                                st.session_state['doc_len'] = doc['doc_len']
                                
                                # C. Reset Chat for new context
                                st.session_state['chat_history'] = {
                                    "legal": [], "finance": [], "compliance": [], "operations": []
                                }
                                
                                st.toast(f"Restored {doc['filename']}!", icon="✅")
                                
                            except Exception as e:
                                st.error(f"Corrupt Archive Data: {e}")
                
                st.markdown("---")

    # Help Tip
    if st.session_state.get('results'):
        st.info("💡 **System Active:** Analysis loaded. Go to 'The Oracle' to chat with this contract.")
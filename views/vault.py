import streamlit as st
import json
from utils.pinecone_client import search_archives

def show():
    st.markdown("## 🏦 The Neural Vault")
    st.markdown("<p style='color:#94a3b8'>Retrieve past contract analyses from Pinecone.</p>", unsafe_allow_html=True)
    
    # 1. SEARCH INPUT (Press Enter to search)
    query = st.text_input("Search Archives...", placeholder="e.g., 'Employment' or 'SLA'", key="vault_search")
    
    # 2. PERFORM SEARCH
    if query:
        with st.spinner("Scanning Vector Space..."):
            archives = search_archives(query)
            
        if not archives:
            st.warning("No archives found.")
        else:
            st.success(f"Found {len(archives)} archived records.")
            st.markdown("---")
            
            # 3. RENDER RESULTS
            cols = st.columns(3)
            for i, doc in enumerate(archives):
                with cols[i % 3]:
                    with st.container():
                        # Clean HTML Card Style
                        st.markdown(f"""
                        <div style="background: #0e1117; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px;">
                            <h4 style="color: #00f2ff; margin:0;">📄 {doc['filename']}</h4>
                            <p style="font-size: 12px; color: #666;">{doc['date']} • {doc['doc_len']} Pages</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # THE LOAD BUTTON
                        if st.button(f"⚡ LOAD", key=doc['id'], use_container_width=True):
                            try:
                                # A. Load Analysis Data
                                payload = doc.get('analysis_json', '{}')
                                st.session_state['results'] = json.loads(payload)
                                st.session_state['doc_len'] = doc['doc_len']
                                st.session_state['filename'] = doc['filename']
                                
                                # B. Load Config (THIS FIXES THE MISSING TABS)
                                config_str = doc.get('config_json', None)
                                
                                if config_str and config_str != '{}':
                                    st.session_state['report_config'] = json.loads(config_str)
                                else:
                                    # Fallback for old files: Show ALL tabs
                                    st.session_state['report_config'] = {
                                        "tone": "Restored",
                                        "agents": ["Legal", "Finance", "Compliance", "Operations"]
                                    }

                                # C. Reset Chat
                                st.session_state['chat_history'] = {"legal": [], "finance": [], "compliance": [], "operations": []}
                                
                                st.toast(f"Restored {doc['filename']}!", icon="✅")
                                st.rerun() # Refresh to show tabs immediately
                                
                            except Exception as e:
                                st.error(f"Corrupt Data: {e}")

    # Help Tip
    if st.session_state.get('results'):
        st.info("💡 **System Active:** Analysis loaded. Go to 'The Oracle' to chat.")
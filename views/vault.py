import streamlit as st

def show():
    st.title("🗄️ Neural Archives (Pinecone)")
    st.markdown("<p style='color:#94a3b8'>Retrieve past contract vectors.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text_input("Search Contract Vectors...", placeholder="e.g., 'NDA' or 'Payment Terms'")
    with c2:
        st.write("")
        st.write("")
        if st.button("Search DB"):
            st.success("Connected to Pinecone Index: 'contract-analysis'")
            # Mock results for demo
            results = [
                {"file": "Vendor_SLA_v2.pdf", "score": 92},
                {"file": "Employment_Agreement.docx", "score": 88},
                {"file": "Service_Contract_2024.pdf", "score": 75}
            ]
            for res in results:
                st.markdown(f"""
                <div class="glass-panel" style="padding:15px; display:flex; justify-content:space-between; align-items:center;">
                    <span>📄 <b>{res['file']}</b></span>
                    <span style="color:#00ff87">Match: {res['score']}%</span>
                    <button style="background:none; border:1px solid #00f2ff; color:#00f2ff; border-radius:5px; padding:5px 10px;">Load Data</button>
                </div>
                """, unsafe_allow_html=True)